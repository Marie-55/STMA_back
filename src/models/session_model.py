from src.database import db

class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    duration = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String, nullable=False)
    start_time = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    day_schedule_date = db.Column(db.String, db.ForeignKey('day_schedule.date'), nullable=False)
    user = db.relationship('User', backref='session', lazy=True)
    day_schedule = db.relationship('DaySchedule', backref='session', lazy=True)