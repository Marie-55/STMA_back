from src.database import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    #stats_id = db.Column(db.Integer, db.ForeignKey('stats.id'), nullable=True)
    stats = db.relationship("Stats", backref="user", uselist=False)
