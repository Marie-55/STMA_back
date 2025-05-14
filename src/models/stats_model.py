from src.database import db

class Stats(db.Model):
    """ 
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            missed_tasks INTEGER DEFAULT 0,
            completed_tasks INTEGER DEFAULT 0,
            productivity_score REAL DEFAULT 0,
            average_task_duration REAL DEFAULT 0,
            user_id INTEGER,

            FOREIGN KEY (user_id) REFERENCES User(id)
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    missed_tasks = db.Column(db.Integer, default=0)
    completed_tasks = db.Column(db.Integer, default=0)
    productivity_score = db.Column(db.Float, default=0.0)
    average_task_duration = db.Column(db.Float, default=0.0)