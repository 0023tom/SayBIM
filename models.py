from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta, date
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    avatar = db.Column(db.String(200), nullable=True)
    password_hash = db.Column(db.String(128))
    xp = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)
    hearts = db.Column(db.Integer, default=5)
    diamonds = db.Column(db.Integer, default=0)
    streak = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_heart_update = db.Column(db.DateTime, nullable=True)
    last_streak_date = db.Column(db.Date, nullable=True)
    weekly_xp = db.Column(db.Integer, default=0)
    last_weekly_reset = db.Column(db.DateTime, nullable=True)
    topic_progress = db.Column(db.String(500), default='{}')
    
    # Shop items
    shield_count = db.Column(db.Integer, default=0)
    timer_freeze_count = db.Column(db.Integer, default=0)
    xp_boost_expiry = db.Column(db.DateTime, nullable=True)

    def update_streak(self):
        today = date.today()
        if self.last_streak_date is not None:
            delta = today - self.last_streak_date
            if delta.days > 1:
                self.streak = 0

    def add_streak_for_today(self):
        self.update_streak()
        today = date.today()
        if self.last_streak_date != today:
            self.streak += 1
            self.last_streak_date = today

    def update_hearts(self):
        max_hearts = 5
        if self.hearts < max_hearts and self.last_heart_update:
            elapsed = datetime.utcnow() - self.last_heart_update
            hours_elapsed = elapsed.total_seconds() / 3600.0
            hearts_to_add = int(hours_elapsed // 6)
            
            if hearts_to_add > 0:
                self.hearts = min(max_hearts, self.hearts + hearts_to_add)
                if self.hearts == max_hearts:
                    self.last_heart_update = None
                else:
                    self.last_heart_update += timedelta(hours=6 * hearts_to_add)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Relationships
    quiz_results = db.relationship('QuizResult', backref='user', lazy=True)
    badges = db.relationship('UserBadge', backref='user', lazy=True)

    def to_dict(self):
        next_heart_in_seconds = 0
        if self.hearts < 5 and self.last_heart_update:
            elapsed = (datetime.utcnow() - self.last_heart_update).total_seconds()
            next_heart_in_seconds = max(0, (6 * 3600) - elapsed)

        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'avatar': self.avatar,
            'xp': self.xp,
            'weekly_xp': self.weekly_xp,
            'level': self.level,
            'hearts': self.hearts,
            'diamonds': self.diamonds,
            'streak': self.streak,
            'topic_progress': self.topic_progress,
            'next_heart_in_seconds': next_heart_in_seconds,
            'shield_count': self.shield_count,
            'timer_freeze_count': self.timer_freeze_count,
            'xp_boost_active': self.xp_boost_expiry > datetime.utcnow() if self.xp_boost_expiry else False,
            'xp_boost_expiry': (self.xp_boost_expiry.isoformat() + 'Z') if self.xp_boost_expiry else None
        }

class QuizResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)

class UserBadge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    badge_name = db.Column(db.String(100), nullable=False)
    awarded_at = db.Column(db.DateTime, default=datetime.utcnow)
