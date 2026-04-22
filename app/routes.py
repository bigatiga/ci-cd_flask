from flask import Blueprint, jsonify, request, send_from_directory
import os
from . import storage

tasks_bp = Blueprint("tasks", __name__)


@tasks_bp.route("/")
def index():
    static_dir = os.path.join(os.path.dirname(__file__), "..", "static")
    return send_from_directory(os.path.abspath(static_dir), "index.html")


@tasks_bp.route("/api/tasks", methods=["GET"])
def list_tasks():
    return jsonify(storage.get_all()), 200


@tasks_bp.route("/api/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = storage.get_by_id(task_id)
    if task is None:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(task), 200


@tasks_bp.route("/api/tasks", methods=["POST"])
def create_task():
    data = request.get_json(silent=True) or {}
    try:
        task = storage.create(
            title=data.get("title", ""),
            description=data.get("description", ""),
        )
        return jsonify(task), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@tasks_bp.route("/api/tasks/<int:task_id>", methods=["PATCH"])
def update_task(task_id):
    data = request.get_json(silent=True) or {}
    try:
        task = storage.update(task_id, data)
        return jsonify(task), 200
    except KeyError:
        return jsonify({"error": "Task not found"}), 404
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@tasks_bp.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    try:
        storage.delete(task_id)
        return "", 204
    except KeyError:
        return jsonify({"error": "Task not found"}), 404


@tasks_bp.route("/health")
def health():
    return jsonify({"status": "ok"}), 200
