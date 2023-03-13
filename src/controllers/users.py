from flask import Blueprint, jsonify
from models import User
from schemas import user_schema

users = Blueprint('users', __name__)

@users.route("/profile/<int:id>", methods=["GET"])
def get_user(id):

  user = User.query.filter_by(id=id).first()
  
  return jsonify({"name": user.name, "email": user.email, "join_date": user.join_date})