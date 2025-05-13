# src/utils/db_factory.py

from src.utils.db_utils import get_active_db_type
from src.models.user_model import User
from src.models.task_model import Task
from src.models.stats_model import Stats
from src.models.logs_model import Logs
from src.models.session_model import Session
from src.models.day_schedule_model import DaySchedule
from src.models.week_schedule_model import WeekSchedule

# Import Firebase models
from src.models.firebase.user_model import FirebaseUser
from src.models.firebase.task_model import FirebaseTask
from src.models.firebase.stats_model import FirebaseStats
from src.models.firebase.logs_model import FirebaseLogs
from src.models.firebase.session_model import FirebaseSession
from src.models.firebase.day_schedule_model import FirebaseDaySchedule
from src.models.firebase.week_schedule_model import FirebaseWeekSchedule

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

    @staticmethod
    def get_week_schedule_model():
        db_type = get_active_db_type()
        if db_type == "firebase":
            return FirebaseWeekSchedule()
        return WeekSchedule