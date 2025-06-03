from src.utils.db_factory import DatabaseFactory
from src.database import db
from datetime import datetime
from src.models.__init__ import FirebaseDaySchedule

class DayScheduleController:
    def __init__(self):
        self.day_schedule_model = DatabaseFactory.get_day_schedule_model()
        self.session_model = DatabaseFactory.get_session_model()

    def create_schedule(self, schedule_date, user_id=None, sessions=None):
        """Create new day schedule"""
        try:
            if isinstance(self.day_schedule_model, FirebaseDaySchedule):
                return self.day_schedule_model.create(
                    schedule_date=schedule_date,
                    sessions=sessions or [],
                    user_id=user_id
                )
            else:
                schedule = self.day_schedule_model(
                    date=schedule_date,
                    user_id=user_id
                )
                db.session.add(schedule)
                db.session.commit()
                return schedule
        except Exception as e:
            raise ValueError(f"Could not create day schedule: {str(e)}")

    def get_by_date(self, schedule_date):
        """Get schedule by date"""
        if isinstance(self.day_schedule_model, FirebaseDaySchedule):
            return self.day_schedule_model.get_by_date(schedule_date)
        else:
            return self.day_schedule_model.query.get(schedule_date)

    def add_session(self, schedule_date, session_id):
        """Add session to schedule"""
        if isinstance(self.day_schedule_model, FirebaseDaySchedule):
            return self.day_schedule_model.add_session(schedule_date, session_id)
        else:
            schedule = self.get_by_date(schedule_date)
            if schedule:
                session = self.session_model.query.get(session_id)
                if session:
                    session.day_schedule_date = schedule_date
                    db.session.commit()
                    return schedule
            return None

    def remove_session(self, schedule_date, session_id):
        """Remove session from schedule"""
        if isinstance(self.day_schedule_model, FirebaseDaySchedule):
            return self.day_schedule_model.remove_session(schedule_date, session_id)
        else:
            schedule = self.get_by_date(schedule_date)
            if schedule:
                session = self.session_model.query.get(session_id)
                if session and session.day_schedule_date == schedule_date:
                    session.day_schedule_date = None
                    db.session.commit()
                    return schedule
            return None

    def get_sessions(self, schedule_date):
        """Get all sessions for a specific date"""
        if isinstance(self.day_schedule_model, FirebaseDaySchedule):
            schedule = self.day_schedule_model.get_by_date(schedule_date)
            if schedule and 'sessions' in schedule:
                return [
                    self.session_model.get_by_id(sid) 
                    for sid in schedule['sessions']
                ]
        else:
            return self.session_model.query.filter_by(
                day_schedule_date=schedule_date
            ).all()
        return []

    def delete_schedule(self, schedule_date):
        """Delete day schedule"""
        if isinstance(self.day_schedule_model, FirebaseDaySchedule):
            return self.day_schedule_model.delete(schedule_date)
        else:
            schedule = self.day_schedule_model.query.get(schedule_date)
            if schedule:
                db.session.delete(schedule)
                db.session.commit()
                return True
            return False