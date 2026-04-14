from flask import Flask, render_template, jsonify, request, send_from_directory, redirect, url_for, session, flash
from models import db, User, QuizResult, UserBadge
from flask_cors import CORS
import os
import random
from datetime import datetime, timedelta
import json
from werkzeug.utils import secure_filename
import requests
from dotenv import load_dotenv

load_dotenv() # Load from .env file
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
from quiz_data import generate_topic_quiz

# Helper to get or create default user
import math

def calculate_level(xp):
    if xp < 100: return 1
    # Solves 25(L-1)(L+2) <= xp
    # L = (-1 + sqrt(9 + 0.16 * xp)) / 2
    level = math.floor((-1 + math.sqrt(9 + 0.16 * xp)) / 2)
    return min(100, max(1, level))

def get_xp_for_level(level):
    if level <= 1: return 0
    return 25 * (level - 1) * (level + 2)

@app.context_processor
def utility_processor():
    return dict(calculate_level=calculate_level, get_xp_for_level=get_xp_for_level)

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

@app.route('/topic/<int:topic_id>')
def topic_page(topic_id):
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
        
    try:
        progress_dict = json.loads(user.topic_progress or '{}')
    except:
        progress_dict = {}
        
    # Get highest unlocked lesson for this topic (defaults to 1)
    highest_unlocked = progress_dict.get(str(topic_id), 1)
    
    return render_template('topic_lessons.html', user=user, topic_id=topic_id, highest_unlocked=highest_unlocked)

@app.route('/quiz/<int:topic_id>/<int:lesson_id>')
def quiz_page(topic_id, lesson_id):
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
    if user.hearts <= 0:
        flash("You are out of hearts. Wait for a refill or buy more to play!", "danger")
        return redirect(url_for('topic_page', topic_id=topic_id))
    return render_template('quiz_page.html', user=user, topic_id=topic_id, lesson_id=lesson_id)

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

@app.route('/api/quiz/<int:topic_id>/<int:lesson_id>', methods=['GET'])
def get_quiz(topic_id, lesson_id):
    questions = generate_topic_quiz(topic_id, lesson_id)
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
    
    # Check level up (Scaling: +50 per level)
    new_level = calculate_level(user.xp or 0)
    if new_level > (user.level or 1):
        user.level = new_level
        user.diamonds = (user.diamonds or 0) + 100 # Increased bonus for harder levels
    
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

@app.route('/api/user/buy_time', methods=['POST'])
def buy_time():
    user = get_current_user()
    if not user: return jsonify({'error': 'Unauthorized'}), 401
    if (user.diamonds or 0) >= 100:
        user.diamonds = (user.diamonds or 0) - 100
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
    user.xp = (user.xp or 0) + 10
    user.weekly_xp = (user.weekly_xp or 0) + 10
    
    # Check level up
    new_level = calculate_level(user.xp or 0)
    if new_level > (user.level or 1):
        user.level = new_level
        user.diamonds = (user.diamonds or 0) + 100
    
    user.commit()
    return jsonify({'success': True, 'user': user.to_dict(), 'message': f'Learned {word}! +10 XP'})

@app.route('/api/lesson/complete', methods=['POST'])
def complete_lesson():
    user = get_current_user()
    user.add_streak_for_today()
    
    data = request.get_json(silent=True) or {}
    fully_completed = data.get('fully_completed', False)
    topic_id = str(data.get('topic_id', '1'))
    lesson_id = int(data.get('lesson_id', 0))

    check_and_reset_weekly_xp(user)

    if fully_completed:
        is_mastery = (topic_id == '1' and lesson_id == 8) or (topic_id == '2' and lesson_id == 9)
        
        if is_mastery:
            xp_reward = 200
            diamond_reward = 100
            message = f"Topic {topic_id} Complete! +200 XP, +100 Diamonds"
        else:
            xp_reward = 50
            diamond_reward = 25
            message = "Lesson Completed! +50 XP, +25 Diamonds"

        user.xp = (user.xp or 0) + xp_reward
        user.weekly_xp = (user.weekly_xp or 0) + xp_reward
        user.diamonds = (user.diamonds or 0) + diamond_reward
        
        # Update topic progress
        try:
            progress_dict = json.loads(user.topic_progress or '{}')
        except:
            progress_dict = {}
        
        current_highest = progress_dict.get(topic_id, 1)
        if lesson_id >= current_highest:
            progress_dict[topic_id] = lesson_id + 1
            user.topic_progress = json.dumps(progress_dict)
            
    else:
        user.xp = (user.xp or 0) + 50
        user.weekly_xp = (user.weekly_xp or 0) + 50
        message = "Lesson Completed! +50 XP"
    
    new_level = calculate_level(user.xp or 0)
    if new_level > (user.level or 1):
        user.level = new_level
        user.diamonds = (user.diamonds or 0) + 100 # Level up bonus
        
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

# --- Telegram Feedback Profile ---
# Pulled from .env file
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "").strip()

@app.route('/api/feedback', methods=['POST'])
def handle_feedback():
    user = get_current_user()
    data = request.json
    text = data.get('feedback', '')
    
    if not text:
        return jsonify({'success': False, 'message': 'No feedback provided'}), 400
        
    username = user.username if user else "Guest"
    email = user.email if user else "N/A"
    
    # Format message for Telegram
    message = f"🆕 *New Feedback from SayBIM*\n\n"
    message += f"👤 *User:* {username}\n"
    message += f"📧 *Email:* {email}\n"
    message += f"💬 *Message:* {text}\n"
    message += f"⏰ *Time:* {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    # Send to Telegram
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        }
        res = requests.post(url, json=payload, timeout=10)
        
        if res.status_code == 200:
            return jsonify({'success': True, 'message': 'Feedback sent to Telegram!'})
        else:
            print(f"Telegram API Error: {res.text}")
            return jsonify({'success': False, 'message': 'Could not reach Telegram API'}), 500
            
    except Exception as e:
        print(f"Feedback error: {e}")
        return jsonify({'success': False, 'message': 'Internal server error'}), 500

# Initialize DB
with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        print(f"Warning: Could not create SQLite database (expected if using Firebase on Vercel): {e}")

if __name__ == '__main__':
    app.run(debug=True)
