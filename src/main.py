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

    #create the flask app object
    app = Flask(__name__)

    #configuring the app, includes establishing database URL and secret key
    app.config.from_object("config.app_config_development") #change to app_config_testing for testing mode
    
    #create database object
    db.init_app(app)

    # create marshmallow object
    ma.init_app(app)

    #create jwt and bcrypt objects for authentication
    jwt.init_app(app)
    bcrypt.init_app(app)

    #import cli commands and register blueprint
    from commands import db_commands
    app.register_blueprint(db_commands)


    #import controllers and register blueprint
    from controllers import registerable_controllers

    for controller in registerable_controllers:
        app.register_blueprint(controller)

    return app