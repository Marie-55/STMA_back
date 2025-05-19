from src.database import db

class FixedSession(db.Model):
    """ 
        CREATE TABLE IF NOT EXISTS FixedSession (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            day_index INTEGER,
            duration REAL,
            start_time TEXT,
            user_id INTEGER,
                            
            FOREIGN KEY (user_id) REFERENCES User(id)
        )
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    day_index = db.Column(db.Integer, nullable=False)  # 0 for Monday, 1 for Tuesday, etc.
    duration = db.Column(db.Float, nullable=False)  # Duration in hours
    start_time = db.Column(db.String(20), nullable=False)  # Start time in HH:MM format
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref='fixed_session', lazy=True)