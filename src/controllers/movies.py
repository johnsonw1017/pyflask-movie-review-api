from flask import Blueprint, jsonify, request, abort
from models import Movie
from schemas import movie_schema, movies_schema

movies = Blueprint("movies", __name__)

@movies.route("/movies", methods=["GET"])
def get_movies():
  
  #get ALL movies from database table *change for final
  recent_movies_list = Movie.query.all()
  #conversion to json format
  result = movies_schema.dump(recent_movies_list)

  return jsonify(result)

@movies.route("/movie", methods=["GET"])
def get_movie():
  
  #get ALL movies from database table *change for final
  movies_list = Movie.query.all()
  #conversion to json format
  result = movies_schema.dump(movies_list)

  return jsonify(result)