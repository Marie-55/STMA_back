from flask import Blueprint, request, jsonify
import src.controllers.session_controller  as session 
from datetime import datetime
from src.utils.util_func import model_to_dict


session_routes = Blueprint("/session", __name__)
#write
@session_routes.route("/write/add", methods=["POST"])
def add_session():
    data = request.json
    sess = session.create_session(
        datetime.strptime(data.get("date"), "%Y-%m-%d"),
        data.get("start_time"),
        data.get("task_id")
    )
    if sess:
        return jsonify({"message": "Session added successfully", "session": model_to_dict(sess)}), 201
    else:
        return jsonify({"message": "Session is not added", "session": "empty"}), 404
    

#read
@session_routes.route("/read/all", methods=["GET"])
def fetch_all_sessions():
    sess = session.get_all_sessions()
    print(sess)
    if sess:
        sess= [model_to_dict(s) for s in sess]
        return jsonify({"message": "Sessions fetched successfully", "session": sess}), 200
    else:
        return jsonify({"message": "Sessions not found", "session": "empty"}), 404
    

@session_routes.route("/read/<int:sess_id>", methods=["GET"])
def fetch_session(sess_id):
    sess = session.get_session(sess_id[0])
    if sess:
        return jsonify({"message": "Session fetched successfully", "session": model_to_dict(sess)}), 200
    else:
        return jsonify({"message": "Session not found", "session": "empty"}), 404
    
   
@session_routes.route("/read/details/<int:sess_id>", methods=["GET"])
def fetch_session_details(sess_id):
    sess = session.get_session_details(sess_id)
    if sess:
        return jsonify({"message": "Session details fetched successfully", "session": model_to_dict(sess)}), 200
    else:
        return jsonify({"message": "Session not found", "session": "empty"}), 404

#update
@session_routes.route("/update/<int:sess_id>/<int:task_id>", methods=["PATCH"])
def update_session_task(sess_id,task_id):
    sess = session.update_session_task(sess_id,task_id)
    if sess:
        return jsonify({"message": "Session Updated successfully", "session": model_to_dict(sess)}), 200
    else:
        return jsonify({"message": "Session not found", "session": "empty"}), 404

#delete
@session_routes.route("/delete/<int:sess_id>", methods=["DELETE"])
def delete_session(sess_id):
    sess = session.delete_session(sess_id)
    if sess:
        return jsonify({"message": "Session deleted successfully", "session": model_to_dict(sess)}), 200
    else:
        return jsonify({"message": "Session not found", "session": "empty"}), 404
    
@session_routes.route("/delete/all", methods=["DELETE"])
def delete_all_sessions(sess_id):
    sess = session.delete_all_sessions(sess_id)
    if sess:
        return jsonify({"message": "Sessions deleted successfully", "session": model_to_dict(sess)}), 200
    else:
        return jsonify({"message": "Session not found", "session": "empty"}), 404
    
    
