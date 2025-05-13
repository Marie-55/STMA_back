from src.utils.db_factory import DatabaseFactory
from src.utils.db_utils import get_active_db_type
from src.database import db
from src.models import Logs  # SQLite model
from datetime import datetime
from  src.models import  Logs

def log_user_activity(user_id):
    db_type = get_active_db_type()

    if db_type == "firebase":
        log_model = DatabaseFactory.get_log_model()
        return log_model.create(user_id=user_id, date=datetime.utcnow().date())
    else:
        log_entry = Logs(user_id=user_id, date=datetime.utcnow().date())
        db.session.add(log_entry)
        db.session.commit()
        return log_entry
