import os

class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # access to .env and get the value of SECRET_KEY, the variable name can be any but needs to match
    JWT_SECRET_KEY =  os.environ.get("SECRET_KEY")
    DEBUG = os.environ.get("FLASK_DEBUG") == '1'
    @property
    def SQLALCHEMY_DATABASE_URI(self):
        # access to .env and get the value of DATABASE_URL, the variable name can be any but needs to match
        value = os.environ.get("DATABASE_URL")

        if not value:
            raise ValueError("DATABASE_URL is not set")

        return value

class DevelopmentConfig(Config):
    pass

class TestingConfig(Config):
    TESTING = True

app_config_development = DevelopmentConfig()
app_config_testing = TestingConfig()