from flask import Flask, render_template, jsonify, request, send_from_directory, redirect, url_for, session, flash
from models import db, User, QuizResult, UserBadge
from flask_cors import CORS
import os
import random
from datetime import datetime, timedelta, date
import json
from werkzeug.utils import secure_filename
import requests
from dotenv import load_dotenv

load_dotenv() # Load from .env file
app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = os.environ.get('SECRET_KEY', 'default-key-for-dev')
CORS(app)

# Database Config
basedir = os.path.abspath(os.path.dirname(__file__))
# On Vercel, the root filesystem is read-only. Must use /tmp if need SQLite temporarily, 
# although Firebase should be primary in production.
if os.environ.get('VERCEL') == '1':
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/app.db'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
    
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Firebase Setup
from firebase_config import db_firestore
# Use Firestore if it is initialized, else fallback to SQL
# This allows the app to still run while the user sets up Firebase
USE_FIREBASE = db_firestore is not None

from data_manager import DataManager, UserWrapper, USE_FIREBASE
from quiz_data import generate_topic_quiz

# Helper to get or create default user
import math

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.png', mimetype='image/png')

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

BADGE_DEFS = {
    'first_practice_camera': {'label': 'First Camera Practice (1x)', 'emoji': '📷', 'weekly': False},
    'topic_1_complete': {'label': 'Topic 1 Master (Lessons 1-8)', 'emoji': '📘', 'weekly': False},
    'topic_2_complete': {'label': 'Topic 2 Master (Lessons 1-9)', 'emoji': '📙', 'weekly': False},
    'weekly_top_1': {'label': 'Weekly Top 1', 'emoji': '🥇', 'weekly': True},
    'weekly_top_2': {'label': 'Weekly Top 2', 'emoji': '🥈', 'weekly': True},
    'weekly_top_3': {'label': 'Weekly Top 3', 'emoji': '🥉', 'weekly': True},
}

def get_week_start(dt=None):
    now = dt or datetime.utcnow()
    return (now - timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)

def get_next_weekly_reset(dt=None):
    return get_week_start(dt) + timedelta(days=7)

def _badge_record_for_key(key, week_start=None):
    if BADGE_DEFS.get(key, {}).get('weekly'):
        week_id = (week_start or get_week_start()).date().isoformat()
        return f'badge::{key}::{week_id}'
    return f'badge::{key}'

def _parse_badge_inventory(raw_badges):
    now = datetime.utcnow()
    owned = {}
    equipped_key = None
    equipped_raw = None

    for raw in raw_badges:
        if raw.startswith('equipped::'):
            equipped_key = raw.split('::', 1)[1]
            equipped_raw = raw
            continue

        if not raw.startswith('badge::'):
            continue

        parts = raw.split('::')
        if len(parts) < 2:
            continue
        key = parts[1]
        if key not in BADGE_DEFS:
            continue

        meta = BADGE_DEFS[key]
        expires_at = None
        is_active = True

        if meta.get('weekly'):
            if len(parts) < 3:
                continue
            try:
                week_start = datetime.fromisoformat(parts[2])
                expires_at = week_start + timedelta(days=7)
                is_active = now < expires_at
            except ValueError:
                is_active = False

        if not is_active:
            continue

        owned[key] = {
            'key': key,
            'name': meta['label'],
            'emoji': meta['emoji'],
            'is_weekly': meta['weekly'],
            'expires_at': (expires_at.isoformat() + 'Z') if expires_at else None
        }

    if equipped_key and equipped_key not in owned and equipped_raw:
        return list(owned.values()), None, equipped_raw
    return list(owned.values()), owned.get(equipped_key), None

def get_user_badge_payload(user_id):
    raw = DataManager.get_user_badges(user_id)
    owned, equipped, stale_equipped = _parse_badge_inventory(raw)
    if stale_equipped:
        DataManager.delete_user_badge_exact(user_id, stale_equipped)
    return {'owned': owned, 'equipped': equipped}

def award_badge_if_missing(user_id, key, week_start=None):
    if key not in BADGE_DEFS:
        return False
    raw = DataManager.get_user_badges(user_id)
    record = _badge_record_for_key(key, week_start=week_start)
    if record in raw:
        return False
    DataManager.add_badge(user_id, record)
    return True

def set_equipped_badge(user_id, badge_key):
    DataManager.delete_user_badges_by_prefix(user_id, 'equipped::')
    if badge_key:
        DataManager.add_badge(user_id, f'equipped::{badge_key}')

def check_and_finalize_weekly_leaderboard():
    """
    Checks if the previous week stand-ins have been finalized and awarded.
    Should be called regularly (e.g., during leaderboard or user fetch).
    """
    now = datetime.utcnow()
    current_week_start = get_week_start(now)
    prev_week_start = current_week_start - timedelta(days=7)
    prev_week_id = prev_week_start.date().isoformat()
    
    # Check if Top 1 for previous week has been awarded to ANYONE yet
    # This acts as our "finalization" flag for the system
    finalization_flag = f'system::finalized_week::{prev_week_id}'
    
    # We use a special "System" badge check. 
    # To keep it simple without adding models, we'll check if any user has this system badge.
    # Actually, better to check if Top 1 was awarded.
    # But what if Top 1 hasn't logged in? 
    # Let's use a "System" record. We award it to User ID 1 or a dummy?
    # Better: check DataManager for existence of ANY badge with that suffix.
    
    # Re-reading app.py... I'll check the Top 1 badge.
    top_1_key = f'badge::weekly_top_1::{prev_week_id}'
    
    # We need a global way to check if this was done. 
    # For now, let's look at the leaderboard Standings when a reset is due.
    pass

def award_weekly_rank_badges(raw_users, week_start=None):
    if not week_start:
        week_start = get_week_start()
    top_keys = ['weekly_top_1', 'weekly_top_2', 'weekly_top_3']
    newly_earned = []
    for rank, user_item in enumerate(raw_users[:3], start=1):
        weekly_xp = user_item.weekly_xp if hasattr(user_item, 'weekly_xp') else user_item.get('weekly_xp', 0)
        if (weekly_xp or 0) <= 0:
            continue
        user_id = user_item.id if hasattr(user_item, 'id') else user_item.get('id')
        if user_id is None:
            continue
        if award_badge_if_missing(user_id, top_keys[rank - 1], week_start=week_start):
            newly_earned.append(top_keys[rank - 1])
    return newly_earned

def get_progress_dict(user):
    tp = user.topic_progress
    if not tp:
        return {}
    if isinstance(tp, dict):
        return tp
    try:
        return json.loads(tp)
    except (ValueError, TypeError):
        return {}

def check_badges(user):
    earned = []
    progress_dict = get_progress_dict(user)

    if progress_dict.get('1', 1) > 8 and award_badge_if_missing(user.id, 'topic_1_complete'):
        earned.append(BADGE_DEFS['topic_1_complete']['label'])

    if progress_dict.get('2', 1) > 9 and award_badge_if_missing(user.id, 'topic_2_complete'):
        earned.append(BADGE_DEFS['topic_2_complete']['label'])

    return earned

@app.route('/')
def home():
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
    user.update_hearts()
    user.update_streak()
    user.commit()
    return render_template('index.html', user=user)

@app.route('/topic/<int:topic_id>')
def topic_page(topic_id):
    user = get_current_user()
    if not user:
        return redirect(url_for('login'))
        
    # Initialize progress if needed
    progress_dict = get_progress_dict(user)
    
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

    new_badges = []
    if not last_reset or last_reset < most_recent_monday:
        # WEEKLY FINALIZATION: 
        # Before resetting, if this user is potentially a winner, 
        # we trigger a global check/award for the week that just ended.
        raw_users = DataManager.get_all_users_sorted_by_weekly_xp()
        # Award badges for the week that just ended (last_reset's week)
        all_newly_earned = award_weekly_rank_badges(raw_users, week_start=last_reset or (most_recent_monday - timedelta(days=7)))
        
        # Check if OUR user was in the newly earned list
        # Map labels to keys for consistency with what check_badges returns
        for badge_key in all_newly_earned:
            # We want to know if THIS user earned it.
            # award_weekly_rank_badges awards it to the user_id in the list.
            # We check the leaderboard again or trust award_weekly_rank_badges?
            # Actually, award_weekly_rank_badges already did the work. 
            # Let's check if the top user matches our user.
            pass
            
        # Refined: just check which badges the user HAS now that match the prev week id.
        prev_week_start = last_reset or (most_recent_monday - timedelta(days=7))
        # Find which of the top 1-3 were awarded specifically to THIS user for THAT week
        top_keys = ['weekly_top_1', 'weekly_top_2', 'weekly_top_3']
        for bk in top_keys:
            full_record = f'badge::{bk}::{prev_week_start.date().isoformat()}'
            owned = DataManager.get_user_badges(user.id)
            if full_record in owned:
                new_badges.append(bk) # Add key for celebration

        user.weekly_xp = 0
        user.last_weekly_reset = now
        user.commit() # Save changes
        return new_badges
    return []

# === API ROUTES ===

@app.route('/api/user', methods=['GET'])
def get_user_stats():
    user = get_current_user()
    if not user: return jsonify({'error': 'Unauthorized'}), 401
    user.update_hearts()
    user.update_streak()
    
    # Check for weekly reset and badges
    weekly_badges = check_and_reset_weekly_xp(user)
    
    user.commit()
    badge_payload = get_user_badge_payload(user.id)
    return jsonify({
        **user.to_dict(),
        'badges': badge_payload['owned'],
        'equipped_badge': badge_payload['equipped'],
        'new_badges': weekly_badges # Frontend will celebrate these!
    })

@app.route('/api/leaderboard', methods=['GET'])
def get_leaderboard():
    # In Firebase mode, do a batch reset if performance is an issue,
    # but for 10 users only?
    
    # Top 10 by weekly_xp
    raw_users = DataManager.get_all_users_sorted_by_weekly_xp()
    
    result = []
    for u in raw_users:
        wrapper = UserWrapper(u)
        check_and_reset_weekly_xp(wrapper)
        d = wrapper.to_dict()
        # Override the general xp field specifically for the leaderboard display
        d['xp'] = d.get('weekly_xp', 0)
        d['equipped_badge'] = get_user_badge_payload(d['id']).get('equipped')
        result.append(d)
        
    return jsonify(result)

@app.route('/api/badges/equip', methods=['POST'])
def equip_badge():
    user = get_current_user()
    if not user:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 401

    data = request.get_json(silent=True) or {}
    badge_key = (data.get('badge_key') or '').strip()
    if badge_key == '':
        set_equipped_badge(user.id, None)
        payload = get_user_badge_payload(user.id)
        return jsonify({'success': True, 'equipped_badge': payload.get('equipped')})

    payload = get_user_badge_payload(user.id)
    owned_keys = {b['key'] for b in payload.get('owned', [])}
    if badge_key not in owned_keys:
        return jsonify({'success': False, 'message': 'Badge not owned or expired'}), 400

    set_equipped_badge(user.id, badge_key)
    payload = get_user_badge_payload(user.id)
    return jsonify({'success': True, 'equipped_badge': payload.get('equipped')})

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
    
    xp_gain = 0
    if is_correct:
        xp_gain = 10
        # Check for 2x XP boost
        if user.xp_boost_expiry:
            expiry = user.xp_boost_expiry
            if isinstance(expiry, str): expiry = datetime.fromisoformat(expiry)
            if expiry.tzinfo: expiry = expiry.replace(tzinfo=None)
            if expiry > datetime.utcnow():
                xp_gain *= 2

        user.xp = (user.xp or 0) + xp_gain
        user.weekly_xp = (user.weekly_xp or 0) + xp_gain
    else:
        # Check for Shield (Second Chance)
        if (user.shield_count or 0) > 0:
            user.shield_count -= 1
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
    
    # Also collect any weekly badges from reset
    weekly_badges = check_and_reset_weekly_xp(user)
    new_badges.extend(weekly_badges)
    
    badge_payload = get_user_badge_payload(user.id)
    
    message = f'Correct! +{xp_gain} XP' if is_correct else 'Not quite! Try again.'
    
    return jsonify({
        'success': True,
        'message': message,
        'xp_gain': xp_gain,
        'new_badges': new_badges,
        'user': {
            **user.to_dict(),
            'badges': badge_payload['owned'],
            'equipped_badge': badge_payload['equipped']
        }
    })
 # Return updated stats

@app.route('/api/user/refill_hearts', methods=['POST'])
def refill_hearts():
    user = get_current_user()
    if not user: return jsonify({'error': 'Unauthorized'}), 401
    if (user.diamonds or 0) >= 150:
        user.diamonds = (user.diamonds or 0) - 150
        user.hearts = 5
        user.last_heart_update = None
        user.commit()
        return jsonify({'success': True, 'user': user.to_dict()})
    return jsonify({'success': False, 'message': 'Not enough diamonds'}), 400

@app.route('/api/shop/purchase', methods=['POST'])
def purchase_item():
    user = get_current_user()
    if not user: return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    
    data = request.json
    item_id = data.get('item_id')
    
    shop_items = {
        'heart_refill': {'name': 'Heart Refill', 'cost': 150},
        'timer_freeze': {'name': 'Timer Freeze', 'cost': 80},
        'shield': {'name': 'Second Chance (Shield)', 'cost': 100},
        'xp_card': {'name': '2x XP Card', 'cost': 300},
        'streak_repair': {'name': 'Streak Repair', 'cost': 500}
    }
    
    if item_id not in shop_items:
        return jsonify({'success': False, 'message': 'Invalid item'}), 400
        
    item = shop_items[item_id]
    if (user.diamonds or 0) < item['cost']:
        return jsonify({'success': False, 'message': 'Not enough diamonds'}), 400
        
    user.diamonds -= item['cost']
    
    if item_id == 'heart_refill':
        user.hearts = 5
        user.last_heart_update = None
    elif item_id == 'timer_freeze':
        user.timer_freeze_count = (user.timer_freeze_count or 0) + 1
    elif item_id == 'shield':
        user.shield_count = (user.shield_count or 0) + 1
    elif item_id == 'xp_card':
        now = datetime.utcnow()
        current_expiry = user.xp_boost_expiry
        if current_expiry:
            if isinstance(current_expiry, str): current_expiry = datetime.fromisoformat(current_expiry)
            if current_expiry.tzinfo: current_expiry = current_expiry.replace(tzinfo=None)
            base = max(now, current_expiry)
        else:
            base = now
        user.xp_boost_expiry = base + timedelta(minutes=30)
    elif item_id == 'streak_repair':
        # Logic: If streak was lost (0), restore it to 1 and set last_streak_date to yesterday
        # Or even better: if they missed a day, just set last_streak_date to yesterday
        today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        yesterday = today - timedelta(days=1)
        if user.streak == 0:
            user.streak = 1 # Give them a fresh start at 1 if they were at 0
        user.last_streak_date = yesterday
        
    user.commit()
    return jsonify({
        'success': True, 
        'message': f'Purchased {item["name"]}!', 
        'user': user.to_dict()
    })

@app.route('/api/shop/use_timer_freeze', methods=['POST'])
def use_timer_freeze():
    user = get_current_user()
    if not user: return jsonify({'success': False, 'message': 'Unauthorized'}), 401
    if (user.timer_freeze_count or 0) > 0:
        user.timer_freeze_count -= 1
        user.commit()
        return jsonify({'success': True, 'message': 'Timer Freeze activated!'})
    return jsonify({'success': False, 'message': 'No Timer Freezes available'}), 400

@app.route('/api/practice/complete', methods=['POST'])
def complete_practice():
    data = request.json
    word = data.get('word')
    user = get_current_user()
    
    # Award for practice
    check_and_reset_weekly_xp(user)
    xp_reward = 10
    
    # Check for 2x XP boost
    if user.xp_boost_expiry:
        expiry = user.xp_boost_expiry
        if isinstance(expiry, str): expiry = datetime.fromisoformat(expiry)
        if expiry.tzinfo: expiry = expiry.replace(tzinfo=None)
        if expiry > datetime.utcnow():
            xp_reward *= 2
            
    user.xp = (user.xp or 0) + xp_reward
    user.weekly_xp = (user.weekly_xp or 0) + xp_reward
    
    # Check level up
    new_level = calculate_level(user.xp or 0)
    if new_level > (user.level or 1):
        user.level = new_level
        user.diamonds = (user.diamonds or 0) + 100
    
    user.commit()
    new_badges = []
    if award_badge_if_missing(user.id, 'first_practice_camera'):
        new_badges.append(BADGE_DEFS['first_practice_camera']['label'])
        
    # Also include weekly reset badges if it's Monday!
    weekly_badges = check_and_reset_weekly_xp(user)
    new_badges.extend(weekly_badges)
    
    check_badges(user)
    badge_payload = get_user_badge_payload(user.id)
    return jsonify({
        'success': True,
        'user': {**user.to_dict(), 'badges': badge_payload['owned'], 'equipped_badge': badge_payload['equipped']},
        'message': f'Learned {word}! +{xp_reward} XP',
        'new_badges': new_badges
    })

@app.route('/api/lesson/complete', methods=['POST'])
def complete_lesson():
    user = get_current_user()
    user.add_streak_for_today()
    
    data = request.get_json(silent=True) or {}
    fully_completed = data.get('fully_completed', False)
    topic_id = str(data.get('topic_id', '1'))
    lesson_id = int(data.get('lesson_id', 0))
    xp_reward = 0
    message = 'Progress saved.'

    check_and_reset_weekly_xp(user)

    if fully_completed:
        is_mastery = (topic_id == '1' and lesson_id == 8) or (topic_id == '2' and lesson_id == 9)
        if is_mastery:
            xp_reward = 200
            diamond_reward = 100
            base_msg = f"Topic {topic_id} Complete!"
        else:
            xp_reward = 50
            diamond_reward = 25
            base_msg = "Lesson Completed!"

        # Check for 2x XP boost
        if user.xp_boost_expiry:
            expiry = user.xp_boost_expiry
            if isinstance(expiry, str): expiry = datetime.fromisoformat(expiry)
            if expiry.tzinfo: expiry = expiry.replace(tzinfo=None)
            if expiry > datetime.utcnow():
                xp_reward *= 2

        user.xp = (user.xp or 0) + xp_reward
        user.weekly_xp = (user.weekly_xp or 0) + xp_reward
        user.diamonds = (user.diamonds or 0) + diamond_reward
        
        message = f"{base_msg} +{xp_reward} XP, +{diamond_reward} Diamonds"
        
        # Update topic progress
        progress_dict = get_progress_dict(user)
        
        current_highest = progress_dict.get(topic_id, 1)
        if lesson_id >= current_highest:
            progress_dict[topic_id] = lesson_id + 1
            # If using Firestore, we store the dict directly
            # If SQL, we store the JSON string. UserWrapper handles this in __setattr__.
            if not user.is_sql:
                user.topic_progress = progress_dict
            else:
                user.topic_progress = json.dumps(progress_dict)
    
    new_level = calculate_level(user.xp or 0)
    if new_level > (user.level or 1):
        user.level = new_level
        user.diamonds = (user.diamonds or 0) + 100 # Level up bonus
        
    user.commit()
    new_badges = check_badges(user)
    
    # Add weekly reset badges
    weekly_badges = check_and_reset_weekly_xp(user)
    new_badges.extend(weekly_badges)
    
    badge_payload = get_user_badge_payload(user.id)
    
    return jsonify({
        'success': True,
        'message': message,
        'reward_xp': xp_reward,
        'new_badges': new_badges,
        'user': {
            **user.to_dict(),
            'badges': badge_payload['owned'],
            'equipped_badge': badge_payload['equipped']
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
