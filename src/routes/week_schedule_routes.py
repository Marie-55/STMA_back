
from flask import Blueprint, request, jsonify
import src.controllers.week_schedule_controller  as week 
from datetime import datetime

week_routes = Blueprint("week_schedule_routes", __name__)

@week_routes.route("/week_schedule", methods=["POST"])
def add_week_schedule():
    data = request.json
    schedule = week.create_week_schedule(data.get("start_date"), data.get("end_date"), data.get("day_schedules"))
    return jsonify({"message": "Week schedule added", "schedule": schedule.__dict__}), 201
