from flask import Blueprint, jsonify, abort, request
from models import User
from main import db, bcrypt
from schemas import user_schema
from flask_jwt_extended import jwt_required, get_jwt_identity

users = Blueprint('users', __name__)

#user profile
@users.route("/profile/<int:id>", methods=["GET"])
def get_user(id):

  user = User.query.filter_by(id=id).first()
  
  return jsonify(user_schema.dump(user))

@users.route("/profile/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_user(id):
  access_user_id  = get_jwt_identity()
  user = User.query.filter_by(id=id).first()

  #check if user is in database
  if not user:
    return abort(401, description="Invalid user")
  
  #check if user is admin or user is the same as admin user
  if not (user.admin or access_user_id == str(id)):
    return abort(401, description= "You do not have the required permissions to perform this action")
  
  db.session.delete(user)
  db.session.commit()

@users.route("/profile/<int:id>", methods=["PUT"])
@jwt_required()
def update_user(id):
  access_user_id  = get_jwt_identity()
  user = User.query.filter_by(id=id).first()

  #check if user is in database
  if not user:
    return abort(401, description="Invalid user")
  
  #check if user is admin or the actual user themselves
  if not (user.admin or access_user_id == str(id)):
    return abort(401, description= "You do not have the required permissions to perform this action")
  
  user_fields = user_schema.load(request.json)
  
  #only these following fields can be updated/edited, rest will remain the same
  user.email = user_fields["email"]
  user.name = user_fields["name"]
  user.password = bcrypt.generate_password_hash(user_fields["password"]).decode("utf-8")

  db.session.commit()

  return jsonify(user_schema.dump(user))