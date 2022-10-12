from App.database import db
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.mutable import MutableDict


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reviewer_id = db.Column(db.Integer, db.ForeignKey("reviewer.id"), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"), nullable=False)
    text = db.Column(db.String, nullable=False)
    votes = db.Column(MutableDict.as_mutable(JSON), nullable=True)

    def __init__(self, student_id, user_id, text):
        self.student_id = student_id
        self.reviewer_id = user_id
        self.text = text
        self.votes = {"num_upvotes": 0, "num_downvotes": 0}

    def vote(self, voter_id, vote): # this is fucked
        self.votes.update({voter_id: vote})
        self.votes.update({"num_upvotes": len([vote for vote in self.votes.values() if vote == "up"])})
        self.votes.update({"num_downvotes": len([vote for vote in self.votes.values() if vote == "down"])})

    def get_num_upvotes(self):
        return self.votes["num_upvotes"]

    def get_num_downvotes(self):
        return self.votes["num_downvotes"]

    def get_karma(self):
        return self.get_num_upvotes() - self.get_num_downvotes()

    def get_votes(self):
        return self.votes

    def to_json(self):
        return {
            "id": self.id,
            "student_id": self.student_id,
            "reviewer_id": self.reviewer_id,
            "text": self.text,
            "num_upvotes": self.get_num_upvotes(),
            "num_downvotes": self.get_num_downvotes(),
            "karma": self.get_karma(),
        }
