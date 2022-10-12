from flask import jsonify
from App.models import Student
from App.database import db


def create_student(student_id, name, programme, faculty):
    new_student = Student(
        student_id=student_id, name=name, programme=programme, faculty=faculty
    )
    db.session.add(new_student)
    db.session.commit()
    return new_student


def get_student(id):
    return Student.query.get(id)


def get_student_by_student_id(student_id):
    return Student.query.filter_by(student_id=student_id).first()


def get_all_students():
    return Student.query.all()


def get_all_students_json():
    students = Student.query.all()
    if not students:
        return []
    students = [student.to_json() for student in students]
    return students


def get_all_students_reviews(id):
    student = Student.query.get(id)
    if not student:
        return {"error": "Student not found"}, 404
    reviews = [review.to_json() for review in student.reviews]
    return reviews, 200


def update_student(id, student_id=None, name=None, programme=None, faculty=None):
    student = Student.query.get(id)
    if student:
        if student_id:
            student.student_id = student_id
        if name:
            student.name = name
        if programme:
            student.programme = programme
        if faculty:
            student.faculty = faculty
        db.session.add(student)
        db.session.commit()
        return jsonify({"success": "Student updated"})
    return jsonify({"error": "Student not found"}), 404


def delete_student(id):
    student = Student.query.get(id)
    if student:
        db.session.delete(student)
        db.session.commit()
        return {"success": "Student deleted"}, 200
    return {"error": "Student not found"}, 404
