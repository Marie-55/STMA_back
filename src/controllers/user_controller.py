from src.utils.db_factory import DatabaseFactory
from  src.models import  User, Task, Session, DaySchedule, WeekSchedule, Stats, Logs
from src.utils.db_utils import get_active_db_type
from src.database import db
from werkzeug.security import generate_password_hash

def create_user(email, password):
    db_type = get_active_db_type()
    
    if db_type == "firebase":
        user_model = DatabaseFactory.get_user_model()
        return user_model.create(email=email, password=password)
    else:
        user = User(email=email, password_hash=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        print(type(user))
        return user

def get_user(email):
    db_type = get_active_db_type()
    
    if db_type == "firebase":
        user_model = DatabaseFactory.get_user_model()
        return user_model.get_by_email(email)
    else:
        user = User.query.filter_by(email=email).first()
        print(f"the user is {user}")
        if user:
            print("found the user")
            return user
        return None
    
def get_user_password(email):
    db_type = get_active_db_type()
    
    if db_type == "firebase":
        user_model = DatabaseFactory.get_user_model()
        usr= user_model.get_by_email(email)
        return usr.password_hash
    else:
        user = User.query.filter_by(email=email).first()
        print(f"the user is {user}")
        if user:
            print("found the user")
            return user.password_hash
        return None

def update_user_password(email, password):
    db_type = get_active_db_type()
    
    if db_type == "firebase":
        user_model = DatabaseFactory.get_user_model()
        return user_model.update(email, {"password": password})
    else:
        user = User.query.get(email)
        if user:
            user.password_hash = generate_password_hash(password)
            db.session.commit()
            return user
        return None

def delete_user(email):
    db_type = get_active_db_type()
    
    if db_type == "firebase":
        user_model = DatabaseFactory.get_user_model()
        return user_model.delete(email)
    else:
        user = User.query.get(email)
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False