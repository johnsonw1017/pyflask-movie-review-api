from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

def create_app():

    #create the flask app object
    app = Flask(__name__)

    #configuring the app, includes establishing database URL and secret key
    app.config.from_object("config.app_config_development") #change to app_config_testing for testing mode
    
    #create database object
    db.init_app(app)

    # create marshmallow object
    ma.init_app(app)

    #import controllers and register blueprint
    from controllers import registerable_controllers

    for controller in registerable_controllers:
        app.register_blueprint(controller)

    return app