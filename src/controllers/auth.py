from flask import Blueprint, jsonify, request, abort
from main import db, bcrypt
from models import User
from schemas import user_schema, users_schema
from datetime import date, timedelta
from flask_jwt_extended import create_access_token

auth = Blueprint('auth', __name__, url_prefix="/auth")

@auth.route("/register", methods=["POST"])
def auth_register():
  #request data loaded in user_schema
  user_fields = user_schema.load(request.json)

  #check if the email exists
  user = User.query.filter_by(email=user_fields["email"]).first()

  if user:
    return abort(400, description="Email already registered")

  user = User()
  user.name = user_fields["name"]
  user.email = user_fields["email"]
  user.password = bcrypt.generate_password_hash(user_fields["password"]).decode("utf-8")
  user.admin = False
  user.join_date = date.today()

  #add to database and commit change
  db.session.add(user)
  db.session.commit()
  #create access token with 1 day expiry
  expiry = timedelta(days=1)
  access_token = create_access_token(identity=str(user.id), expires_delta=expiry)
    
  return jsonify({"name": user.name, "token": access_token})

@auth.route("/login", methods=["POST"])
def auth_login():
    #get the user data from the request
    user_fields = user_schema.load(request.json)

    #check if email exists
    user = User.query.filter_by(email=user_fields["email"]).first()

    # error if user not exist or password incorrect
    if not user or not bcrypt.check_password_hash(user.password, user_fields["password"]):
        return abort(401, description="Incorrect username or password")
    
    #create access token with 1 day expiry
    expiry = timedelta(days=1)
    access_token = create_access_token(identity=str(user.id), expires_delta=expiry)
    
    return jsonify({"name": user.name, "token": access_token})