
from flask import Blueprint, jsonify, request
from datetime import datetime, timedelta, date
from AI_services.database_integrate import DatabaseScheduler  # Assuming this is in the same package
from src.database import db
import sys
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]
sys.path.append(str(project_root))

scheduling_bp = Blueprint('scheduling', __name__, url_prefix='/api/schedule')

@scheduling_bp.route('/generate', methods=['POST'])
def generate_schedule():
    try:
        data = request.get_json()
        user_email = data.get('user_id')
        
        if not user_email:
            return jsonify({"error": "user_email is required"}), 400

        db_session = db.session
        scheduler = DatabaseScheduler( user_email)
        schedule = scheduler.run_scheduling()
        
        # Format response
        formatted = []
        for day, sessions in schedule.items():
            day_info = {
                "date": day.isoformat(),
                "tasks": []
            }
            for session in sessions:
                day_info["tasks"].append({
                    "task_id": session['task_id'],
                    "title": session.get('title', ''),
                    "start": session['start_time'].strftime('%H:%M'),
                    "end": (datetime.combine(day, session['start_time']) + 
                          timedelta(minutes=session['duration'])).strftime('%H:%M'),
                    "duration": f"{session['duration']} minutes",
                    "category": session.get('category', '')
                })
            formatted.append(day_info)
        
        return jsonify({
            "status": "success",
            "schedule": formatted
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500