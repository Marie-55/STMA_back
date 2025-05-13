from flask import Blueprint, request, jsonify
import src.controllers.task_controller  as tasks 
from datetime import datetime
from src.utils.util_func import model_to_dict

task_routes = Blueprint("/tasks", __name__)


#writing routes
@task_routes.route("/write/add", methods=["POST"])
def add_task():
    data = request.json
    if data.get('is_scheduled'):
        scheduled= data.get('is_scheduled')
    else:
        scheduled= False
    if data.get('to_reschedule'):
        schedule= data.get('to_reschedule')
    else:
        schedule= False
    if data.get('is_synched'):
        synched= data.get('is_synched')
    else:
        synched= False
    if data.get('user'):
        user= data.get('user')
    else:
        user= "test@gmail.com"

    task = tasks.create_task(
        data.get("title"),
        data.get("category"),
        datetime.strptime(data.get("deadline"), "%Y-%m-%d"),
        data.get("duration"),
        data.get("priority"),
        scheduled,synched,schedule,
        user=user
    )
    return jsonify({"message": "Task added successfully","task": model_to_dict(task)}), 201


#reading
@task_routes.route("/read/all", methods=["GET"])
def fetch_tasks():
    all = tasks.get_all_tasks()
    print(all)
    if all:
        return jsonify({"message": "Tasks fetched", "tasks":[model_to_dict(task) for task in all]})
    else:
        return jsonify({"error": "Tasks not found"}), 404


@task_routes.route("/read/to_reschedule", methods=["GET"])
def fetch_tasks_to_reschedule():
    to_schedule = tasks.get_tasks_to_reschedule()
    if to_schedule:
        return jsonify({"message": "Tasks fetched", "tasks":[model_to_dict(task) for task in to_schedule]})
    else:
        return jsonify({"error": "Tasks not found"}), 404

@task_routes.route("/read/status/<int:status>", methods=["GET"])
def fetch_tasks_by_status(status):
    to_schedule = tasks.get_tasks_by_status(status=status)
    if to_schedule:
        return jsonify({"message": "Tasks fetched", "tasks":[model_to_dict(task) for task in to_schedule]})
    else:
        return jsonify({"error": "Tasks not found"}), 404


#updating
@task_routes.route("/update/status/<int:task_id>/<string:n_status>", methods=["PATCH"])
def modify_task_status(task_id,n_status):
    data = request.json
    task = tasks.update_task_status(task_id,n_status)
    if task:
        return jsonify({"message": "Task updated", "task":model_to_dict(task)}), 200
    return jsonify({"error": "Task not found"}), 404

@task_routes.route("/update/title/<int:task_id>/<string:n_title>", methods=["PATCH"])
def modify_task_title(task_id,n_title):
    data = request.json
    task = tasks.update_task_title(task_id,n_title)
    if task:
        return jsonify({"message": "Task updated", "task":model_to_dict(task)}), 200
    return jsonify({"error": "Task not found"}), 404

@task_routes.route("/update/ddl/<int:task_id>/<string:ddl>", methods=["PATCH"])
def modify_task_deadline(task_id,ddl):
    data = request.json
    task = tasks.update_task_deadline(task_id,ddl)
    if task:
        return jsonify({"message": "Task updated", "task":model_to_dict(task)}), 200
    return jsonify({"error": "Task not found"}), 404

@task_routes.route("/update/sync/<int:task_id>/<string:syn>", methods=["PATCH"])
def modify_task_syn(task_id,syn):
    data = request.json
    task = tasks.update_task_sync_status(task_id,syn)
    if task:
        return jsonify({"message": "Task updated", "task":model_to_dict(task)}), 200
    return jsonify({"error": "Task not found"}), 404


#deleting
@task_routes.route("/delete/all", methods=["DELETE"])
def delete_tasks():
    data = request.json
    task = tasks.delete_all_tasks()
    if task:
        return jsonify({"message": "Tasks Deleted", "tasks":model_to_dict(task)}), 200
    return jsonify({"edrror": "No Tasks found"}), 404

@task_routes.route("/delete/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    data = request.json
    task = tasks.delete_task(task_id=task_id)
    if task:
        return jsonify({"message": "Task Deleted", "tasks":model_to_dict(task)}), 200
    return jsonify({"edrror": "No Tasks found"}), 404

@task_routes.route("/search/<string:query>", methods=["GET"])
def search_tasks_route(query):
    matching_tasks = tasks.search_tasks(query)
    if matching_tasks:
        return jsonify({
            "message": "Tasks found",
            "tasks": [model_to_dict(task) for task in matching_tasks]
        })
    return jsonify({"message": "No tasks found matching your search"}), 404