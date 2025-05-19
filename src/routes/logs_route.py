
from flask import Blueprint, request, jsonify
from src.controllers.logs_controller import LogsController
from src.utils.response_helper import format_response
from datetime import datetime

logs_bp = Blueprint('logs', __name__)
logs_controller = LogsController()

@logs_bp.route('/create', methods=['POST'])
def create_log():
    """Create a new log entry"""
    try:
        data = request.json
        if not data or 'user_id' not in data:
            return jsonify({
                'success': False,
                'error': 'missing_user_id',
                'message': 'User ID is required'
            }), 400

        log = logs_controller.create_log(
            user_id=data['user_id'],
            login_time=data.get('login_time')
        )
        
        return jsonify({
            'success': True,
            'message': 'Log created successfully',
            'data': format_response(log)
        }), 201

    except ValueError as e:
        return jsonify({
            'success': False,
            'error': 'invalid_data',
            'message': str(e)
        }), 400

@logs_bp.route('/logout', methods=['POST'])
def update_logout():
    """Update logout time for a log"""
    try:
        data = request.json
        if not data or 'date' not in data:
            return jsonify({
                'success': False,
                'error': 'missing_date',
                'message': 'Date is required'
            }), 400

        log = logs_controller.update_logout(
            date=data['date'],
            logout_time=data.get('logout_time')
        )
        
        if not log:
            return jsonify({
                'success': False,
                'error': 'not_found',
                'message': 'Log not found'
            }), 404

        return jsonify({
            'success': True,
            'message': 'Logout time updated successfully',
            'data': format_response(log)
        }), 200

    except ValueError as e:
        return jsonify({
            'success': False,
            'error': 'invalid_data',
            'message': str(e)
        }), 400

@logs_bp.route('/increment-tasks', methods=['POST'])
def increment_tasks():
    """Increment completed tasks counter"""
    try:
        data = request.json
        if not data or 'date' not in data:
            return jsonify({
                'success': False,
                'error': 'missing_date',
                'message': 'Date is required'
            }), 400

        log = logs_controller.increment_tasks(data['date'])
        
        if not log:
            return jsonify({
                'success': False,
                'error': 'not_found',
                'message': 'Log not found'
            }), 404

        return jsonify({
            'success': True,
            'message': 'Tasks counter incremented successfully',
            'data': format_response(log)
        }), 200

    except ValueError as e:
        return jsonify({
            'success': False,
            'error': 'invalid_data',
            'message': str(e)
        }), 400

@logs_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_logs(user_id):
    """Get all logs for a user"""
    try:
        logs = logs_controller.get_by_user(user_id)
        return jsonify({
            'success': True,
            'data': [format_response(log) for log in logs]
        }), 200

    except ValueError as e:
        return jsonify({
            'success': False,
            'error': 'server_error',
            'message': str(e)
        }), 500

@logs_bp.route('/date/<string:date>', methods=['GET'])
def get_log_by_date(date):
    """Get log by date"""
    try:
        log = logs_controller.get_by_date(date)
        if not log:
            return jsonify({
                'success': False,
                'error': 'not_found',
                'message': 'Log not found'
            }), 404

        return jsonify({
            'success': True,
            'data': format_response(log)
        }), 200

    except ValueError as e:
        return jsonify({
            'success': False,
            'error': 'server_error',
            'message': str(e)
        }), 500

@logs_bp.route('/range', methods=['GET'])
def get_logs_range():
    """Get logs within a date range"""
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

        logs = logs_controller.get_by_date_range(
            user_id=int(user_id),
            start_date=start_date,
            end_date=end_date
        )

        return jsonify({
            'success': True,
            'data': [format_response(log) for log in logs]
        }), 200

    except ValueError as e:
        return jsonify({
            'success': False,
            'error': 'invalid_data',
            'message': str(e)
        }), 400
