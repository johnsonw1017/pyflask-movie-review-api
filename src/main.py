from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow.validate import Length
from flask_bcrypt import Bcrypt
from datetime import date, timedelta
from flask_jwt_extended import JWTManager, create_access_token

def create_app():
  app = Flask(__name__)
  # configure from config.py  
  app.config.from_object("config.app_config")
  db = SQLAlchemy(app)
  return app

ma = Marshmallow(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

#database object


#create database object Movie

class Movie(db.Model):
  #table name of db
  __tablename__ = "MOVIES"

  #primary key
  id = db.Column(db.Integer, primary_key=True)

  #other attributes
  title = db.Column(db.String())
  description = db.Column(db.String())
  release_date = db.Column(db.Date())
  run_time = db.Column(db.Integer())
  #genre = db.Column(db.String()) #depends whether can integrate from csv

class MovieSchema(ma.Schema):
  class Meta:
    #fields that would be exposed
    fields = ("title", "description", "release_date", "run_time")

#for one card retrieval 
movie_schema = MovieSchema()

#for multiple cards retrieval
movies_schema = MovieSchema(many=True)

class User(db.Model):
  __tablename__ = "USERS"

  #primary key
  id = db.Column(db.Integer, primary_key=True)

  #other attributes
  name = db.Column(db.String())
  email = db.Column(db.String(), nullable=False, unique=True)
  password = db.Column(db.String(), nullable=False)
  admin = db.Column(db.Boolean(), default=False)
  join_date = db.Column(db.Date())

class UserSchema(ma.SQLAlchemyAutoSchema):
  class Meta:
    model = User
  #validate password length  
  password = ma.String(validate=Length(min=6))
    
#for one card retrieval 
user_schema = UserSchema()

#for multiple cards retrieval
users_schema = UserSchema(many=True)

#cli commands for the app
@app.cli.command("create")
def create_db():
  db.create_all()
  print("Table created")

@app.cli.command("seed")
def seed_db():
  movie1 = Movie(
    title = "Toy Story",
    description = "Led by Woody, Andy's toys live happily in his room until Andy's birthday brings Buzz Lightyear onto the scene. Afraid of losing his place in Andy's heart, Woody plots against Buzz. But when circumstances separate Buzz and Woody from their owner, the duo eventually learns to put aside their differences.",
    release_date = "1995-10-30",
    run_time = 81,
  )

  movie2 = Movie(
    title = "Jumanji",
    description = "When siblings Judy and Peter discover an enchanted board game that opens the door to a magical world, they unwittingly invite Alan -- an adult who's been trapped inside the game for 26 years -- into their living room. Alan's only hope for freedom is to finish the game, which proves risky as all three find themselves running from giant rhinoceroses, evil monkeys and other terrifying creatures.",
    release_date = "1995-12-15",
    run_time = 104,
  )

  admin_user = User(
    name = "Johnson Wang",
    email = "admin@email.com",
    password = bcrypt.generate_password_hash("123456").decode("utf-8"),
    admin = True,
    join_date = date.today()
  )

  user1 = User(
    name = "Lumberjack Williams",
    email = "user1@email.com",
    password = bcrypt.generate_password_hash("654321").decode("utf-8"),
    join_date = date.today()
  )

  db.session.add(movie1)
  db.session.add(movie2)
  db.session.add(admin_user)
  db.session.add(user1)
  db.session.commit()

  print("Table seeded")

@app.cli.command("drop")
def drop_db():
    db.drop_all()
    print("Tables dropped") 

@app.route("/movies", methods=["GET"])
def get_movies():
  
  #get ALL movies from database table *change for final
  movies_list = Movie.query.all()
  #conversion to json format
  result = movies_schema.dump(movies_list)

  return jsonify(result)

@app.route("/auth/register", methods=["POST"])
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
    
  return jsonify({"user": user.email, "token": access_token})

@app.route("/auth/login", methods=["POST"])
def auth_login():
    #get the user data from the request
    user_fields = user_schema.load(request.json)

    #check if email exists
    user = User.query.filter_by(email=user_fields["email"]).first()

    # error if user not exist or password incorrect
    if not user or not bcrypt.check_password_hash(user.password, user_fields["password"]):
        return abort(401, description="Incorrect username and password")
    
    #create access token with 1 day expiry
    expiry = timedelta(days=1)
    access_token = create_access_token(identity=str(user.id), expires_delta=expiry)
    
    return jsonify({"user": user.email, "token": access_token})