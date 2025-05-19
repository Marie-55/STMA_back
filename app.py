# app.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from src.routes import task_routes, day_routes, week_routes, log_routes, session_routes, stat_routes, user_routes, auth_routes
from src.services.schedule_task import schedule_blueprint
import os
from src.utils.db_utils import LOCAL_DB, USE_FIREBASE, REMOTE_DB
from src.database import db
from src.config.firebase_config import FirebaseConfig

#  added by bilal 
from flask_cors import CORS



def create_app():
    app = Flask(__name__)
#  added by bilal 
    
    CORS(app, origins="*", supports_credentials=True)

    if USE_FIREBASE:
        # Initialize Firebase if enabled
        firebase = FirebaseConfig()
        firebase.initialize_app()
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = LOCAL_DB

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize SQLAlchemy with app
    db.init_app(app)


        


    # Register all Blueprints
    app.register_blueprint(task_routes, url_prefix='/api/tasks')
    app.register_blueprint(day_routes, url_prefix='/api/day')
    app.register_blueprint(schedule_blueprint, url_prefix='/api')
    app.register_blueprint(week_routes, url_prefix='/api/week')
    app.register_blueprint(log_routes, url_prefix='/api/logs')
    app.register_blueprint(session_routes, url_prefix='/api/session')
    app.register_blueprint(stat_routes, url_prefix='/api/stats')
    app.register_blueprint(user_routes, url_prefix='/api/user')
    app.register_blueprint(auth_routes, url_prefix='/api/auth')

    # Create all SQLAlchemy tables
    with app.app_context():
        db.create_all()

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
