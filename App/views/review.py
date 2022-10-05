from flask import Blueprint, jsonify, request
from pytest import param
from App.controllers import (
    create_review,
    get_all_reviews,
    get_reviews_by_student_id,
    upvote_review,
    downvote_review,
    get_review,
)

review_views = Blueprint("review_views", __name__, template_folder="../templates")


@review_views.route("/reviews", methods=["POST"])
def create():
    data = request.get_json()
    review = create_review(data["student_id"], data["user_id"], data["text"])
    if review:
        return jsonify(review), 201
    return jsonify({"error": "Review not created"}), 400


@review_views.route("/reviews", methods=["GET"])
def list():
    reviews = get_all_reviews()
    return jsonify([review.to_json() for review in reviews])


# Get review using query parameter
# How to use
# /review?student_id=816024901
# /review?id=1
@review_views.route("/review", methods=["GET"])
def get_by_id():
    args = request.args
    review = None
    if "student_id" in args:
        review = get_reviews_by_student_id(args["student_id"])
    if "id" in args:
        review = get_review(args["id"])
    if review:
        return jsonify(review)
    return jsonify({"error": "Review not found"}), 404


@review_views.route("/reviews/vote", methods=["PUT"])
def vote():
    data = request.get_json()
    if data["vote_type"] == "up":
        return jsonify(upvote_review(data["id"]))
    return jsonify(downvote_review(data["id"]))
