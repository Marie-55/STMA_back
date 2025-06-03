from src.utils.db_factory import DatabaseFactory
from src.database import db
from datetime import datetime
from src.models.__init__ import FirebaseSession

class SessionController:
    def __init__(self):
        self.session_model = DatabaseFactory.get_session_model()
        self.task_model = DatabaseFactory.get_task_model()
        # day_schedule_model.add_session(schedule_date, session_id)
        self.day_schedule_model = DatabaseFactory.get_day_schedule_model()

    def create_session(self, title, date, start_time, user_id, task, duration=None):
        """Create a new session"""
        try:
            # Validate task exists if task_id provided
            if task:
                task_exists = self.task_model.get_by_id(str(task))
                if not task_exists:
                    raise ValueError("Task not found")

            # Ensure all values are properly typed
            session = self.session_model.create(
                title=str(title),
                duration=int(duration) if duration else 0,
                date=str(date),
                start_time=str(start_time),
                user_id=str(user_id),
                task_id=str(task) ,
            )
            try:
                self.day_schedule_model.add_session(date, int(session["id"]))
            except Exception as e:
                print(f"Error adding session to day schedule: {str(e)}")
                raise ValueError(f"Could not add session to day schedule: {str(e)}")
            

            return session
        except Exception as e:
            print(f"Error creating session: {str(e)}")
            raise ValueError(f"Could not create session: {str(e)}")

    def get_session_by_id(self, session_id):
        """Get session by ID"""
        if isinstance(self.session_model, FirebaseSession):
            return self.session_model.get_by_id(session_id)
        else:
            return self.session_model.query.get(session_id)

    def get_user_sessions(self, user_id):
        """Get all sessions for a user"""
        try:
            # Convert user_id to string for Firebase queries
            user_id = str(user_id)
            
            if isinstance(self.session_model, FirebaseSession):
                return self.session_model.get_by_user(user_id)
            else:
                return self.session_model.query.filter_by(user_id=user_id).all()
        except Exception as e:
            print(f"Error fetching user sessions: {str(e)}")
            raise

    def get_schedule_sessions(self, day_schedule_date):
        """Get all sessions for a specific day schedule"""
        if isinstance(self.session_model, FirebaseSession):
            return self.session_model.get_by_day_schedule(day_schedule_date)
        else:
            return self.session_model.query.filter_by(day_schedule_date=day_schedule_date).all()

    def update_session(self, session_id, data):
        """Update session data"""
        if isinstance(self.session_model, FirebaseSession):
            return self.session_model.update(session_id, data)
        else:
            session = self.session_model.query.get(session_id)
            if session:
                for key, value in data.items():
                    setattr(session, key, value)
                db.session.commit()
                return session
            return None

    def delete_session_from_day_schedule(self, session_id, day_schedule_date):
        """Delete session from a specific day schedule"""
        if isinstance(self.session_model, FirebaseSession):
            return self.session_model.remove_from_day_schedule(session_id, day_schedule_date)
        else:
            session = self.session_model.query.get(session_id)
            if session and session.day_schedule_date == day_schedule_date:
                session.day_schedule_date = None
                db.session.commit()
                return True
            return False


    def delete_session(self, session_id):
        """Delete session"""
        if isinstance(self.session_model, FirebaseSession):
            return self.session_model.delete(session_id)
        else:
            session = self.session_model.query.get(session_id)
            if session:
                db.session.delete(session)
                db.session.commit()
                return True
            return False

    def get_all_sessions(self):
        """Get all sessions"""
        if isinstance(self.session_model, FirebaseSession):
            return self.session_model.query_collection()
        else:
            return self.session_model.query.all()

    def get_task_id(self, session_id):
        """Get task ID associated with a session"""
        if isinstance(self.session_model, FirebaseSession):
            session = self.session_model.get_by_id(session_id)
            return session.get("task_id") if session else None
        else:
            session = self.session_model.query.get(session_id)
            return session.task_id if session else None
