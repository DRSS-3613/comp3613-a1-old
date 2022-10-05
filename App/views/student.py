from flask import Blueprint, jsonify, request


from App.controllers import (
    create_student,
    get_all_students_json,
    get_student,
    student,
)

student_views = Blueprint("student_views", __name__, template_folder="../templates")


@student_views.route("/students", methods=["POST"])
def create():
    data = request.get_json()
    return jsonify(create_student(data["name"]))

@student_views.route("/students", methods=["GET"])
def list():
    students = get_all_students_json()
    return jsonify(students)

@student_views.route("/students/<id>", methods=["GET"])
def get_by_id(id):
    student = get_student(id)
    if student:
        return jsonify(student.to_json())
    return jsonify({"error": "Student not found"}), 404

