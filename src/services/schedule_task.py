from flask import Blueprint, request, jsonify
from src.models import Task, Session, DaySchedule
from src.database import db
from datetime import datetime, timedelta

schedule_blueprint = Blueprint('schedule', __name__)

def find_least_crowded_day(before_date, required_duration):
    """
    Find a date before the task deadline where the session can fit.
    """
    days = DaySchedule.query.filter(DaySchedule.date <= before_date).all()
    
    # Sort days by the total scheduled hours (less crowded first)
    days.sort(key=lambda d: sum(s.duration for s in d.sessions))

    for day in days:
        available_hours = 8 - sum(s.duration for s in day.sessions)  # Assume max 8 hours per day
        
        if available_hours >= required_duration:
            return day.date  # Return the first available date

    return None  # No suitable day found

@schedule_blueprint.route('/schedule_task', methods=['POST'])
def schedule_task():
    """
    Schedule a task automatically before its deadline.
    """
    data = request.json
    task_id = data.get("task_id")
    
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    # Find the best date to schedule before the deadline
    best_date = find_least_crowded_day(task.deadline, task.duration)

    if not best_date:
        return jsonify({"error": "No available days for scheduling"}), 400

    # Create a session and assign it to the best date
    new_session = Session(
        task_id=task.id,
        duration=task.duration,
        date=best_date,
        start_time="10:00"  # Example: default start time
    )

    db.session.add(new_session)
    db.session.commit()

    return jsonify({"message": "Task scheduled successfully", "scheduled_date": best_date})
