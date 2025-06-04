from flask import Blueprint, request, jsonify
from src.controllers.task_controller import TaskController
from datetime import datetime
from src.utils.response_helper import format_response

task_routes_bp = Blueprint('tasks', __name__)
task_controller = TaskController()

@task_routes_bp.route('/create', methods=['POST'])
def create_task():
    """Create a new task"""
    try:
        data = request.json
        if not data or not all(k in data for k in ['title', 'category', 'deadline', 'duration', 'priority']):
            return jsonify({
                'success': False,
                'error': 'missing_fields',
                'message': 'Required fields missing'
            }), 400

        # Parse the ISO format datetime string
        try:
            deadline = datetime.strptime(data['deadline'], "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            return jsonify({
                'success': False,
                'error': 'invalid_data',
                'message': 'Deadline must be in format YYYY-MM-DDThh:mm:ss'
            }), 400

        task = task_controller.create_task(
            title=data['title'],
            category=data['category'],
            deadline=deadline.strftime("%Y-%m-%dT%H:%M:%S"),  # Store in ISO format
            duration=data['duration'],
            priority=data['priority'],
            is_scheduled=data.get('is_scheduled', False),
            is_synched=data.get('is_synched', False),
            to_reschedule=data.get('to_reschedule', False),
            user_id=data.get('user_id'),
            status=data.get('status', 'To Do')
        )

        return jsonify({
            'success': True,
            'message': 'Task created successfully',
            'data': format_response(task)
        }), 201

    except ValueError as e:
        return jsonify({
            'success': False,
            'error': 'invalid_data',
            'message': str(e)
        }), 400

@task_routes_bp.route('/user/<user_id>', methods=['GET'])
def get_user_tasks(user_id):
    """Get all tasks for a user"""
    try:
        tasks = task_controller.get_user_tasks(user_id)
        return jsonify({
            'success': True,
            'data': format_response(tasks)
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'server_error',
            'message': str(e)
        }), 500

@task_routes_bp.route('/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Get task by ID"""
    try:
        task = task_controller.get_task_by_id(task_id)
        if not task:
            return jsonify({
                'success': False,
                'error': 'not_found',
                'message': 'Task not found'
            }), 404

        return jsonify({
            'success': True,
            'data': format_response(task)
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'server_error',
            'message': str(e)
        }), 500

@task_routes_bp.route('/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update task"""
    try:
        data = request.json
        if not data:
            return jsonify({
                'success': False,
                'error': 'missing_data',
                'message': 'No data provided for update'
            }), 400

        task = task_controller.update_task(task_id, data)
        if not task:
            return jsonify({
                'success': False,
                'error': 'not_found',
                'message': 'Task not found'
            }), 404

        return jsonify({
            'success': True,
            'message': 'Task updated successfully',
            'data': format_response(task)
        }), 200

    except ValueError as e:
        return jsonify({
            'success': False,
            'error': 'invalid_data',
            'message': str(e)
        }), 400

@task_routes_bp.route('/<int:task_id>/status', methods=['PATCH'])
def update_task_status(task_id):
    """Update task status"""
    try:
        data = request.json
        if not data or 'status' not in data:
            return jsonify({
                'success': False,
                'error': 'missing_status',
                'message': 'Status is required'
            }), 400

        task = task_controller.update_task_status(task_id, data['status'])
        if not task:
            return jsonify({
                'success': False,
                'error': 'not_found',
                'message': 'Task not found'
            }), 404

        return jsonify({
            'success': True,
            'message': 'Task status updated successfully',
            'data': format_response(task)
        }), 200

    except ValueError as e:
        return jsonify({
            'success': False,
            'error': 'invalid_data',
            'message': str(e)
        }), 400

@task_routes_bp.route('/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task by ID"""
    try:
        success = task_controller.delete_task(task_id)
        if not success:
            return jsonify({
                'success': False,
                'error': 'not_found',
                'message': 'Task not found'
            }), 404

        return jsonify({
            'success': True,
            'message': 'Task deleted successfully'
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'server_error',
            'message': str(e)
        }), 500

@task_routes_bp.route('/search', methods=['GET'])
def search_tasks():
    """Search tasks by title"""
    try:
        search_term = request.args.get('q')
        user_id = request.args.get('user_id')

        if not search_term or not user_id:
            return jsonify({
                'success': False,
                'error': 'missing_parameters',
                'message': 'Search term (q) and user_id are required'
            }), 400

        tasks = task_controller.search_tasks_by_title(user_id, search_term)
        
        return jsonify({
            'success': True,
            'data': format_response(tasks)
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'server_error',
            'message': str(e)
        }), 500
    
@task_routes_bp.route('/user/<user_id>/to_reschedule', methods=['GET'])
def get_tasks_to_reschedule(user_id):
    """Get all tasks for a user that need rescheduling (not scheduled)"""
    try:
        tasks = task_controller.get_user_tasks(user_id)
        # Filter tasks: to_reschedule is True and is_scheduled is False
        filtered_tasks = [
            t for t in tasks
            if getattr(t, 'is_scheduled', False)
        ]
        return jsonify({
            'success': True,
            'data': format_response(filtered_tasks)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'server_error',
            'message': str(e)
        }), 500