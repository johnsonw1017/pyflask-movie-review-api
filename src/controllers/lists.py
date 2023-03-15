from flask import Blueprint, jsonify, request, abort
from main import db
from models import List, User, Movie
from schemas import list_schema, lists_schema
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

lists = Blueprint("lists", __name__)

#get 10 most recent lists created by anyone
@lists.route("/lists", methods=["GET"])
def get_lists():
  
  lists = List.query.filter_by(private=False).order_by(List.post_date.desc()).limit(10)

  return jsonify(lists_schema.dump(lists))

#get lists from users profile (10 most recent)
@lists.route("/profile/<int:user_id>/lists", methods=["GET"])
@jwt_required()
def get_lists_profile(user_id):
  access_user_id = int(get_jwt_identity())
  access_user = User.query.get(access_user_id)

  #check if user is in database
  if not access_user:
    return abort(401, description="Invalid user")

  if access_user_id == user_id or access_user.admin:
    lists = List.query.filter_by(user_id=user_id).order_by(List.post_date.desc()).limit(10)
  else:
    lists = List.query.filter_by(user_id=user_id, private=False).order_by(List.post_date.desc()).limit(10)

  return jsonify(lists_schema.dump(lists))

#get individual lists
@lists.route("/lists/<int:list_id>", methods=["GET"])
@jwt_required()
def get_list(list_id):
  access_user_id = int(get_jwt_identity())
  access_user = User.query.get(access_user_id)

  #check if user is in database
  if not access_user:
    return abort(401, description="Invalid user")

  list = List.query.filter_by(id=list_id).first()

  if (not list.private) or (list.private and (access_user_id == list.user_id or access_user.admin)):
    return jsonify(list_schema.dump(list))
  else:
    return abort(401, description="You do not have the required permissions to perform this action")


#post a list
@lists.route("/lists", methods=["POST"])
@jwt_required()
def create_list():
  list_fields = list_schema.load(request.json)

  #user_id from jwt
  user_id = get_jwt_identity()

  new_list = List()
  new_list.title = list_fields["title"]
  new_list.comment = list_fields["comment"]
  new_list.private = list_fields["private"]
  new_list.user_id = user_id
  new_list.post_date = datetime.now()

  movies = list_fields["movies"]

  for movie_object in movies:
    #check if movie_id exist in database before appending to the list
    movie_id = movie_object["id"]
    movie = Movie.query.filter_by(id=movie_id).first()
    if movie:
      new_list.movies.append(movie)

  # add to the database and commit
  db.session.add(new_list)
  db.session.commit()

  return jsonify(list_schema.dump(new_list))

#delete list
@lists.route("/lists/<int:list_id>", methods=["DELETE"])
@jwt_required()
def delete_list(list_id):
  user_id  = get_jwt_identity()
  user = User.query.get(user_id)

  #check if user is in database
  if not user:
    return abort(401, description="Invalid user")
  
  list = list.query.filter_by(id=list_id).first()

  #check if list is in database
  if not list:
    return abort(400, description= "list does not exist")
  
  #check if user is authorised either the list maker or an admin user
  if not (user.admin or user_id == str(list.user_id)):
    return abort(401, description= "You do not have the required permissions to perform this action")
  
  db.session.delete(list)
  db.session.commit()

  return jsonify(list_schema.dump(list))

@lists.route("/lists/<int:list_id>", methods=["PUT"])
@jwt_required()
def update_list(list_id):
  user_id  = get_jwt_identity()
  user = User.query.get(user_id)

  #check if user is in database
  if not user:
    return abort(401, description="Invalid user")
  
  list = List.query.filter_by(id=list_id).first()

  #check if list is in database
  if not list:
    return abort(400, description= "list does not exist")
  
  #check if user is authorised either the list maker or an admin user
  if not (user.admin or user_id == str(list.user_id)):
    return abort(401, description= "You do not have the required permissions to perform this action")
  
  list_fields = list_schema.load(request.json)
  
  #only these following fields can be updated/edited, rest will remain the same
  list.title = list_fields["title"]
  list.comment = list_fields["comment"]
  list.private = list_fields["private"]

  #empty movies before adding
  list.movies = []

  movies = list_fields["movies"]

  for movie_object in movies:
    #check if movie_id exist in database before appending to the list
    movie_id = movie_object["id"]
    movie = Movie.query.filter_by(id=movie_id).first()
    if movie:
      list.movies.append(movie)

  db.session.commit()

  return jsonify(list_schema.dump(list))