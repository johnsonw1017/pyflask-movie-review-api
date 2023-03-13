from flask import Blueprint, jsonify, request, abort
from models import Movie
from schemas import movie_schema, movies_schema

movies = Blueprint("movies", __name__)

#get top 10 highest rate movies
@movies.route("/top-ten-movies", methods=["GET"])
def get_top10_movies():
  
  #get top 10 movies based on average rating (need to join average rating)
  top10_movies_list = Movie.query.limit(10)
  result = movies_schema.dump(top10_movies_list)

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