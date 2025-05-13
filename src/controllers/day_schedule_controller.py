from src.utils.db_factory import DatabaseFactory
from src.utils.db_utils import get_active_db_type
from src.database import db
from src.models import   DaySchedule
import src.controllers.session_controller as sess

def create_day_schedule(date, session_ids):
    db_type = get_active_db_type()
    
    if db_type == "firebase":
        day_model = DatabaseFactory.get_day_schedule_model()
        return day_model.create(date=date, tasks=session_ids)
    else:
        schedule = DaySchedule(date=date, session_ids=session_ids)
        db.session.add(schedule)
        db.session.commit()
        return schedule

def add_session_to_day(date, session_id):
    db_type = get_active_db_type()
    
    if db_type == "firebase":
        day_model = DatabaseFactory.get_day_schedule_model()
        day = day_model.get_by_date(date)
        if day:
            tasks = day.get('tasks', [])
            tasks.append(session_id)
            return day_model.update(date, {'tasks': tasks})
        else:
            return day_model.create(date=date, tasks=[session_id])
    else:
        schedule = DaySchedule.query.get(date)
        if schedule:
            schedule.session_ids.append(session_id)
            db.session.commit()
        else:
            schedule = DaySchedule(date=date, session_ids=[session_id])
            db.session.add(schedule)
            db.session.commit()
        return schedule

def get_day_sessions(date):
    db_type = get_active_db_type()
    
    if db_type == "firebase":
        day_model = DatabaseFactory.get_day_schedule_model()
        session_model = DatabaseFactory.get_session_model()
        day = day_model.get_by_date(date)
        if not day or 'tasks' not in day:
            return None
        return [session_model.get_by_id(sid) for sid in day['tasks']]
    else:
        schedule = DaySchedule.query.get(date)
        if schedule:
            return [get_session(sid)[0] for sid in schedule.session_ids]
        return None