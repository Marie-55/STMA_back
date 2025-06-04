from flask import Blueprint, request, jsonify
from src.controllers.session_controller import SessionController
from datetime import datetime
from src.utils.response_helper import format_response

session_routes_bp = Blueprint('session', __name__)
session_controller = SessionController()

# """
#     CREATE TABLE IF NOT EXISTS Session (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         duration INTEGER,
#         date TEXT,
#         start_time TEXT,
        
#         user_id INTEGER,
#         day_schedule_date TEXT,
#         FOREIGN KEY (user_id) REFERENCES User(id),
#         FOREIGN KEY (day_schedule_date) REFERENCES DaySchedule(date)
#     )
# """

@session_routes_bp.route('/create', methods=['POST'])
def create_session():
    """Create a new session"""
    try:
        data = request.json
        required_fields = ['title', 'date', 'start_time', 'user_id', 'duration', 'task_id']
        if not data or not all(k in data for k in required_fields):
            return jsonify({
                'success': False,
                'error': 'missing_fields',
                'message': f'Required fields: {", ".join(required_fields)}'
            }), 400

        session = session_controller.create_session(
            title=data['title'],
            date=data['date'],
            start_time=data['start_time'],
            user_id=data['user_id'],
            task=data['task_id'],  # Optional
            duration=data['duration'],
        )
        
        return jsonify({
            'success': True,
            'message': 'Session created successfully',
            'data': format_response(session)
        }), 201

    except ValueError as e:
        return jsonify({
            'success': False,
            'error': 'invalid_data',
            'message': str(e)
        }), 400

@session_routes_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_sessions(user_id):
    """Get all sessions for a user"""
    try:
        print(type(user_id))
        sessions = session_controller.get_user_sessions(user_id)
        return jsonify({
            'success': True,
            'data': format_response(sessions)
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'server_error',
            'message': str(e)
        }), 500

@session_routes_bp.route('/<int:session_id>', methods=['GET'])
def get_session(session_id):
    """Get session by ID"""
    try:
        session = session_controller.get_session_by_id(session_id)
        if not session:
            return jsonify({
                'success': False,
                'error': 'not_found',
                'message': 'Session not found'
            }), 404

        return jsonify({
            'success': True,
            'data': format_response(session)
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'server_error',
            'message': str(e)
        }), 500

@session_routes_bp.route('/schedule/<string:date>', methods=['GET'])
def get_schedule_sessions(date):
    """Get sessions for a specific day schedule"""
    try:
        sessions = session_controller.get_schedule_sessions(date)
        return jsonify({
            'success': True,
            'data': format_response(sessions)
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'server_error',
            'message': str(e)
        }), 500

@session_routes_bp.route('/<int:session_id>', methods=['PUT'])
def update_session(session_id):
    """Update session"""
    try:
        data = request.json
        if not data:
            return jsonify({
                'success': False,
                'error': 'missing_data',
                'message': 'No data provided for update'
            }), 400

        session = session_controller.update_session(session_id, data)
        if not session:
            return jsonify({
                'success': False,
                'error': 'not_found',
                'message': 'Session not found'
            }), 404

        return jsonify({
            'success': True,
            'message': 'Session updated successfully',
            'data': format_response(session)
        }), 200

    except ValueError as e:
        return jsonify({
            'success': False,
            'error': 'invalid_data',
            'message': str(e)
        }), 400

@session_routes_bp.route('/<int:session_id>', methods=['DELETE'])
def delete_session(session_id):
    """Delete session"""
    try:
        success = session_controller.delete_session(session_id)
        if not success:
            return jsonify({
                'success': False,
                'error': 'not_found',
                'message': 'Session not found'
            }), 404

        return jsonify({
            'success': True,
            'message': 'Session deleted successfully'
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'server_error',
            'message': str(e)
        }), 500

@session_routes_bp.route('/', methods=['GET'])
def get_all_sessions():
    """Get all sessions"""
    try:
        sessions = session_controller.get_all_sessions()
        return jsonify({
            'success': True,
            'data': format_response(sessions)
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'server_error',
            'message': str(e)
        }), 500

@session_routes_bp.route('/<int:session_id>/task/', methods=['GET'])
def get_task_id(session_id):
    """Get task ID associated with a session"""
    try:
        task_id = session_controller.get_task_id(session_id)
        if task_id is None:
            return jsonify({
                'success': False,
                'error': 'not_found',
                'message': 'Session not found or no task associated'
            }), 404

        return jsonify({
            'success': True,
            'data': {'task_id': task_id}
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'server_error',
            'message': str(e)
        }), 500
    
@session_routes_bp.route('/<int:session_id>/remove_from_day_schedule/<string:day_schedule_date>', methods=['DELETE'])
def delete_session_from_day_schedule(session_id, day_schedule_date):
    """Delete session from a specific day schedule"""
    try:
        success = session_controller.delete_session_from_day_schedule(session_id, day_schedule_date)
        if not success:
            return jsonify({
                'success': False,
                'error': 'not_found',
                'message': 'Session not found or not associated with the specified day schedule'
            }), 404

        return jsonify({
            'success': True,
            'message': 'Session removed from day schedule successfully'
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'server_error',
            'message': str(e)
        }), 500

@session_routes_bp.route('/user/<int:user_id>/date/<string:date>', methods=['GET'])
def get_user_schedule_sessions(user_id, date):
    """Get sessions for a specific day schedule and user"""
    try:
        # First get sessions for the schedule date
        schedule_sessions = session_controller.get_schedule_sessions(date)
        print (f"Schedule sessions for date {date}: {schedule_sessions}")
        
        # Filter sessions for the specific user
        user_schedule_sessions = [
            session for session in schedule_sessions 
            if str(session.get('user_id')) == str(user_id)
        ]
        
        return jsonify({
            'success': True,
            'data': format_response(user_schedule_sessions)
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'server_error',
            'message': str(e)
        }), 500