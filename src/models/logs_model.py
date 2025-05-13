from src.database import db
from datetime import datetime


class Logs(db.Model):
    date = db.Column(db.Date, primary_key=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship("User", backref="logs")