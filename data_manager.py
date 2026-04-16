from models import db, User, QuizResult, UserBadge
from firebase_config import db_firestore
from google.cloud.firestore_v1.base_query import FieldFilter
from datetime import datetime, date, timedelta
import os

# Check if we should use Firebase
USE_FIREBASE = db_firestore is not None

class UserWrapper:
    """Wraps either a SQLAlchemy User object or a Firestore dict to provide a common interface."""
    def __init__(self, data):
        self.data = data
        self.is_sql = hasattr(data, 'id')

    def __getattr__(self, name):
        if self.is_sql:
            return getattr(self.data, name)
        if name in self.data:
            return self.data[name]
            
        # Treat known database fields as None if they are missing in the Firestore document
        known_db_fields = {
            'id', 'username', 'email', 'avatar', 'password_hash',
            'xp', 'weekly_xp', 'level', 'hearts', 'diamonds', 'streak',
            'last_streak_date', 'last_heart_update', 'last_weekly_reset',
            'created_at', 'topic_progress',
            'shield_count', 'timer_freeze_count', 'xp_boost_expiry'
        }
        if name in known_db_fields:
            return None
            
        raise AttributeError(f"'UserWrapper' object has no attribute '{name}'")

    def __setattr__(self, name, value):
        if name in ['data', 'is_sql']:
            super().__setattr__(name, value)
        elif self.is_sql:
            setattr(self.data, name, value)
        else:
            self.data[name] = value

    def to_dict(self):
        if self.is_sql:
            return self.data.to_dict()
        
        # Firestore logic for next_heart_in_seconds
        next_heart_in_seconds = 0
        hearts = self.data.get('hearts', 5)
        last_heart_update = self.data.get('last_heart_update')
        
        if hearts < 5 and last_heart_update:
            # Ensure it is naive for comparison
            if last_heart_update.tzinfo is not None:
                last_heart_update = last_heart_update.replace(tzinfo=None)
            
            elapsed = (datetime.utcnow() - last_heart_update).total_seconds()
            next_heart_in_seconds = max(0, (6 * 3600) - elapsed)

        xp_boost_expiry = self.data.get('xp_boost_expiry')
        xp_boost_active = False
        if xp_boost_expiry:
            # Handle string from Firestore or SQLAlchemy
            if isinstance(xp_boost_expiry, str):
                xp_boost_expiry = datetime.fromisoformat(xp_boost_expiry)
            # Ensure it is naive for comparison (Firestore returns aware)
            if hasattr(xp_boost_expiry, 'tzinfo') and xp_boost_expiry.tzinfo is not None:
                xp_boost_expiry = xp_boost_expiry.replace(tzinfo=None)
            
            xp_boost_active = xp_boost_expiry > datetime.utcnow()

        return {
            'id': self.data.get('id'),
            'username': self.data.get('username'),
            'email': self.data.get('email'),
            'avatar': self.data.get('avatar'),
            'xp': self.data.get('xp', 0),
            'weekly_xp': self.data.get('weekly_xp', 0),
            'level': self.data.get('level', 1),
            'hearts': hearts,
            'diamonds': self.data.get('diamonds', 0),
            'streak': self.data.get('streak', 0),
            'topic_progress': self.data.get('topic_progress') or ('{}' if self.is_sql else {}),
            'next_heart_in_seconds': next_heart_in_seconds,
            'shield_count': self.data.get('shield_count', 0),
            'timer_freeze_count': self.data.get('timer_freeze_count', 0),
            'xp_boost_active': xp_boost_active,
            'xp_boost_expiry': (xp_boost_expiry.isoformat() + 'Z') if hasattr(xp_boost_expiry, 'isoformat') else xp_boost_expiry
        }

    def update_streak(self):
        today = date.today()
        last_streak_date = self.last_streak_date
        
        # Convert string/date from Firestore if needed
        if last_streak_date and isinstance(last_streak_date, str):
            last_streak_date = date.fromisoformat(last_streak_date)
        elif isinstance(last_streak_date, datetime):
            last_streak_date = last_streak_date.date()

        if last_streak_date is not None:
            delta = today - last_streak_date
            if delta.days > 1:
                self.streak = 0

    def add_streak_for_today(self):
        self.update_streak()
        today = date.today()
        last_streak_date = self.last_streak_date
        
        if last_streak_date and isinstance(last_streak_date, str):
            last_streak_date = date.fromisoformat(last_streak_date)
        elif isinstance(last_streak_date, datetime):
            last_streak_date = last_streak_date.date()

        if last_streak_date != today:
            self.streak = (self.streak or 0) + 1
            self.last_streak_date = datetime.combine(today, datetime.min.time()) if not self.is_sql else today

    def update_hearts(self):
        max_hearts = 5
        hearts = self.hearts or 0
        last_heart_update = self.last_heart_update

        if hearts < max_hearts and last_heart_update:
            # Ensure it is naive for comparison
            if last_heart_update.tzinfo is not None:
                last_heart_update = last_heart_update.replace(tzinfo=None)
                
            elapsed = datetime.utcnow() - last_heart_update
            hours_elapsed = elapsed.total_seconds() / 3600.0
            hearts_to_add = int(hours_elapsed // 6)
            
            if hearts_to_add > 0:
                self.hearts = min(max_hearts, hearts + hearts_to_add)
                if self.hearts == max_hearts:
                    self.last_heart_update = None
                else:
                    self.last_heart_update = last_heart_update + timedelta(hours=6 * hearts_to_add)

    def set_password(self, password):
        from werkzeug.security import generate_password_hash
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password_hash, password)

    def commit(self):
        """Save changes back to the database."""
        if self.is_sql:
            db.session.commit()
        else:
            DataManager.save_user(self.data)

class DataManager:
    @staticmethod
    def verify_username_uniqueness(username, exclude_user_id=None):
        if USE_FIREBASE:
            users_ref = db_firestore.collection('users')
            query = users_ref.where(filter=FieldFilter('username', '==', username)).stream()
            for doc in query:
                if exclude_user_id and doc.id == str(exclude_user_id):
                    continue
                return False
            return True
        else:
            user = User.query.filter_by(username=username).first()
            if user and (not exclude_user_id or user.id != exclude_user_id):
                return False
            return True

    @staticmethod
    def verify_email_uniqueness(email, exclude_user_id=None):
        if USE_FIREBASE:
            users_ref = db_firestore.collection('users')
            query = users_ref.where(filter=FieldFilter('email', '==', email)).stream()
            for doc in query:
                if exclude_user_id and doc.id == str(exclude_user_id):
                    continue
                return False
            return True
        else:
            user = User.query.filter_by(email=email).first()
            if user and (not exclude_user_id or user.id != exclude_user_id):
                return False
            return True

    @staticmethod
    def get_user_by_id(user_id):
        if USE_FIREBASE:
            doc = db_firestore.collection('users').document(str(user_id)).get()
            if doc.exists:
                return UserWrapper({**doc.to_dict(), 'id': doc.id})
            return None
        else:
            u = User.query.get(user_id)
            return UserWrapper(u) if u else None

    @staticmethod
    def get_user_by_username(username):
        if USE_FIREBASE:
            users_ref = db_firestore.collection('users')
            query = users_ref.where(filter=FieldFilter('username', '==', username)).limit(1).stream()
            for doc in query:
                return UserWrapper({**doc.to_dict(), 'id': doc.id})
            return None
        else:
            u = User.query.filter_by(username=username).first()
            return UserWrapper(u) if u else None


    @staticmethod
    def get_user_by_email(email):
        if USE_FIREBASE:
            users_ref = db_firestore.collection('users')
            query = users_ref.where(filter=FieldFilter('email', '==', email)).limit(1).stream()
            for doc in query:
                return UserWrapper({**doc.to_dict(), 'id': doc.id})
            return None
        else:
            u = User.query.filter_by(email=email).first()
            return UserWrapper(u) if u else None

    @staticmethod
    def save_user(user_data):
        if USE_FIREBASE:
            # If user_data is a dict from Firestore, it might have an 'id'
            user_id = user_data.get('id')
            if not user_id:
                # Create new
                doc_ref = db_firestore.collection('users').document()
                user_id = doc_ref.id
                user_data['id'] = user_id
            else:
                doc_ref = db_firestore.collection('users').document(user_id)
            
            doc_ref.set(user_data)
            return user_id
        else:
            # This logic will be stayed in app.py for now as it handles session.add/commit
            pass

    @staticmethod
    def get_all_users_sorted_by_weekly_xp():
        if USE_FIREBASE:
            users_ref = db_firestore.collection('users')
            # Firestore handles sorting
            query = users_ref.order_by('weekly_xp', direction='DESCENDING').limit(10).stream()
            return [{**doc.to_dict(), 'id': doc.id} for doc in query]
        else:
            return User.query.order_by(User.weekly_xp.desc()).limit(10).all()

    @staticmethod
    def add_quiz_result(user_id, score, total):
        if USE_FIREBASE:
            db_firestore.collection('quiz_results').add({
                'user_id': str(user_id),
                'score': score,
                'total_questions': total,
                'completed_at': datetime.utcnow()
            })
        else:
            res = QuizResult(user_id=user_id, score=score, total_questions=total)
            db.session.add(res)
            db.session.commit()

    @staticmethod
    def add_badge(user_id, badge_name):
        if USE_FIREBASE:
            db_firestore.collection('user_badges').add({
                'user_id': str(user_id),
                'badge_name': badge_name,
                'awarded_at': datetime.utcnow()
            })
        else:
            badge = UserBadge(user_id=user_id, badge_name=badge_name)
            db.session.add(badge)
            db.session.commit()

    @staticmethod
    def get_user_badges(user_id):
        if USE_FIREBASE:
            badges_ref = db_firestore.collection('user_badges')
            query = badges_ref.where(filter=FieldFilter('user_id', '==', str(user_id))).stream()
            return [doc.to_dict()['badge_name'] for doc in query]
        else:
            user = User.query.get(user_id)
            return [b.badge_name for b in user.badges] if user else []

    @staticmethod
    def delete_user_badges_by_prefix(user_id, prefix):
        if USE_FIREBASE:
            badges_ref = db_firestore.collection('user_badges')
            query = badges_ref.where(filter=FieldFilter('user_id', '==', str(user_id))).stream()
            for doc in query:
                badge_name = doc.to_dict().get('badge_name', '')
                if badge_name.startswith(prefix):
                    doc.reference.delete()
        else:
            UserBadge.query.filter(
                UserBadge.user_id == user_id,
                UserBadge.badge_name.like(f'{prefix}%')
            ).delete(synchronize_session=False)
            db.session.commit()

    @staticmethod
    def delete_user_badge_exact(user_id, badge_name):
        if USE_FIREBASE:
            badges_ref = db_firestore.collection('user_badges')
            query = badges_ref.where(filter=FieldFilter('user_id', '==', str(user_id))).stream()
            for doc in query:
                if doc.to_dict().get('badge_name') == badge_name:
                    doc.reference.delete()
        else:
            UserBadge.query.filter_by(user_id=user_id, badge_name=badge_name).delete(synchronize_session=False)
            db.session.commit()

    @staticmethod
    def delete_user_account(user_id):
        if USE_FIREBASE:
            user_id = str(user_id)
            # Delete badges
            badges = db_firestore.collection('user_badges').where(filter=FieldFilter('user_id', '==', user_id)).stream()
            for b in badges: b.reference.delete()
            
            # Delete quiz results
            results = db_firestore.collection('quiz_results').where(filter=FieldFilter('user_id', '==', user_id)).stream()
            for r in results: r.reference.delete()
            
            # Delete user
            db_firestore.collection('users').document(user_id).delete()
        else:
            # Logic in app.py
            pass
