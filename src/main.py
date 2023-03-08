from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app():
  app = Flask(__name__)
  # configure from config.py  
  app.config.from_object("config.app_config") #change to app_config_testing for testing mode
  
  #initialise database, marshmallow, bcrypt and jwt objects
  db.init_app(app)
  ma.init_app(app)
  bcrypt.init_app(app)
  jwt.init_app(app)

  #register blueprints from other files
  from commands import db_commands
  from controllers import registerable_controllers

  app.register_blueprint(db_commands)
  
  for controller in registerable_controllers:
    app.register_blueprint(controller)

  return app