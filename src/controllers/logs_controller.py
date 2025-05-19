from src.utils.db_factory import DatabaseFactory
from src.database import db
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from src.models import FirebaseLogs

class LogsController:
    def __init__(self):
        self.logs_model = DatabaseFactory.get_logs_model()

    def create_log(self, user_id, login_time=None):
        """Create new log entry"""
        try:
            if isinstance(self.logs_model, FirebaseLogs):
                return self.logs_model.create(
                    user_id=user_id,
                    login_time=login_time or datetime.now().strftime("%H:%M:%S"),
                    date=datetime.now()
                )
            else:
                log = self.logs_model(
                    date=datetime.now().strftime("%Y-%m-%d"),
                    user_id=user_id,
                    login_time=login_time or datetime.now().strftime("%H:%M:%S"),
                    logout_time=None
                )
                db.session.add(log)
                db.session.commit()
                return log
        except Exception as e:
            if not isinstance(self.logs_model, FirebaseLogs):
                db.session.rollback()
            raise ValueError(f"Could not create log: {str(e)}")

    def update_logout(self, date, logout_time=None):
        """Update logout time for a specific date"""
        try:
            logout_time = logout_time or datetime.now().strftime("%H:%M:%S")
            if isinstance(self.logs_model, FirebaseLogs):
                return self.logs_model.update_logout(date, logout_time)
            else:
                log = self.logs_model.query.get(date)
                if log:
                    log.logout_time = logout_time
                    db.session.commit()
                    return log
                return None
        except Exception as e:
            if not isinstance(self.logs_model, FirebaseLogs):
                db.session.rollback()
            raise ValueError(f"Could not update logout time: {str(e)}")

    def increment_tasks(self, date):
        """Increment completed tasks counter"""
        try:
            if isinstance(self.logs_model, FirebaseLogs):
                return self.logs_model.increment_tasks(date)
            else:
                log = self.logs_model.query.get(date)
                if log:
                    log.tasks_completed += 1
                    db.session.commit()
                    return log
                return None
        except Exception as e:
            if not isinstance(self.logs_model, FirebaseLogs):
                db.session.rollback()
            raise ValueError(f"Could not increment tasks: {str(e)}")

    def get_by_date(self, date):
        """Get log by date"""
        try:
            if isinstance(self.logs_model, FirebaseLogs):
                return self.logs_model.get_by_date(date)
            else:
                return self.logs_model.query.get(date)
        except Exception as e:
            raise ValueError(f"Could not get log: {str(e)}")

    def get_by_user(self, user_id):
        """Get all logs for a user"""
        try:
            if isinstance(self.logs_model, FirebaseLogs):
                return self.logs_model.get_by_user(user_id)
            else:
                return self.logs_model.query.filter_by(
                    user_id=user_id
                ).order_by(self.logs_model.date.desc()).all()
        except Exception as e:
            raise ValueError(f"Could not get user logs: {str(e)}")

    def get_by_date_range(self, user_id, start_date, end_date):
        """Get logs within a date range"""
        try:
            if isinstance(self.logs_model, FirebaseLogs):
                return self.logs_model.get_by_date_range(
                    user_id, start_date, end_date
                )
            else:
                return self.logs_model.query.filter(
                    self.logs_model.user_id == user_id,
                    self.logs_model.date >= start_date,
                    self.logs_model.date <= end_date
                ).order_by(self.logs_model.date.desc()).all()
        except Exception as e:
            raise ValueError(f"Could not get logs by date range: {str(e)}")