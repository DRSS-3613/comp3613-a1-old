from App.database import db


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reviewer_id = db.Column(db.Integer, db.ForeignKey("reviewer.id"), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"), nullable=False)
    text = db.Column(db.String, nullable=False)
    num_upvotes = db.Column(db.Integer, nullable=True)
    num_downvotes = db.Column(db.Integer, nullable=True)

    def __init__(self, student_id, user_id, text):
        self.student_id = student_id
        self.reviewer_id = user_id
        self.text = text

    def set_defaults(self):
        self.num_downvotes = 0
        self.num_upvotes = 0

    def upvote(self):
        self.num_upvotes += 1

    def downvote(self):
        self.num_downvotes += 1

    def get_karma(self):
        return self.num_upvotes - self.num_downvotes

    def to_json(self):
        return {
            "id": self.id,
            "student_id": self.student_id,
            "reviewer_id": self.reviewer_id,
            "text": self.text,
            "num_upvotes": self.num_upvotes,
            "num_downvotes": self.num_downvotes,
        }
