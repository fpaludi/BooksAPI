import os
from flask import Flask
from src import login_manager, db, bootstrap

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "1234"
    GOODREAD_API_URL = "https://www.goodreads.com/book/review_counts.json"

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    if not SQLALCHEMY_DATABASE_URI:
        raise RuntimeError("DATABASE_URL is not set")

    GOODREAD_API_KEY = os.getenv("GOODREAD_API_KEY")
    if not GOODREAD_API_KEY:
        raise RuntimeError("GOODREAD_API_KEY is not set")

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    pass


def create_app(config_name):
    config = {
        "development": DevelopmentConfig,
        "testing": TestingConfig,
        "production": ProductionConfig,
        "default": DevelopmentConfig,
    }

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)

    # Register blueprint
    from src.controllers import control
    app.register_blueprint(control)

    return app
