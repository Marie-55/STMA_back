
from flask import Blueprint, request, jsonify
import src.controllers.logs_controller  as log 
from datetime import datetime

log_routes = Blueprint("log_routes", __name__)

@log_routes.route("/write/logs", methods=["POST"])
def log_activity():
    data = request.json
    log_entry = log.log_user_activity(data.get("user_id"))
    return jsonify({"message": "Log added", "log": log_entry.__dict__}), 201
