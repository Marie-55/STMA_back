from src.database import db
"""
    CREATE TABLE IF NOT EXISTS DaySchedule (
        date TEXT PRIMARY KEY
    )
"""
class DaySchedule(db.Model):
    date = db.Column(db.Date, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('day_schedules', lazy=True))