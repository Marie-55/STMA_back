# src/utils/db_factory.py
from src.utils.db_utils import get_active_db_type
from src.models.__init__ import User, Task, Stats, Logs, Session, DaySchedule, FixedSession, Stats, Logs
from src.models.__init__ import FirebaseUser, FirebaseTask, FirebaseStats, FirebaseLogs, FirebaseSession, FirebaseDaySchedule, FirebaseFixedSession


class DatabaseFactory:
    @staticmethod
    def get_user_model():
        db_type = get_active_db_type()
        if db_type == "firebase":
            return FirebaseUser()
        # Default to SQLAlchemy User model
        return User

    @staticmethod
    def get_task_model():
        db_type = get_active_db_type()
        if db_type == "firebase":
            return FirebaseTask()
        return Task

    @staticmethod
    def get_stats_model():
        db_type = get_active_db_type()
        if db_type == "firebase":
            return FirebaseStats()
        return Stats

    @staticmethod
    def get_logs_model():
        db_type = get_active_db_type()
        if db_type == "firebase":
            return FirebaseLogs()
        return Logs

    @staticmethod
    def get_session_model():
        db_type = get_active_db_type()
        if db_type == "firebase":
            return FirebaseSession()
        return Session

    @staticmethod
    def get_day_schedule_model():
        db_type = get_active_db_type()
        if db_type == "firebase":
            return FirebaseDaySchedule()
        return DaySchedule

    # FixedSession, Stats, Logs
    @staticmethod
    def get_fixed_session_model():
        db_type = get_active_db_type()
        if db_type == "firebase":
            return FirebaseFixedSession()
        return FixedSession

    @staticmethod
    def get_stats_model():
        db_type = get_active_db_type()
        if db_type == "firebase":
            return FirebaseStats()
        return Stats

    @staticmethod
    def get_logs_model():
        db_type = get_active_db_type()
        if db_type == "firebase":
            return FirebaseLogs()
        return Logs