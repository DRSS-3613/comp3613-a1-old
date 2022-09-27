from App.models import Student
from App.database import db


def create_student(name, student_id):
    new_student = Student(name=name, student_id=student_id)
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
