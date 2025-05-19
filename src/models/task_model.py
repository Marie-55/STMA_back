from src.database import db
"""
        CREATE TABLE IF NOT EXISTS Task (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            category TEXT,
            deadline TEXT,
            duration INTEGER,
            priority INTEGER,
            is_scheduled BOOLEAN,
            to_reschedule BOOLEAN,
            is_synched BOOLEAN,
            status TEXT DEFAULT 'To Do',
            user_id INTEGER,

            FOREIGN KEY (user_id) REFERENCES User(id)
        )
"""
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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='task', lazy=True)