from flask import jsonify
from App.models import Review, Student
from App.database import db
from App.models.user import Reviewer

#Interesting Block of code
def create_review(student_id, user_id, text):
    print("Creating review", student_id, user_id, text)
    reviewer = Reviewer.query.get(user_id)
    student = Student.query.get(student_id)
    new_review = None 
    if reviewer and student:
        new_review = Review(student_id=student_id, user_id=user_id, text=text)
        new_review.set_defaults()
    if new_review == None:
        return None
    db.session.add(new_review)
    db.session.commit()

    reviewer.reviews.append(new_review)
    student.reviews.append(new_review)
    db.session.add(reviewer)
    db.session.add(student)
    db.session.commit()
    return new_review.to_json()

def get_review(id):
    return Review.query.get(id)


def get_all_reviews():
    return Review.query.all()


def get_reviews_by_student_id(student_id):
    reviews = Review.query.filter_by(student_id=student_id)
    if reviews:
        return [review.to_json() for review in reviews]
    return None

def get_reviews_by_user_id(user_id):
    reviews = Reviewer.query.get(user_id).reviews
    if reviews:
        return [review.to_json() for review in reviews]
    return None

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
