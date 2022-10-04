from App.database import db


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"), nullable=False)
    text = db.Column(db.String, nullable=False)
    num_upvotes = db.Column(db.Integer, nullable=True)
    num_downvotes = db.Column(db.Integer, nullable=True)

    def __init(self, student_id, text):
        self.student_id = student_id
        self.text = text
        self.num_upvotes = 0
        self.num_downvotes = 0

    def upvote(self):
        self.num_upvotes += 1

    def downvote(self):
        self.num_downvotes += 1

    def to_json(self):
        return {
            "id": self.id,
            "student_id": self.student_id,
            "text": self.text,
            "num_upvotes": self.num_upvotes,
            "num_downvotes": self.num_downvotes,
        }
