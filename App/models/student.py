from App.database import db


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String, nullable=False)
    faculty = db.Column(db.String, nullable=False)
    programme = db.Column(db.String, nullable=False)
    reviews = db.relationship(
        "Review", backref="student", lazy=True, cascade="all, delete-orphan"
    )

    def __init__(self, name, student_id, faculty, programme):
        self.name = name
        self.student_id = student_id
        self.faculty = faculty
        self.programme = programme

    def get_karma(self):
        karma = 0
        for review in self.reviews:
            karma += review.get_karma()
        return karma

    def to_json(self):
        return {
            "id": self.id,
            "student_id": self.student_id,
            "name": self.name,
            "faculty": self.faculty,
            "programme": self.programme,
            "karma": self.get_karma(),
        }
