from flask import Blueprint, jsonify, request
from main import db
from models import User

users = Blueprint('users', __name__, url_prefix="/profile")

#GET routes endpoint
@users.route("/", methods=["GET"])
def get_user():

    return "User profile retrieved"

#POST routes endpoint
@users.route("/", methods=["POST"])
def create_user():

    return "User registered"

#DELETE routes endpoint
@users.route("/<int:id>/", methods=["DELETE"])
def delete_card(id):

    return "User deleted"