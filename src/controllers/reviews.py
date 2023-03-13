from flask import Blueprint, jsonify, request, abort
from models import Review
from schemas import review_schema, reviews_schema
from flask_jwt_extended import JWTManager, create_access_token, jwt_required

reviews = Blueprint("reviews", __name__)

#get reviews from movie page (10 most recent)
@reviews.route("/movies/<int:movie_id>/reviews", methods=["GET"])
def get_reviews(movie_id):
  
  reviews = Review.query.filter_by(movie_id=movie_id).order_by(Review.post_date.desc()).limit(10)

  result = reviews_schema.dump(reviews)

  return jsonify(result)