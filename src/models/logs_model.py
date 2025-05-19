from src.database import db

"""
    CREATE TABLE IF NOT EXISTS Logs (
            date TEXT PRIMARY KEY,
            user_id INTEGER,
            login_time TEXT,
            logout_time TEXT,
            tasks_completed INTEGER DEFAULT 0,
            FOREIGN KEY (user_id) REFERENCES User(id)
        )
"""
class Logs(db.Model):
    date = db.Column(db.String, primary_key=True)
    login_time = db.Column(db.String, nullable=False)
    logout_time = db.Column(db.String, nullable=False)
    tasks_completed = db.Column(db.Integer, default=0) 

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship("User", backref="logs")