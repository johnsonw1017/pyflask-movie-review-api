from main import db
from flask import Blueprint
from main import bcrypt
from models import Movie, User
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
    cursor.copy_from(f, 'MOVIES', sep='|')

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

  print("Table seeded")

@db_commands.cli.command("drop")
def drop_db():
    db.drop_all()
    print("Tables dropped") 
