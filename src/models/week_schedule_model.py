from src.database import db

class WeekSchedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    day_schedules = db.Column(db.JSON, nullable=True)  # Store day schedule IDs as a list
