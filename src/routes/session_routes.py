from flask import Blueprint, request, jsonify
from src.controllers.session_controller import SessionController
from datetime import datetime
from src.utils.response_helper import format_response

session_routes = Blueprint('session', __name__)
session_controller = SessionController()

@session_routes.route('/create', methods=['POST'])
def create_session():
    """Create a new session"""
    try:
        data = request.json
        if not data or not all(k in data for k in ['date', 'start_time', 'user_id']):
            return jsonify({
                'success': False,
                'error': 'missing_fields',
                'message': 'Date, start time, and user ID are required'
            }), 400

        session = session_controller.create_session(
            date=data['date'],
            start_time=data['start_time'],
            user_id=data['user_id'],
            duration=data.get('duration'),
            day_schedule_date=data.get('day_schedule_date')
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

@session_routes.route('/user/<int:user_id>', methods=['GET'])
def get_user_sessions(user_id):
    """Get all sessions for a user"""
    try:
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

@session_routes.route('/<int:session_id>', methods=['GET'])
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

@session_routes.route('/schedule/<string:date>', methods=['GET'])
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

@session_routes.route('/range', methods=['GET'])
def get_sessions_range():
    """Get sessions within a date range"""
    try:
        user_id = request.args.get('user_id')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        if not all([user_id, start_date, end_date]):
            return jsonify({
                'success': False,
                'error': 'missing_parameters',
                'message': 'User ID, start date, and end date are required'
            }), 400

        sessions = session_controller.get_sessions_by_date_range(
            user_id=int(user_id),
            start_date=start_date,
            end_date=end_date
        )

        return jsonify({
            'success': True,
            'data': format_response(sessions)
        }), 200

    except ValueError as e:
        return jsonify({
            'success': False,
            'error': 'invalid_data',
            'message': str(e)
        }), 400

@session_routes.route('/<int:session_id>', methods=['PUT'])
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

@session_routes.route('/<int:session_id>', methods=['DELETE'])
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

@session_routes.route('/', methods=['GET'])
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


