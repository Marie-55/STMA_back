from flask import Blueprint, request, jsonify
from src.controllers.stats_controller import StatsController
from src.utils.response_helper import format_response

stats_routes = Blueprint('stats', __name__)
stats_controller = StatsController()

@stats_routes.route('/user/<int:user_id>', methods=['GET'])
def get_stats(user_id):
    """Get user statistics"""
    try:
        stats = stats_controller.get_user_stats(user_id)
        if not stats:
            return jsonify({
                'success': False,
                'error': 'not_found',
                'message': 'Stats not found'
            }), 404

        return jsonify({
            'success': True,
            'data': format_response(stats)
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'server_error',
            'message': str(e)
        }), 500

@stats_routes.route('/user/<int:user_id>/task', methods=['POST'])
def update_task_stats(user_id):
    """Update task completion statistics"""
    try:
        data = request.json
        if not isinstance(data.get('completed'), bool):
            return jsonify({
                'success': False,
                'error': 'invalid_data',
                'message': 'Task completion status (completed) is required as boolean'
            }), 400

        stats = stats_controller.update_task_stats(
            user_id=user_id,
            task_completed=data['completed']
        )

        if not stats:
            return jsonify({
                'success': False,
                'error': 'not_found',
                'message': 'Stats not found'
            }), 404

        return jsonify({
            'success': True,
            'message': 'Task stats updated successfully',
            'data': format_response(stats)
        }), 200

    except ValueError as e:
        return jsonify({
            'success': False,
            'error': 'invalid_data',
            'message': str(e)
        }), 400

@stats_routes.route('/user/<int:user_id>/productivity', methods=['GET'])
def calculate_productivity(user_id):
    """Calculate and get productivity score"""
    try:
        stats = stats_controller.calculate_productivity_score(user_id)
        if not stats:
            return jsonify({
                'success': False,
                'error': 'not_found',
                'message': 'Stats not found'
            }), 404

        return jsonify({
            'success': True,
            'data': format_response(stats)
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'server_error',
            'message': str(e)
        }), 500

@stats_routes.route('/user/<int:user_id>/duration', methods=['POST'])
def update_duration(user_id):
    """Update average task duration"""
    try:
        data = request.json
        if not data or 'duration' not in data:
            return jsonify({
                'success': False,
                'error': 'missing_duration',
                'message': 'Duration is required'
            }), 400

        stats = stats_controller.update_average_duration(
            user_id=user_id,
            duration=float(data['duration'])
        )

        if not stats:
            return jsonify({
                'success': False,
                'error': 'not_found',
                'message': 'Stats not found'
            }), 404

        return jsonify({
            'success': True,
            'message': 'Average duration updated successfully',
            'data': format_response(stats)
        }), 200

    except ValueError as e:
        return jsonify({
            'success': False,
            'error': 'invalid_data',
            'message': str(e)
        }), 400

@stats_routes.route('/user/<int:user_id>/create', methods=['POST'])
def create_stats(user_id):
    """Create initial stats for a new user"""
    try:
        stats = stats_controller.create_user_stats(user_id)
        return jsonify({
            'success': True,
            'message': 'Stats created successfully',
            'data': format_response(stats)
        }), 201

    except ValueError as e:
        return jsonify({
            'success': False,
            'error': 'invalid_data',
            'message': str(e)
        }), 400