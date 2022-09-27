from App.database import db


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String, nullable=False)
    faculty = db.Column(db.String, nullable=True)
    programme = db.Column(db.String, nullable=True)
    karma = db.Column(db.Integer, nullable=False)

    def __init__(self, name, student_id):
        self.name = name
        self.student_id = student_id
        self.karma = 0

    def to_json(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'name': self.name,
            'faculty': self.faculty,
            'programme': self.programme,
            'karma': self.karma
        }
