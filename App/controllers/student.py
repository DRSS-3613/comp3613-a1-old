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


def get_user_by_student_id(student_id):
    return Student.query.filter_by(student_id=student_id).first()


def get_student(id):
    return Student.query.get(id)


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
        return None
    reviews = [review.to_json() for review in student.reviews]
    return reviews


def update_student(id, student_id, name, programme, faculty):
    student = Student.query.get(id)
    if student:
        student.student_id = student_id
        student.programme = programme
        student.faculty = faculty
        student.name = name
        db.session.add(student)
        db.session.commit()
        return jsonify({"success": "Student updated"})
    return jsonify({"error": "Student not found"}), 404
