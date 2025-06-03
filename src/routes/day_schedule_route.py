from flask import Blueprint, request, jsonify
from src.controllers.day_schedule_controller import DayScheduleController
from datetime import datetime
from src.utils.response_helper import format_response

day_schedule_bp = Blueprint('day_schedule', __name__)
day_schedule_controller = DayScheduleController()

@day_schedule_bp.route('/create', methods=['POST'])
def create_schedule():
    """Create a new day schedule"""
    try:
        data = request.json
        if not data or 'date' not in data:
            return jsonify({
                'success': False,
                'error': 'missing_date',
                'message': 'Date is required'
            }), 400

        schedule = day_schedule_controller.create_schedule(
            schedule_date=data['date'],
            user_id=data.get('user_id'),
            sessions=data.get('sessions', [])
        )
        
        return jsonify({
            'success': True,
            'message': 'Schedule created successfully',
            'data': format_response(schedule)
        }), 201

    except ValueError as e:
        return jsonify({
            'success': False,
            'error': 'invalid_data',
            'message': str(e)
        }), 400

@day_schedule_bp.route('/add_session', methods=['POST'])
def add_session():
    """Add a session to a schedule"""
    try:
        data = request.json
        if not data or 'date' not in data or 'session_id' not in data:
            return jsonify({
                'success': False,
                'error': 'missing_fields',
                'message': 'Date and session_id are required'
            }), 400

        schedule = day_schedule_controller.add_session(
            schedule_date=data['date'],
            session_id=data['session_id']
        )
        
        if not schedule:
            return jsonify({
                'success': False,
                'error': 'not_found',
                'message': 'Schedule or session not found'
            }), 404

        return jsonify({
            'success': True,
            'message': 'Session added successfully',
            'data': format_response(schedule)
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'server_error',
            'message': str(e)
        }), 500

@day_schedule_bp.route('/date/<string:date>', methods=['GET'])
def get_schedule(date):
    """Get schedule for a specific date"""
    try:
        schedule = day_schedule_controller.get_by_date(date)
        if not schedule:
            return jsonify({
                'success': False,
                'error': 'not_found',
                'message': 'Schedule not found'
            }), 404

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

@day_schedule_bp.route('/date/<string:date>/sessions', methods=['GET'])
def get_schedule_sessions(date):
    """Get all sessions for a specific date"""
    try:
        sessions = day_schedule_controller.get_sessions(date)
        return jsonify({
            'success': True,
            'data': [format_response(session) for session in sessions]
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'server_error',
            'message': str(e)
        }), 500

@day_schedule_bp.route('/remove_session', methods=['POST'])
def remove_session():
    """Remove a session from a schedule"""
    try:
        data = request.json
        if not data or 'date' not in data or 'session_id' not in data:
            return jsonify({
                'success': False,
                'error': 'missing_fields',
                'message': 'Date and session_id are required'
            }), 400

        schedule = day_schedule_controller.remove_session(
            schedule_date=data['date'],
            session_id=data['session_id']
        )
        
        if not schedule:
            return jsonify({
                'success': False,
                'error': 'not_found',
                'message': 'Schedule or session not found'
            }), 404

        return jsonify({
            'success': True,
            'message': 'Session removed successfully',
            'data': format_response(schedule)
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'server_error',
            'message': str(e)
        }), 500

@day_schedule_bp.route('/date/<string:date>', methods=['DELETE'])
def delete_schedule(date):
    """Delete a day schedule"""
    try:
        success = day_schedule_controller.delete_schedule(date)
        if not success:
            return jsonify({
                'success': False,
                'error': 'not_found',
                'message': 'Schedule not found'
            }), 404

        return jsonify({
            'success': True,
            'message': 'Schedule deleted successfully'
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'server_error',
            'message': str(e)
        }), 500