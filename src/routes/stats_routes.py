
from flask import Blueprint, request, jsonify
import src.controllers.stats_controller  as stat 
from datetime import datetime

stat_routes = Blueprint("stats_routes", __name__)


@stat_routes.route("/stats", methods=["PATCH"])
def update_stats():
    data = request.json
    stats = stat.update_user_stats(data.get("user_id"), data.get("missed_tasks"), data.get("completed_tasks"))
    return jsonify({"message": "Stats updated", "stats": stats.__dict__}), 200

