from src.utils.db_factory import DatabaseFactory
from  src.models import  WeekSchedule
from src.utils.db_utils import get_active_db_type
from src.database import db
from src.models import WeekSchedule  # SQLite model
from datetime import datetime

def create_week_schedule(start_date, end_date, day_schedules):
    db_type = get_active_db_type()

    if db_type == "firebase":
        week_schedule_model = DatabaseFactory.get_week_schedule_model()
        return week_schedule_model.create(
            start_date=start_date,
            end_date=end_date,
            day_schedules=day_schedules
        )
    else:
        week_schedule = WeekSchedule(
            start_date=start_date,
            end_date=end_date,
            day_schedules=day_schedules
        )
        db.session.add(week_schedule)
        db.session.commit()
        return week_schedule
