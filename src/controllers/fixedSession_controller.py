from src.utils.db_factory import DatabaseFactory
from src.database import db
from datetime import datetime
from src.models.__init__ import FirebaseFixedSession

class FixedSessionController:
    def __init__(self):
        self.fixed_session_model = DatabaseFactory.get_fixed_session_model()

    def create_fixed_session(self, title, day_index, duration, start_time, user_id):
        """Create a new fixed session"""
        try:
            if isinstance(self.fixed_session_model, FirebaseFixedSession):
                return self.fixed_session_model.create(
                    title=title,
                    day_index=day_index,
                    duration=float(duration),
                    start_time=start_time,
                    user_id=user_id
                )
            else:
                fixed_session = self.fixed_session_model(
                    title=title,
                    day_index=day_index,
                    duration=float(duration),
                    start_time=start_time,
                    user_id=user_id
                )
                db.session.add(fixed_session)
                db.session.commit()
                return fixed_session
        except Exception as e:
            raise ValueError(f"Could not create fixed session: {str(e)}")

    def get_fixed_session_by_id(self, session_id):
        """Get fixed session by ID"""
        if isinstance(self.fixed_session_model, FirebaseFixedSession):
            return self.fixed_session_model.get_by_id(session_id)
        else:
            return self.fixed_session_model.query.get(session_id)

    def get_user_fixed_sessions(self, user_id):
        """Get all fixed sessions for a user"""
        if isinstance(self.fixed_session_model, FirebaseFixedSession):
            return self.fixed_session_model.get_by_user(user_id)
        else:
            return self.fixed_session_model.query.filter_by(user_id=user_id).all()

    def get_day_fixed_sessions(self, user_id, day_index):
        """Get fixed sessions for a specific day"""
        if isinstance(self.fixed_session_model, FirebaseFixedSession):
            return self.fixed_session_model.get_by_day(user_id, day_index)
        else:
            return self.fixed_session_model.query.filter_by(
                user_id=user_id,
                day_index=day_index
            ).all()

    def update_fixed_session(self, session_id, data):
        """Update fixed session data"""
        if isinstance(self.fixed_session_model, FirebaseFixedSession):
            return self.fixed_session_model.update(session_id, data)
        else:
            session = self.fixed_session_model.query.get(session_id)
            if session:
                for key, value in data.items():
                    if key == 'duration':
                        value = float(value)
                    setattr(session, key, value)
                db.session.commit()
                return session
            return None

    def delete_fixed_session(self, session_id):
        """Delete fixed session"""
        if isinstance(self.fixed_session_model, FirebaseFixedSession):
            return self.fixed_session_model.delete(session_id)
        else:
            session = self.fixed_session_model.query.get(session_id)
            if session:
                db.session.delete(session)
                db.session.commit()
                return True
            return False

    def get_week_schedule(self, user_id):
        """Get all fixed sessions organized by day for the week"""
        week_schedule = {i: [] for i in range(7)}  # 0-6 for Monday-Sunday
        
        if isinstance(self.fixed_session_model, FirebaseFixedSession):
            sessions = self.fixed_session_model.get_by_user(user_id)
            for session in sessions:
                day_index = session['day_index']
                week_schedule[day_index].append(session)
        else:
            sessions = self.fixed_session_model.query.filter_by(user_id=user_id).all()
            for session in sessions:
                week_schedule[session.day_index].append(session)
        
        return week_schedule