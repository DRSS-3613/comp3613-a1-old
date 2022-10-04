from App.database import db


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    faculty = db.Column(db.String, nullable=True)
    programme = db.Column(db.String, nullable=True)
    reviews = db.relationship(
        "Review", backref="student", lazy=True, cascade="all, delete-orphan"
    )

    def __init__(self, name):
        self.name = name

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "faculty": self.faculty,
            "programme": self.programme,
            "karma": self.karma,
        }
