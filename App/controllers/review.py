from App.models import Review
from App.database import db


def create_review(student_id, text):
    new_review = Review(student_id=student_id, text=text)
    db.session.add(new_review)
    db.session.commit()
    return new_review


def get_review(id):
    return Review.query.get(id)


def get_all_reviews():
    return Review.query.all()


def get_reviews_by_student_id(student_id):
    return Review.query.filter_by(student_id=student_id)


def upvote_review(id):
    review = get_review(id)
    if review:
        review.upvote()
        db.session.add(review)
        return db.session.commit()
    return None


def downvote_review(id):
    review = get_review(id)
    if review:
        review.downvote()
        db.session.add(review)
        return db.session.commit()
    return None
