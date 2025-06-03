from src.database import db

class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)  # Add title field
    duration = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String, nullable=False)
    start_time = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=True)  # Add task relationship
    day_schedule_date = db.Column(db.String, db.ForeignKey('day_schedule.date'), nullable=True)  # Make nullable
    
    user = db.relationship('User', backref='sessions', lazy=True)
    task = db.relationship('Task', backref='sessions', lazy=True)  # Add task relationship
    day_schedule = db.relationship('DaySchedule', backref='sessions', lazy=True)
