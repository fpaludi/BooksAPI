import os
from flask import Flask
from src import login_manager, bootstrap
# from src import db
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from src.adapters import orm

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SESSION_PERMANENT = False
    SESSION_TYPE = "filesystem"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "1234"
    GOODREAD_API_URL = "https://www.goodreads.com/book/review_counts.json"

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    if not SQLALCHEMY_DATABASE_URI:
        raise RuntimeError("SQLALCHEMY_DATABASE_URI is not set")

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
    # db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    
    # Register blueprint
    from src.controllers import control
    app.register_blueprint(control)

    return app


# def create_db(app):
#     orm.start_mappers()
#     engine = create_engine(app.config["DATABASE_URL"])
#     get_session = sessionmaker(bind=engine)
#     return get_session