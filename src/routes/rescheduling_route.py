from flask import Blueprint, request, jsonify
from datetime import datetime
from src.services.rescheduling import ReschedulingService
from src.controllers.session_controller import SessionController
from src.controllers.task_controller import TaskController
from src.utils.response_helper import format_response

# Create blueprint
rescheduling_bp = Blueprint('reschedule', __name__)

# Initialize controllers
session_controller = SessionController()
task_controller = TaskController()
rescheduling_service = ReschedulingService(session_controller, task_controller)

@rescheduling_bp.route('/<int:session_id>', methods=['POST'])
def reschedule_task(session_id):
    """Reschedule a task by deleting its session and updating its deadline"""
    try:
        data = request.json
        if not data or 'new_deadline' not in data:
            return jsonify({
                'success': False,
                'error': 'missing_fields',
                'message': 'New deadline is required'
            }), 400

        # 1. Get task_id from session
        task_id = session_controller.get_task_id(session_id)
        if not task_id:
            return jsonify({
                'success': False,
                'error': 'not_found',
                'message': 'No task associated with this session'
            }), 404

        # 2. Get session details for day_schedule_date
        session = session_controller.get_session_by_id(session_id)
        if not session:
            return jsonify({
                'success': False,
                'error': 'not_found',
                'message': 'Session not found'
            }), 404

        day_schedule_date = session.get('day_schedule_date')

        # 3. Delete session from day schedule if it's scheduled
        if day_schedule_date:
            session_controller.delete_session_from_day_schedule(session_id, day_schedule_date)

        # 4. Delete session
        session_controller.delete_session(session_id)

        # 5. Update task
        try:
            deadline = datetime.strptime(data['new_deadline'], "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            return jsonify({
                'success': False,
                'error': 'invalid_data',
                'message': 'Deadline must be in format YYYY-MM-DDThh:mm:ss'
            }), 400

        task = task_controller.update_task(task_id, {
            'deadline': deadline.strftime("%Y-%m-%dT%H:%M:%S"),
            'is_scheduled': False,
            'to_reschedule': True  # Mark for rescheduling
        })

        # 6. Call schedule_tasks
        user_id = session.get('user_id')
        rescheduling_service.schedule_tasks(user_id)

        return jsonify({
            'success': True,
            'message': 'Task rescheduled successfully',
            'data': format_response(task)
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'server_error',
            'message': str(e)
        }), 500