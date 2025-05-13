from src.utils.db_factory import DatabaseFactory
from  src.models import  Session,Task
from src.controllers.task_controller import get_task
from src.utils.util_func import model_to_dict
from src.utils.db_utils import get_active_db_type
from src.database import db
from datetime import datetime

def create_session(date, start_time, task_id):
    db_type = get_active_db_type()
    
    if db_type == "firebase":
        session_model = DatabaseFactory.get_session_model()
        task_model = DatabaseFactory.get_task_model()
        task = task_model.get_by_id(task_id)
        if not task:
            return None
        return session_model.create(
            duration=task['duration'],
            date=date,
            start_time=start_time,
            task_id=task_id
        )
    else:
        task = get_task(task_id)[0]
        session = Session(
            duration=task.duration,
            date=date,
            start_time=datetime.strptime(start_time, "%H:%M:%S").time(),
            task_id=task_id
        )
        db.session.add(session)
        db.session.commit()
        return session

def get_all_sessions():
    db_type = get_active_db_type()
    
    if db_type == "firebase":
        session_model = DatabaseFactory.get_session_model()
        return session_model.query_collection()
    else:
        return Session.query.all()

def get_session(id):
    db_type = get_active_db_type()
    
    if db_type == "firebase":
        session_model = DatabaseFactory.get_session_model()
        return session_model.get_by_id(id)
    else:
        return Session.query.filter_by(id=id).all()

def get_session_details(id):
    db_type = get_active_db_type()
    
    if db_type == "firebase":
        session_model = DatabaseFactory.get_session_model()
        task_model = DatabaseFactory.get_task_model()
        session = session_model.get_by_id(id)
        if session:
            task = task_model.get_by_id(session['task_id'])
            return {**session, "task": task}
        return None
    else:
        session = Session.query.get(id)
        if session:
            task = Task.query.get(session.task_id)
            return {
                "id": session.id,
                "duration": session.duration,
                "date": session.date,
                "start_time": session.start_time,
                "task_id": {
                    "id": task.id,
                    "title": task.title,
                    "duration": task.duration
                }
            }
        return None

def delete_session(session_id):
    db_type = get_active_db_type()
    
    if db_type == "firebase":
        session_model = DatabaseFactory.get_session_model()
        return session_model.delete(session_id)
    else:
        session = Session.query.get(session_id)
        if session:
            db.session.delete(session)
            db.session.commit()
            return True
        return False