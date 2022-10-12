from flask import Blueprint, render_template, jsonify, request, send_from_directory
from flask_jwt import jwt_required


from App.controllers import (
    create_reviewer,
    create_admin,
    get_reviewer_by_id,
    get_admin_by_id,
    get_all_users,
    get_all_users_json,
)

user_views = Blueprint("user_views", __name__, template_folder="../templates")


@user_views.route("/users", methods=["GET"])
def get_user_page():
    users = get_all_users()
    return render_template("users.html", users=users)


@user_views.route("/users", methods=["POST"])
def create():
    data = request.get_json()
    if data["type"] == "reviewer":
        user = create_reviewer(data["username"], data["password"])
    elif data["type"] == "admin":
        user = create_admin(data["username"], data["password"])
    else:
        return jsonify({"error": "Invalid user type"}), 400
    if user:
        return jsonify(user.to_json())
    return jsonify({"error": "User not created"}), 400


@user_views.route("/api/users/<id>", methods=["GET"])
def get_user_by_id(id):
    user = get_reviewer_by_id(id)
    if not user:
        user = get_admin_by_id(id)
    if user:
        return jsonify(user.to_json())
    return jsonify({"error": "User not found"}), 404


@user_views.route("/api/users")
def client_app():
    users = get_all_users_json()
    return jsonify(users)


@user_views.route("/static/users")
def static_user_page():
    return send_from_directory("static", "static-user.html")
