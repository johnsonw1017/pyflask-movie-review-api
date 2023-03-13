from flask import Blueprint, jsonify, request, abort
from main import db
from models import Review, User
from schemas import review_schema, reviews_schema
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import datetime

reviews = Blueprint("reviews", __name__)

#get reviews from movie page (10 most recent)
@reviews.route("/movies/<int:movie_id>/reviews", methods=["GET"])
def get_reviews_movie(movie_id):
  
  reviews = Review.query.filter_by(movie_id=movie_id).order_by(Review.post_date.desc()).limit(10)

  result = reviews_schema.dump(reviews)

  return jsonify(result)

#get reviews from users profile (10 most recent)
@reviews.route("/profile/<int:user_id>/reviews", methods=["GET"])
def get_reviews_profile(user_id):
  
  reviews = Review.query.filter_by(user_id=user_id).order_by(Review.post_date.desc()).limit(10)

  result = reviews_schema.dump(reviews)

  return jsonify(result)

#get individual reviews
@reviews.route("/reviews/<int:review_id>", methods=["GET"])
def get_review(review_id):
  
  review = Review.query.filter_by(id=review_id).first()

  result = review_schema.dump(review)

  return jsonify(result)

#post a review for a movie
@reviews.route("/movies/<int:movie_id>/reviews", methods=["POST"])
@jwt_required()
def create_review(movie_id):
  review_fields = review_schema.load(request.json)

  #user_id from jwt
  user_id = get_jwt_identity()
  
  #check if a review already exist for the movie
  review = Review.query.filter_by(user_id=user_id, movie_id=movie_id).count()
  if review > 0:
    return abort(409, description= "Duplication error, review by user alreay exists for this movie")

  new_review = Review()
  new_review.title = review_fields["title"]
  new_review.comment = review_fields["comment"]
  new_review.user_id = user_id
  new_review.movie_id = movie_id

  user_rating = review_fields["rating"]

  #check if user rating is between 0 and 10
  if user_rating in range(0,11):
    new_review.rating = user_rating
  else:
    abort(400, description="Please provide a rating from 0 to 10")

  new_review.post_date = datetime.now()

  # add to the database and commit
  db.session.add(new_review)
  db.session.commit()
  result = review_schema.dump(new_review)

  return jsonify(result)

#delete review
@reviews.route("/reviews/<int:review_id>", methods=["DELETE"])
@jwt_required()
def delete_review(review_id):
  user_id  = get_jwt_identity()
  user = User.query.get(user_id)

  #check if user is in database
  if not user:
    return abort(401, description="Invalid user")
  
  review = Review.query.filter_by(id=review_id).first()

  #check if review is in database
  if not review:
    return abort(400, description= "Review does not exist")
  
  #check if user is authorised either the reviewer or an admin user
  if not (user.admin or user_id == str(review.user_id)):
    return abort(401, description= "You do not have the required permissions to perform this action")
  
  db.session.delete(review)
  db.session.commit()
  result = review_schema.dump(review)

  return jsonify(result)