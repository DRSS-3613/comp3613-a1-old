from flask import (
    Blueprint,
    render_template,
    jsonify,
    request,
    send_from_directory,
    session,
)
from flask_jwt import jwt_required, current_identity


from App.controllers import (
    authenticate,
    login_user,
    logout_user,
    create_reviewer,
    create_admin,
    get_reviewer_by_id,
    get_admin_by_id,
    get_all_admins_json,
    get_all_reviewers_json,
    get_all_users,
    get_all_users_json,
)

user_views = Blueprint("user_views", __name__, template_folder="../templates")


@user_views.route("/static/users")
def static_user_page():
    return send_from_directory("static", "static-user.html")


@user_views.route("/users", methods=["GET"])
def get_user_page():
    users = get_all_users()
    return render_template("users.html", users=users)


@user_views.route("/api/users")
def client_app():
    users = get_all_users_json()
    return jsonify(users)


@user_views.route("/api/users", methods=["POST"])
def signup():
    data = request.get_json()
    if data["type"] == "reviewer":
        user = create_reviewer(data["username"], data["password"])
    elif data["type"] == "admin":
        user = create_admin(data["username"], data["password"])
    else:
        return jsonify({"error": "Invalid user type"}), 400
    if user:
        return jsonify({"message": "User created"}), 201
    return jsonify({"error": "User not created"}), 400


@user_views.route("/identify", methods=["GET"])
@jwt_required()
def identify_user_action():
    return jsonify(
        {
            "message": f"username: {current_identity.username}, id : {current_identity.id}"
        }
    )


@user_views.route("/auth", methods=["POST"])
def login():
    data = request.get_json()
    user = authenticate(username=data["username"], password=["password"])
    if user is not None:
        login_user(user)
        return jsonify({"message": "User logged in"}), 200
    return jsonify({"error": "Invalid username or password"}), 400


@user_views.route("/users/logout", methods=["POST"])
def logout():
    logout_user()
    return jsonify({"message": "User logged out"})


@user_views.route("/api/users/<id>", methods=["GET"])
@jwt_required()
def get_user_by_id(id):
    if not current_identity.is_admin():
        return jsonify({"error": "Unauthorized"}), 401
    user = get_reviewer_by_id(id)
    if not user:
        user = get_admin_by_id(id)
    if user:
        return jsonify(user.to_json())
    return jsonify({"error": "User not found"}), 404


@user_views.route("/api/users/<id>", methods=["DELETE"])
@jwt_required()
def delete_user_by_id(id):
    if not current_identity.is_admin():
        return jsonify({"error": "Unauthorized"}), 401
    user = get_reviewer_by_id(id)
    if not user:
        user = get_admin_by_id(id)
    if user:
        user.delete()
        return jsonify({"message": "User deleted"}), 200
    return jsonify({"error": "User not found"}), 404


@user_views.route("/api/users")
@jwt_required()
def get_all_users_route():
    if not current_identity.is_admin():
        return jsonify({"error": "Unauthorized"}), 401
    users = get_all_users_json()
    return jsonify(users)


@user_views.route("/admins", methods=["GET"])
@jwt_required()
def get_all_admins_route():
    if not current_identity.is_admin():
        return jsonify({"error": "Unauthorized"}), 401
    admins = get_all_admins_json()
    return jsonify(admins)


@user_views.route("/reviewers", methods=["GET"])
@jwt_required()
def get_all_reviewers_route():
    if not current_identity.is_admin():
        return jsonify({"error": "Unauthorized"}), 401
    reviewers = get_all_reviewers_json()
    return jsonify(reviewers)
