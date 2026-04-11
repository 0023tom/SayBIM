from flask import Flask, render_template, jsonify, request, send_from_directory, redirect, url_for, session, flash
from models import db, User, QuizResult, UserBadge
from flask_cors import CORS
import os
import random
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = 'super-secret-key-for-saybim' # In production, use a secure random key
CORS(app)

# Database Config
basedir = os.path.abspath(os.path.dirname(__file__))
# On Vercel, the root filesystem is read-only. We must use /tmp if we need SQLite temporarily, 
# although Firebase should be primary in production.
if os.environ.get('VERCEL') == '1':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/app.db'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
    
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Firebase Setup
from firebase_config import db_firestore
# For now, we use Firestore if it is initialized, else fallback to SQL
# This allows the app to still run while the user sets up Firebase
USE_FIREBASE = db_firestore is not None

from data_manager import DataManager, UserWrapper, USE_FIREBASE

# Helper to get or create default user
def get_current_user():
    if 'user_id' in session:
        return DataManager.get_user_by_id(session['user_id'])
    return None

def check_badges(user):
    # Simple Badge Logic
    # user is now a UserWrapper
    badges = []
    
    current_badges = DataManager.get_user_badges(user.id)

    # Level based badges
    if user.level >= 2 and 'Novice Signer' not in current_badges:
        DataManager.add_badge(user.id, 'Novice Signer')
        badges.append('Novice Signer')
        
    # Wealth based badges
    if user.diamonds >= 1000 and 'Gem Collector' not in current_badges:
        DataManager.add_badge(user.id, 'Gem Collector')
        badges.append('Gem Collector')

    return badges

@app.route('/')
def home():
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
    user.update_hearts()
    user.update_streak()
    db.session.commit()
    return render_template('index.html', user=user)

@app.route('/quiz/<int:lesson_id>')
def quiz_page(lesson_id):
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
    if user.hearts <= 0:
        flash("You are out of hearts. Wait for a refill or buy more to play!", "danger")
        return redirect(url_for('home'))
    return render_template('quiz_page.html', user=user, lesson_id=lesson_id)

@app.route('/practice')
def practice_page():
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
    return render_template('practice_page.html', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = DataManager.get_user_by_username(username)
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'danger')
            
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if DataManager.get_user_by_username(username):
            flash('Username already exists', 'danger')
        elif email and DataManager.get_user_by_email(email):
            flash('Email already registered', 'danger')
        else:
            from werkzeug.security import generate_password_hash
            user_data = {
                'username': username,
                'email': email,
                'password_hash': generate_password_hash(password),
                'xp': 0,
                'level': 1,
                'hearts': 5,
                'diamonds': 500,
                'streak': 0,
                'weekly_xp': 0,
                'created_at': datetime.utcnow()
            }
            
            if USE_FIREBASE:
                user_id = DataManager.save_user(user_data)
                session['user_id'] = user_id
            else:
                new_user = User(username=username, email=email)
                new_user.set_password(password)
                new_user.xp = 0
                new_user.level = 1
                new_user.hearts = 5
                new_user.diamonds = 500
                db.session.add(new_user)
                db.session.commit()
                session['user_id'] = new_user.id
            
            flash('Account created successfully!', 'success')
            return redirect(url_for('home'))
            
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

def check_and_reset_weekly_xp(user):
    now = datetime.utcnow()
    # Find most recent Monday at 00:00:00 UTC
    days_since_monday = now.weekday()
    most_recent_monday = (now - timedelta(days=days_since_monday)).replace(hour=0, minute=0, second=0, microsecond=0)
    
    # user is a UserWrapper
    last_reset = user.last_weekly_reset
    
    # Handle both Firestore timestamps (aware) and SQL/Strings (naive)
    if last_reset:
        if isinstance(last_reset, str):
            last_reset = datetime.fromisoformat(last_reset)
        # Ensure it is naive for comparison
        if last_reset.tzinfo is not None:
            last_reset = last_reset.replace(tzinfo=None)

    if not last_reset or last_reset < most_recent_monday:
        user.weekly_xp = 0
        user.last_weekly_reset = now
        user.commit() # Save changes
        return True
    return False

# === API ROUTES ===

@app.route('/api/user', methods=['GET'])
def get_user_stats():
    user = get_current_user()
    if not user: return jsonify({'error': 'Unauthorized'}), 401
    user.update_hearts()
    user.update_streak()
    user.commit()
    return jsonify({
        **user.to_dict(),
        'badges': DataManager.get_user_badges(user.id)
    })

@app.route('/api/leaderboard', methods=['GET'])
def get_leaderboard():
    # In Firebase mode, we might want to do a batch reset if performance is an issue,
    # but for 10 users it is fine to do it lazily.
    
    # Top 10 by weekly_xp
    raw_users = DataManager.get_all_users_sorted_by_weekly_xp()
    
    result = []
    for u in raw_users:
        wrapper = UserWrapper(u)
        check_and_reset_weekly_xp(wrapper)
        d = wrapper.to_dict()
        # Override the general xp field specifically for the leaderboard display
        d['xp'] = d.get('weekly_xp', 0)
        result.append(d)
        
    return jsonify(result)

@app.route('/api/quiz/<int:lesson_id>', methods=['GET'])
def get_quiz(lesson_id):
    if lesson_id == 2:
        POOL = [
            "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
            "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen",
            "eighteen", "nineteen", "twenty", "twenty_one", "twenty_two", "twenty_three",
            "thirty", "fourty", "hundred", "thousand", "million"
        ]
        HINTS = {
            "one": "Hold up your index finger.",
            "two": "Hold up your index and middle fingers.",
            "three": "Hold up your thumb, index, and middle fingers.",
            "four": "Hold up four fingers, excluding your thumb.",
            "five": "Hold up all five fingers with your hand open.",
            "six": "Touch your thumb to your pinky finger.",
            "seven": "Touch your thumb to your ring finger.",
            "eight": "Touch your thumb to your middle finger.",
            "nine": "Touch your thumb to your index finger.",
            "ten": "Give a thumbs up and shake it side to side.",
            "eleven": "Flick your index finger up twice.",
            "twelve": "Flick your index and middle fingers up twice.",
            "thirteen": "Wiggle your thumb, index, and middle fingers together.",
            "fourteen": "Tuck your thumb and fold your four fingers inward twice.",
            "fifteen": "Wave your open hand back twice.",
            "sixteen": "Twist your hand twice while signing six.",
            "seventeen": "Twist your hand twice while signing seven.",
            "eighteen": "Twist your hand twice while signing eight.",
            "nineteen": "Twist your hand twice while signing nine.",
            "twenty": "Tap your index finger and thumb together.",
            "twenty_one": "Point your finger like a gun and wiggle the thumb.",
            "twenty_two": "Sign two, then bounce your hand and sign two again.",
            "twenty_three": "Sign three, then wiggle your middle finger.",
            "thirty": "Sign three, then sign zero.",
            "fourty": "Sign four, then sign zero.",
            "hundred": "Sign the number, then pull your hand back into a 'C' shape.",
            "thousand": "Tap your fingertips against the flat palm of your other hand.",
            "million": "Tap your fingertips against your palm, then move slightly up and tap again."
        }
    else:
        POOL = [
            "How are you", "Peace be Upon You", "Hi, Hello", "Fine", "Excuse",
            "Sorry", "Salam", "Regards", "You Are Welcome", "Well",
            "Welcome", "Happy Birthday", "Good Bye", "Good Night", "Good Morning",
            "Good Afternoon", "Happy Anniversary", "Please (Welcome)", "Congratulations",
            "Thank You", "Please", "And unto you peace"
        ]
        
        HINTS = {
            "How are you": "Use both hands pointing forward, or sign 'How' and 'You'.",
            "Peace be Upon You": "Touch your chest and move hands outward, symbolizing offering peace.",
            "Hi, Hello": "A simple wave or salute gesture.",
            "Fine": "Tap your thumb on your chest with fingers spread.",
            "Excuse": "Wipe one hand over the other in a forward motion.",
            "Sorry": "Rub a fist in a circular motion over your chest.",
            "Salam": "A traditional gesture of greeting and respect.",
            "Regards": "Move your hands forward from your chest.",
            "You Are Welcome": "A sweeping motion with one hand, or simply the sign for 'welcome'.",
            "Well": "Sign 'Good' by moving your hand from chin to the other hand.",
            "Welcome": "Move your hand toward your body in a welcoming gesture.",
            "Happy Birthday": "Sign 'Happy' (brushing chest upwards) and 'Birthday' (middle finger from chin to chest).",
            "Good Bye": "A simple wave, opening and closing the hand.",
            "Good Night": "Sign 'Good' and then 'Night' by crossing hands downward.",
            "Good Morning": "Sign 'Good' and then bring one hand up like the sun rising.",
            "Good Afternoon": "Sign 'Good' and then bounce one hand down halfway.",
            "Happy Anniversary": "Sign 'Happy' and outline a circle for anniversary year.",
            "Please (Welcome)": "Rub your chest in a circular motion with an open hand.",
            "Congratulations": "Clasp your hands together and shake them slightly.",
            "Thank You": "Touch the fingers of one hand to your chin, then move the hand away from your body.",
            "Please": "Rub your palm in a circle on your chest.",
            "And unto you peace": "Return the gesture of peace pointing towards the person."
        }
    
    # Select 10 random questions (or fewer if pool is small)
    selected_items = random.sample(POOL, min(10, len(POOL)))
    questions = []
    
    for idx, correct_answer in enumerate(selected_items):
        # Create distractors
        distractors = random.sample([item for item in POOL if item != correct_answer], min(3, len(POOL)-1))
        options = distractors + [correct_answer]
        random.shuffle(options)
        
        media_url = None
        media_type = None
        
        # Search for any file in the specific lesson folder
        base_path = os.path.join(app.static_folder, 'quiz_media', f'lesson{lesson_id}')
        
        for ext in ['.mp4', '.jpg', '.jpeg', '.png']:
            filename = f"{correct_answer}{ext}"
            if os.path.exists(os.path.join(base_path, filename)):
                media_url = f"/static/quiz_media/lesson{lesson_id}/{filename}"
                media_type = 'video' if ext == '.mp4' else 'image'
                break
        
        questions.append({
            'id': idx + 1,
            'text': f'What is the sign for "{correct_answer}"?' if not media_url else "What does this sign mean?", 
            'target_sign': correct_answer, 
            'question_text': "What does this sign mean?",
            'options': options,
            'correct_option': correct_answer,
            'media_url': media_url,
            'media_type': media_type,
            'hint': HINTS.get(correct_answer, "Take your time and guess.")
        })
        
    return jsonify(questions)

@app.route('/api/quiz/submit', methods=['POST'])
def submit_quiz_result():
    data = request.json
    user = get_current_user()
    user.update_hearts()

    is_correct = data.get('correct', False)
    
    check_and_reset_weekly_xp(user)
    
    if is_correct:
        user.xp = (user.xp or 0) + 10 # 10 XP per correct answer
        user.weekly_xp = (user.weekly_xp or 0) + 10
    else:
        if (user.hearts or 0) >= 5:
            user.last_heart_update = datetime.utcnow()
        user.hearts = max(0, (user.hearts or 0) - 1)
    
    # Check level up (every 100 XP)
    new_level = 1 + ((user.xp or 0) // 100)
    if new_level > (user.level or 1):
        user.level = new_level
        user.diamonds = (user.diamonds or 0) + 50 # Level up bonus
    
    user.commit()
    new_badges = check_badges(user)
    
    return jsonify({
        **user.to_dict(),
        'new_badges': new_badges
    }) # Return updated stats

@app.route('/api/user/refill_hearts', methods=['POST'])
def refill_hearts():
    user = get_current_user()
    if not user: return jsonify({'error': 'Unauthorized'}), 401
    if (user.diamonds or 0) >= 100:
        user.diamonds = (user.diamonds or 0) - 100
        user.hearts = 5
        user.last_heart_update = None
        user.commit()
        return jsonify({'success': True, 'user': user.to_dict()})
    return jsonify({'success': False, 'message': 'Not enough diamonds'}), 400

@app.route('/api/practice/complete', methods=['POST'])
def complete_practice():
    data = request.json
    word = data.get('word')
    user = get_current_user()
    
    # Award for practice
    check_and_reset_weekly_xp(user)
    user.xp = (user.xp or 0) + 20
    user.weekly_xp = (user.weekly_xp or 0) + 20
    user.diamonds = (user.diamonds or 0) + 10
    
    user.commit()
    return jsonify({'success': True, 'user': user.to_dict(), 'message': f'Learned {word}!'})

@app.route('/api/lesson/complete', methods=['POST'])
def complete_lesson():
    user = get_current_user()
    user.add_streak_for_today()
    
    data = request.get_json(silent=True) or {}
    fully_completed = data.get('fully_completed', False)

    check_and_reset_weekly_xp(user)

    if fully_completed:
        user.xp = (user.xp or 0) + 200 # More XP
        user.weekly_xp = (user.weekly_xp or 0) + 200
        user.diamonds = (user.diamonds or 0) + 100 # More Diamonds
        message = "Lesson Fully Completed! +200 XP, +100 Diamonds"
    else:
        user.xp = (user.xp or 0) + 50
        user.weekly_xp = (user.weekly_xp or 0) + 50
        message = "Lesson Completed! +50 XP"
    
    new_level = 1 + ((user.xp or 0) // 100)
    if new_level > (user.level or 1):
        user.level = new_level
        user.diamonds = (user.diamonds or 0) + 50 # Level up bonus
        
    user.commit()
    new_badges = check_badges(user)
    
    return jsonify({
        'success': True,
        'message': message,
        'user': {
            **user.to_dict(),
            'badges': DataManager.get_user_badges(user.id)
        }
    })
@app.route('/api/user/profile', methods=['POST'])
def update_profile():
    user = get_current_user()
    if not user:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401

    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    avatar_file = request.files.get('avatar')

    alerts = []

    if username and username != user.username:
        if not DataManager.verify_username_uniqueness(username, exclude_user_id=user.id):
            return jsonify({'success': False, 'message': 'Username already taken'}), 400
        user.username = username
        alerts.append('Username updated')

    if email and email != user.email:
        if not DataManager.verify_email_uniqueness(email, exclude_user_id=user.id):
            return jsonify({'success': False, 'message': 'Email already exists'}), 400
        user.email = email
        alerts.append('Email updated')

    if password:
        user.set_password(password)
        alerts.append('Password updated')

    if avatar_file and avatar_file.filename != '':
        filename = secure_filename(f"user_{user.id}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{avatar_file.filename}")
        avatar_dir = os.path.join(app.static_folder, 'avatars')
        os.makedirs(avatar_dir, exist_ok=True)
        filepath = os.path.join(avatar_dir, filename)
        avatar_file.save(filepath)
        user.avatar = f"/static/avatars/{filename}"
        alerts.append('Avatar updated')

    user.commit()
    
    msg = ", ".join(alerts) if alerts else "No changes made."
    return jsonify({'success': True, 'message': msg, 'user': user.to_dict()})

@app.route('/api/user/account', methods=['DELETE'])
def delete_account():
    user = get_current_user()
    if not user:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    # Delete dependent data and user
    DataManager.delete_user_account(user.id)
    
    # Logout
    session.pop('user_id', None)
    
    return jsonify({'success': True, 'message': 'Account deleted successfully'})

# Initialize DB
with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        print(f"Warning: Could not create SQLite database (expected if using Firebase on Vercel): {e}")

if __name__ == '__main__':
    app.run(debug=True)
