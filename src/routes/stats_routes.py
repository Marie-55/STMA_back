from flask import Blueprint, request, jsonify
from src.controllers.stats_controller import (
    get_user_stats,
    update_task_stats,
    calculate_productivity_score,
    update_average_task_duration
)

stats_bp = Blueprint('stats', __name__)

@stats_bp.route('/stats/<user_id>', methods=['GET'])
def get_stats(user_id):
    stats = get_user_stats(user_id)
    if stats:
        return jsonify(stats), 200
    return jsonify({'error': 'Stats not found'}), 404

@stats_bp.route('/stats/<user_id>/task', methods=['POST'])
def update_stats(user_id):
    data = request.get_json()
    task_completed = data.get('completed', True)
    stats = update_task_stats(user_id, task_completed)
    return jsonify(stats), 200

@stats_bp.route('/stats/<user_id>/productivity', methods=['GET'])
def get_productivity_score(user_id):
    score = calculate_productivity_score(user_id)
    if score:
        return jsonify(score), 200
    return jsonify({'error': 'Productivity score not found'}), 404

@stats_bp.route('/stats/<user_id>/duration', methods=['POST'])
def update_duration(user_id):
    data = request.get_json()
    duration = data.get('duration')
    if not duration:
        return jsonify({'error': 'Duration is required'}), 400
    
    stats = update_average_task_duration(user_id, duration)
    if stats:
        return jsonify(stats), 200
    return jsonify({'error': 'Failed to update duration'}), 400