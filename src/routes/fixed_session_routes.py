from flask import Blueprint, request, jsonify
from src.controllers.fixedSession_controller import FixedSessionController
from src.utils.response_helper import format_response

fixed_session_routes_bp = Blueprint('fixed_session', __name__)
fixed_session_controller = FixedSessionController()

@fixed_session_routes_bp.route('/create', methods=['POST'])
def create_fixed_session():
    """Create a new fixed session"""
    try:
        data = request.json
        required_fields = ['title', 'day_index', 'duration', 'start_time', 'user_id']
        
        if not data or not all(field in data for field in required_fields):
            return jsonify({
                'success': False,
                'error': 'missing_fields',
                'message': 'All fields (title, day_index, duration, start_time, user_id) are required'
            }), 400

        session = fixed_session_controller.create_fixed_session(
            title=data['title'],
            day_index=int(data['day_index']),
            duration=float(data['duration']),
            start_time=data['start_time'],
            user_id=data['user_id']
        )
        
        return jsonify({
            'success': True,
            'message': 'Fixed session created successfully',
            'data': format_response(session)
        }), 201

    except ValueError as e:
        return jsonify({
            'success': False,
            'error': 'invalid_data',
            'message': str(e)
        }), 400

@fixed_session_routes_bp.route('/user/<user_id>', methods=['GET'])
def get_user_fixed_sessions(user_id):
    """Get all fixed sessions for a user"""
    try:
        sessions = fixed_session_controller.get_user_fixed_sessions(user_id)
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

@fixed_session_routes_bp.route('/user/<user_id>/day/<int:day_index>', methods=['GET'])
def get_day_fixed_sessions(user_id, day_index):
    """Get fixed sessions for a specific day"""
    try:
        if not 0 <= day_index <= 6:
            return jsonify({
                'success': False,
                'error': 'invalid_day',
                'message': 'Day index must be between 0 (Monday) and 6 (Sunday)'
            }), 400

        sessions = fixed_session_controller.get_day_fixed_sessions(user_id, day_index)
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

@fixed_session_routes_bp.route('/<int:session_id>', methods=['GET'])
def get_fixed_session(session_id):
    """Get fixed session by ID"""
    try:
        session = fixed_session_controller.get_fixed_session_by_id(session_id)
        if not session:
            return jsonify({
                'success': False,
                'error': 'not_found',
                'message': 'Fixed session not found'
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

@fixed_session_routes_bp.route('/<int:session_id>', methods=['PUT'])
def update_fixed_session(session_id):
    """Update fixed session"""
    try:
        data = request.json
        if not data:
            return jsonify({
                'success': False,
                'error': 'missing_data',
                'message': 'No data provided for update'
            }), 400

        session = fixed_session_controller.update_fixed_session(session_id, data)
        if not session:
            return jsonify({
                'success': False,
                'error': 'not_found',
                'message': 'Fixed session not found'
            }), 404

        return jsonify({
            'success': True,
            'message': 'Fixed session updated successfully',
            'data': format_response(session)
        }), 200

    except ValueError as e:
        return jsonify({
            'success': False,
            'error': 'invalid_data',
            'message': str(e)
        }), 400

@fixed_session_routes_bp.route('/<int:session_id>', methods=['DELETE'])
def delete_fixed_session(session_id):
    """Delete fixed session"""
    try:
        success = fixed_session_controller.delete_fixed_session(session_id)
        if not success:
            return jsonify({
                'success': False,
                'error': 'not_found',
                'message': 'Fixed session not found'
            }), 404

        return jsonify({
            'success': True,
            'message': 'Fixed session deleted successfully'
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'server_error',
            'message': str(e)
        }), 500

@fixed_session_routes_bp.route('/user/<user_id>/week', methods=['GET'])
def get_week_schedule(user_id):
    """Get weekly schedule of fixed sessions"""
    try:
        schedule = fixed_session_controller.get_week_schedule(user_id)
        return jsonify({
            'success': True,
            'data': format_response(schedule)
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'server_error',
            'message': str(e)
        }), 500