
from flask import Blueprint, request, jsonify
import src.controllers.day_schedule_controller  as day 
from datetime import datetime
from src.utils.util_func import model_to_dict

day_routes = Blueprint("/day", __name__)

#write
@day_routes.route("/write/add", methods=["POST"])
def add_day_schedule():
    data = request.json
    schedule = day.create_day_schedule(data.get("date"), data.get("session_ids"))
    if schedule:
        return jsonify({"message": "Day schedule added", "schedule": model_to_dict(schedule)}), 200
    else:
        return jsonify({"message": "No days found", "schedule": "empty"}), 404

@day_routes.route("/write/session", methods=["POST"])
def add_session_to_schedule():
    data = request.json
    schedule = day.add_session_to_day(data.get("date"), data.get("session_ids"))
    if schedule:
        return jsonify({"message": "Day schedule added", "schedule": model_to_dict(schedule)}), 200
    else:
        return jsonify({"message": "No days found", "schedule": "empty"}), 404

#reading
@day_routes.route("/read/all")
def get_all_days():
    data =request.json
    days= day.get_all_days()
    if days:
        return jsonify({"message": "all Days fetched", "schedule": [model_to_dict(day) for day in days]}), 200
    else:
        return jsonify({"message": "No days found", "schedule": "empty"}), 404
    
@day_routes.route("/read/day_sessions/<string:date>")
def get_day_session_details(date):
    date=datetime.strptime(date, '%d-%m-%Y').date()
    schedule=day.get_day_sessions(date)
    if schedule:
        return jsonify({"message": "Sessions of the day fetched", "schedule": model_to_dict(schedule)}), 200
    else:
        return jsonify({"message": "No days found", "schedule": "empty"}), 404
