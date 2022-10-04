from App.database import db


class Review(db.model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"), nullable=False)
    text = db.Column(db.String, nullable=False)
    num_upvotes = db.Column(db.Integer, nullable=False)
    num_downvotes = db.Column(db.Integer, nullable=False)

    def __init(self, student_id, text):
        self.student_id = student_id
        self.num_upvotes = 0
        self.num_downvotes = 0
        self.text = text

    def upvote(self):
        self.num_upvotes += 1

    def downvote(self):
        self.num_downvotes += 1
