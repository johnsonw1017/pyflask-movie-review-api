from main import db

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