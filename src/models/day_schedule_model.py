from src.database import db
from sqlalchemy import ARRAY

class DaySchedule(db.Model):
    date = db.Column(db.Date, primary_key=True)
    session_ids = db.Column(ARRAY(db.Integer), nullable=True)  # Store session IDs as a list
