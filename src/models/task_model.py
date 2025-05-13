from src.database import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50),nullable=False)
    category = db.Column(db.String(50), nullable=False)
    deadline = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # Duration in hours
    priority = db.Column(db.String(20), nullable=False)  # Low, Medium, High
    is_scheduled = db.Column(db.Boolean, default=False)
    to_reschedule = db.Column(db.Boolean, default=False)
    is_synched = db.Column(db.Boolean, default=False)
    status=db.Column(db.String,default="To Do",nullable=False)
    user=db.Column(db.String,default="test@gmail.com",nullable=False)
