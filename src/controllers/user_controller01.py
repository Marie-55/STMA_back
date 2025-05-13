# src/controllers/user_controller.py

from src.utils.db_factory import DatabaseFactory
from src.utils.db_utils import get_active_db_type
from src.database import db

def get_user(email):
    db_type = get_active_db_type()
    
    if db_type == "firebase":
        user_model = DatabaseFactory.get_user_model()
        return user_model.get_by_email(email)
    else:
        # SQLite implementation
        User = DatabaseFactory.get_user_model()
        return User.query.filter_by(email=email).first()

def create_user(email, password):
    db_type = get_active_db_type()
    
    if db_type == "firebase":
        user_model = DatabaseFactory.get_user_model()
        return user_model.create(email, password)
    else:
        # SQLite implementation
        User = DatabaseFactory.get_user_model()
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return new_user