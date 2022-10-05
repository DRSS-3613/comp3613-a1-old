from flask import Blueprint, jsonify, request


from App.controllers import (
    create_student,
    get_all_students_json,
    get_student,
    get_user_by_student_id,
    update_student,
    get_all_students_reviews,
)

student_views = Blueprint("student_views", __name__, template_folder="../templates")

@student_views.route("/students", methods=["POST"])
def create():
    data = request.get_json()
    student = create_student(data["student_id"], data["name"], data["programme"], data["faculty"])
    if student:
        return jsonify(student.to_json())
    return jsonify({"error": "Student not created"}), 400

@student_views.route("/students", methods=["GET"])
def list():
    students = get_all_students_json()
    return jsonify(students)


#Get student using query parameter
#How to use
#/student?student_id=816024901
#/student?id=1
@student_views.route("/student", methods=["GET"])
def get_by_id():
    args = request.args
    student = None
    if "student_id" in args:
        student = get_user_by_student_id(args["student_id"])
    if "id" in args:
        student = get_student(args["id"])
    if student:
        return jsonify(student.to_json())
    return jsonify({"error": "Student not found"}), 404

@student_views.route("/students/<id>", methods=["PUT"])
def update(id):
    data = request.get_json()
    return update_student(id, data["student_id"], data["name"], data["programme"], data["faculty"])

@student_views.route("/students/reviews/<id>", methods=["GET"])
def list_student_reviews(id):
    reviews = get_all_students_reviews(id)
    if reviews:
        return jsonify(reviews)
    return jsonify({"error": "Student not found"}), 404
