from src.utils.db_factory import DatabaseFactory
from src.utils.db_utils import get_active_db_type
from src.database import db
from  src.models import  Task


def create_task(title, category, deadline, duration, priority, sch, syn, to_sch, user):
    db_type = get_active_db_type()
    
    if db_type == "firebase":
        task_model = DatabaseFactory.get_task_model()
        return task_model.create(
            title=title,
            category=category,
            deadline=deadline,
            duration=duration,
            priority=priority,
            is_scheduled=sch,
            is_synched=syn,
            to_reschedule=to_sch,
            user_email=user
        )
    else:
        task = Task(
            title=title,
            category=category,
            deadline=deadline,
            duration=duration,
            priority=priority,
            is_scheduled=sch,
            is_synched=syn,
            to_reschedule=to_sch,
            user=user
        )
        db.session.add(task)
        db.session.commit()
        return task

def get_all_tasks():
    db_type = get_active_db_type()
    
    if db_type == "firebase":
        task_model = DatabaseFactory.get_task_model()
        return task_model.query_collection()
    else:
        return Task.query.all()

def get_task(id):
    db_type = get_active_db_type()
    
    if db_type == "firebase":
        task_model = DatabaseFactory.get_task_model()
        return task_model.get_by_id(id)
    else:
        return Task.query.filter_by(id=id).all()

def get_tasks_to_reschedule():
    db_type = get_active_db_type()
    
    if db_type == "firebase":
        task_model = DatabaseFactory.get_task_model()
        return task_model.query_collection("to_reschedule", "==", True)
    else:
        return Task.query.filter_by(to_reschedule=True).all()

def get_tasks_to_sync():
    db_type = get_active_db_type()
    
    if db_type == "firebase":
        task_model = DatabaseFactory.get_task_model()
        return task_model.query_collection("is_synched", "==", False)
    else:
        return Task.query.filter_by(is_synched=False).all()

def get_tasks_by_status(status):
    db_type = get_active_db_type()
    
    if db_type == "firebase":
        task_model = DatabaseFactory.get_task_model()
        return task_model.query_collection("status", "==", status)
    else:
        return Task.query.filter_by(status=status).all()

def search_tasks(query):
    db_type = get_active_db_type()
    
    if not query:
        return None
        
    if db_type == "firebase":
        task_model = DatabaseFactory.get_task_model()
        all_tasks = task_model.query_collection()
        return [task for task in all_tasks if 
               query.lower() in task['title'].lower() or 
               (task.get('category') and query.lower() in task['category'].lower())]
    else:
        search = f"%{query}%"
        return Task.query.filter(
            db.or_(
                Task.title.ilike(search),
                Task.category.ilike(search)
            )
        ).all()

def update_task_status(task_id, new_status):
    db_type = get_active_db_type()
    
    if db_type == "firebase":
        task_model = DatabaseFactory.get_task_model()
        return task_model.update(task_id, {"status": new_status})
    else:
        task = Task.query.get(task_id)
        if task:
            task.status = new_status
            db.session.commit()
            return task
        return None

def delete_task(task_id):
    db_type = get_active_db_type()
    
    if db_type == "firebase":
        task_model = DatabaseFactory.get_task_model()
        return task_model.delete(task_id)
    else:
        task = Task.query.get(task_id)
        if task:
            db.session.delete(task)
            db.session.commit()
            return True
        return False