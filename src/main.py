from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def create_app():

    #create the flask app object
    app = Flask(__name__)

    #configuring the app, includes establishing database URL and secret key
    app.config.from_object("config.app_config_development") #change to app_config_testing for testing mode
    
    #create database object
    db.init_app(app)

    return app