import os

class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get("SECRET_KEY")
    DEBUG = os.environ.get("FLASK_DEBUG") == "1"
    @property
    def SQLALCHEMY_DATABASE_URI(self):
        value = os.environ.get("DATABASE_URL")

        if not value:
            raise ValueError("DATABASE_URL is not set")
    
        return value
    
class DevelopmentProductionConfig(Config):
    pass

class TestingConfig(Config):
    TESTING = True

app_config = DevelopmentProductionConfig()
app_config_testing = TestingConfig()
