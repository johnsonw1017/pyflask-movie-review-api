from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
#database URI via SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://db_dev:123456@localhost:5432/movie_review_db"

#database object
db = SQLAlchemy(app)

@app.route("/")
def hello():
  return "Hello World!"