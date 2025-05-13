from src.database import db
from datetime import datetime

class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    duration = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, default=datetime.utcnow, nullable=False)
    start_time = db.Column(db.String, nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)

    task = db.relationship("Task", backref="sessions")