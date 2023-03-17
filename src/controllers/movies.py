from flask import Blueprint, jsonify, request, abort
from main import db
from models import User, Movie, Review
from schemas import movie_schema, movies_schema
from flask_jwt_extended import jwt_required, get_jwt_identity

movies = Blueprint("movies", __name__)

#get top 10 highest rate movies
@movies.route("/top-ten-movies", methods=["GET"])
def get_top_movies():
  
  #perform join and group-by clause
  top_movies = db.session.query(Movie, db.func.avg(Review.rating).label('avg_rating')) \
                    .join(Review, Movie.id == Review.movie_id) \
                    .group_by(Movie.id) \
                    .order_by(db.desc('avg_rating')) \
                    .limit(10) 
  
  #append results all together
  result = []

  for movie, avg_rating in top_movies:
    movie_data = movie_schema.dump(movie)
    movie_data['avg_rating'] = avg_rating
    result.append(movie_data)

  return jsonify(result)


#get 100 of the most recent movies
@movies.route("/recent-movies", methods=["GET"])
def get_recent_movies():
  
  recent_movies_list = Movie.query\
                      .order_by(Movie.release_date.desc())\
                      .limit(100)
  result = movies_schema.dump(recent_movies_list)

  return jsonify(result)

#get movie by id
@movies.route("/movies/<int:id>", methods=["GET"])
def get_movie(id):
  
  movie = Movie.query.filter_by(id=id).first()
  result = movie_schema.dump(movie)

  return jsonify(result)

#movie title search
@movies.route("/movies/search", methods=["GET"])
def search_movie():

  movies_list = [] #in case multiple movies have the same name
  movies_list = Movie.query.filter_by(title=request.args.get("title"))
  result = movies_schema.dump(movies_list)

  return jsonify(result)

#delete movie, admin user only action
@movies.route("/movies/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_movie(id):
  user_id  = get_jwt_identity()
  user = User.query.get(user_id)

  #check if user is in database
  if not user:
    return abort(401, description="Invalid user")
  
  movie = Movie.query.filter_by(id=id).first()

  #check if movie is in database
  if not movie:
    return abort(400, description= "Movie does not exist")
  
  #check if user is admin
  if not user.admin:
    return abort(401, description= "You do not have the required permissions to perform this action")
  
  db.session.delete(movie)
  db.session.commit()

@movies.route("/movies/<int:id>", methods=["PUT"])
@jwt_required()
def update_movie(id):
  user_id  = get_jwt_identity()
  user = User.query.get(user_id)

  #check if user is in database
  if not user:
    return abort(401, description="Invalid user")
  
  movie = Movie.query.filter_by(id=id).first()

  #check if movie is in database
  if not movie:
    return abort(400, description= "Movie does not exist")
  
  #check if user is admin
  if not user.admin:
    return abort(401, description= "You do not have the required permissions to perform this action")
  
  movie_fields = movie_schema.load(request.json)

  movie.title = movie_fields["title"]
  movie.description = movie_fields["description"]
  movie.runtime = movie_fields["runtime"]
  movie.release_date = movie_fields["release_date"]

  db.session.commit()

  return jsonify(movie_schema.dump(user))