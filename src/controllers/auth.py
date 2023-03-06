from flask import Blueprint, jsonify, request
from main import db, bcrypt
from models import User
from schemas import user_schema

auth = Blueprint('auth', __name__, url_prefix="/auth")

#POST routes endpoint
@auth.route("/register", methods=["POST"])
def auth_register():
    #The request data will be loaded in a user_schema converted to JSON. request needs to be imported from
    user_fields = user_schema.load(request.json)
    #Create the user object
    user = User()
    #Add the user_name attribute
    user.user_name = user_fields["user_name"]
    #Add the email attribute
    user.email = user_fields["email"]
    #Add the password attribute hashed by bcrypt
    user.password = bcrypt.generate_password_hash(user_fields["password"]).decode("utf-8")
    #Add it to the database and commit the changes
    db.session.add(user)
    db.session.commit()
    #Return the user to check the request was successful
    return jsonify(user_schema.dump(user))