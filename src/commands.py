from main import db
from flask import Blueprint
from main import bcrypt
from models import User, Review
from datetime import date
import psycopg2

db_commands = Blueprint("db", __name__)

#cli commands for the app
@db_commands.cli.command("create")
def create_db():
  db.create_all()
  print("Table created")

@db_commands.cli.command("seed")
def seed_db():
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
    join_date = date.today()
  )

  user1 = User(
    name = "Lumberjack Williams",
    email = "user1@email.com",
    password = bcrypt.generate_password_hash("654321").decode("utf-8"),
    join_date = date.today()
  )

  db.session.add(admin_user)
  db.session.add(user1)
  db.session.commit()

  review1 = Review(
     title = "Subtly crap",
     comment = "Jumanji is a bland and uninspired movie that lacks any real excitement or entertainment value. The cast's performances are lackluster and the special effects are underwhelming.",
     rating = 3,
     user = user1,
     movie_id = 8844
  )

  review2 = Review(
     title = "The beginning of my childhood",
     comment = "Toy Story is a timeless classic that will take you back to your childhood in an instant. The movie's heartwarming storyline, packed with humor, action, and adventure, features lovable and relatable characters that you can't help but root for. As someone who grew up watching Toy Story, revisiting the movie was a nostalgic experience that brought back wonderful memories. From the iconic soundtrack to the stunning animation, everything about this movie is truly exceptional. Toy Story is a must-watch for anyone who loves great movies. It's a true masterpiece that will continue to bring joy for generations to come.",
     rating = 9,
     user = user1,
     movie_id = 864
  )
  db.session.add(review1)
  db.session.add(review2)
  db.session.commit()
  print("Table seeded")

@db_commands.cli.command("drop")
def drop_db():
    db.drop_all()
    print("Tables dropped") 
