from main import db
from flask import Blueprint
from main import bcrypt
from models import Movie, User
from datetime import date

db_commands = Blueprint("db", __name__)

#cli commands for the app
@db_commands.cli.command("create")
def create_db():
  db.create_all()
  print("Table created")

@db_commands.cli.command("seed")
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

@db_commands.cli.command("drop")
def drop_db():
    db.drop_all()
    print("Tables dropped") 
