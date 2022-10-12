from App.models import Review, Student
from App.database import db
from App.models.user import Reviewer


# Interesting Block of code
def create_review(student_id, user_id, text):
    print("Creating review", student_id, user_id, text)
    reviewer = Reviewer.query.get(user_id)
    student = Student.query.get(student_id)
    new_review = None
    if reviewer and student:
        new_review = Review(student_id=student_id, user_id=user_id, text=text)
    if new_review is None:
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


def get_review_by_json(id):
    review = get_review(id)
    if review:
        return review.to_json()
    return None


def get_all_reviews():
    reviews = Review.query.all()
    if reviews:
        return [review.to_json() for review in reviews]
    return None


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


def upvote_review(id, voter_id):
    review = get_review(id)
    reviewer = Reviewer.query.get(voter_id)
    if not reviewer:
        return {"error": "Reviewer not found"}, 404
    if review:
        review.vote(voter_id, "up")
        db.session.add(review)
        return db.session.commit(), 200
    return None


def downvote_review(id, voter_id):
    review = get_review(id)
    reviewer = Reviewer.query.get(voter_id)
    if not reviewer:
        return {"error": "Reviewer not found"}, 404
    if review:
        review.vote(voter_id, "down")
        db.session.add(review)
        return db.session.commit(), 200
    return None


def get_review_votes(id):
    review = get_review(id)
    if review:
        return review.get_votes()
    return None


def get_review_karma(id):
    review = get_review(id)
    if review:
        return review.get_karma()
    return None


def delete_review(id):
    review = get_review(id)
    if review:
        db.session.delete(review)
        return db.session.commit(), 200
    return {"error": "Review not found"}, 404


def update_review(id, text):
    review = get_review(id)
    if review:
        review.text = text
        db.session.add(review)
        return db.session.commit(), 200
    return {"error": "Review not found"}, 404
