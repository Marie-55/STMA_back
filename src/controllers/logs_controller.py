from src.utils.db_factory import DatabaseFactory
from src.utils.db_utils import get_active_db_type
from src.database import db
from datetime import datetime
from  src.models import  Logs
from sqlalchemy.exc import SQLAlchemyError



class LogsController:
    
    @staticmethod
    def create_log(user_id: int):
        db_type = get_active_db_type()
        
        if db_type == "firebase":
            logs_model = DatabaseFactory.get_logs_model()
            return logs_model.create(
                user_email=str(user_id),
                date=datetime.now().isoformat(),
                action="user_activity"
            )
        else:
            try:
                new_log = Logs(
                    date=datetime.utcnow().date(),
                    user_id=user_id
                )
                db.session.add(new_log)
                db.session.commit()
                return new_log
            except SQLAlchemyError as e:
                db.session.rollback()
                raise e

    @staticmethod
    def get_log_by_date(date: datetime.date):
        db_type = get_active_db_type()
        
        if db_type == "firebase":
            logs_model = DatabaseFactory.get_logs_model()
            date_str = date.isoformat()
            logs = logs_model.query_collection("date", "==", date_str)
            return logs[0] if logs else None
        else:
            return Logs.query.filter_by(date=date).first()

    @staticmethod
    def get_logs_by_user(user_id: int):
        db_type = get_active_db_type()
        
        if db_type == "firebase":
            logs_model = DatabaseFactory.get_logs_model()
            return logs_model.query_collection("user_email", "==", str(user_id))
        else:
            return Logs.query.filter_by(user_id=user_id).order_by(Logs.date.desc()).all()