from main import db
from flask import Blueprint
from main import bcrypt
from models import User, Movie, Review, List
from datetime import datetime
import psycopg2

db_commands = Blueprint("db", __name__)

#cli commands for the app
@db_commands.cli.command("create")
def create_db():
  db.create_all()
  print("Table created")

@db_commands.cli.command("seed")
def seed_db():

  #import movie date from movies.txt using psycopg2 connect cursor
  conn = psycopg2.connect(
     dbname = "movie_review_db",
     user = "db_dev",
     password = "123456",
     host = "localhost"
  )
  cursor = conn.cursor()

  with open('movies.txt', 'r') as f:
    cursor.copy_from(f, 'movies', sep='|')

  conn.commit()


  admin_user = User(
    name = "Johnson Wang",
    email = "admin@email.com",
    password = bcrypt.generate_password_hash("123456").decode("utf-8"),
    admin = True,
    join_date = datetime.now()
  )

  user1 = User(
    name = "Lumberjack Williams",
    email = "user1@email.com",
    password = bcrypt.generate_password_hash("654321").decode("utf-8"),
    join_date = datetime.now()
  )

  db.session.add(admin_user)
  db.session.add(user1)
  db.session.commit()

  review1 = Review(
     title = "Subtly crap",
     comment = "Jumanji is a bland and uninspired movie that lacks any real excitement or entertainment value. The cast's performances are lackluster and the special effects are underwhelming.",
     rating = 3,
     user = user1,
     movie_id = 8844,
     post_date = datetime.now()
  )

  review2 = Review(
     title = "The beginning of my childhood",
     comment = "Toy Story is a timeless classic that will take you back to your childhood in an instant. The movie's heartwarming storyline, packed with humor, action, and adventure, features lovable and relatable characters that you can't help but root for. As someone who grew up watching Toy Story, revisiting the movie was a nostalgic experience that brought back wonderful memories. From the iconic soundtrack to the stunning animation, everything about this movie is truly exceptional. Toy Story is a must-watch for anyone who loves great movies. It's a true masterpiece that will continue to bring joy for generations to come.",
     rating = 9,
     user = user1,
     movie_id = 862,
     post_date = datetime.now()
  )

  movies_dec_03 = Movie.query.filter(Movie.release_date.between("2003-12-01", "2003-12-31")).all()
  movies_dec_04 = Movie.query.filter(Movie.release_date.between("2004-12-01", "2004-12-31")).all()

  list1 = List(
     title = "Movies of December 2003",
     comment = "These are movies released in December 2003",
     post_date = datetime.now(),
     private = True,
     user = user1
  )

  list2 = List(
     title = "Movies of December 2004",
     comment = "These are movies released in December 2004",
     post_date = datetime.now(),
     user = user1
  )

  for movies in movies_dec_03:
     list1.movies.append(movies)

  for movies in movies_dec_04:
     list2.movies.append(movies)

  db.session.add(review1)
  db.session.add(review2)
  db.session.add(list1)
  db.session.add(list2)
  db.session.commit()
  print("Table seeded")

@db_commands.cli.command("drop")
def drop_db():
    db.drop_all()
    print("Tables dropped") 
