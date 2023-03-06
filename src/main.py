from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#database URI via SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://db_dev:123456@localhost:5432/movie_review_db"

#database object
db = SQLAlchemy(app)

#create database object Movie

class Movie(db.Model):
  #table name of db
  __tablename__ = "MOVIES"

  #primary key
  id = db.Column(db.Integer, primary_key=True)

  #other attributes
  title = db.Column(db.String())
  description = db.Column(db.String())
  director = db.Column(db.String())
  release_date = db.Column(db.Date())
  genre = db.Column(db.String()) #this depends whether this data is available

#cli commands for the app
@app.cli.command("create")
def create_db():
  db.create_all()
  print("Table created")

@app.route("/")
def hello():
  return "Hello World!"