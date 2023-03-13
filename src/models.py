from main import db

class Movie(db.Model):
  #table name of db
  __tablename__ = "movies"

  #primary key
  id = db.Column(db.Integer, primary_key=True)

  #other attributes
  title = db.Column(db.String())
  description = db.Column(db.String())
  release_date = db.Column(db.Date())
  runtime = db.Column(db.Integer())
  reviews = db.relationship("Review", backref="movie")

class User(db.Model):
  __tablename__ = "users"

  #primary key
  id = db.Column(db.Integer, primary_key=True)

  #other attributes
  name = db.Column(db.String())
  email = db.Column(db.String(), nullable=False, unique=True)
  password = db.Column(db.String(), nullable=False)
  admin = db.Column(db.Boolean(), default=False)
  join_date = db.Column(db.Date())
  reviews = db.relationship("Review", backref="user")

class Review(db.Model):
  __tablename__ = "reviews"

  #primary key
  id = db.Column(db.Integer, primary_key=True)

  #other attributes
  title = db.Column(db.String())
  comment = db.Column(db.String())
  rating = db.Column(db.Integer())
  user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
  movie_id = db.Column(db.Integer, db.ForeignKey("movies.id"), nullable=False)