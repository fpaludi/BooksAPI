import os
from os.path import dirname, join
from dotenv import load_dotenv
from flask import Flask

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)


class Settings:  # i.e. Production
    DATABASE_URL = os.environ.get("DATABASE_URL")
    GOODREAD_API_KEY = os.environ.get("GOODREAD_API_KEY")
    GOODREAD_API_URL = os.environ.get("GOODREAD_API_URL")
    SECRET_KEY = os.environ.get("SECRET_KEY")


class ProdSettings:
    pass


class DevSettings:
    DEBUG = True


class TestSettings:
    TESTING = True
    DATABASE_URL = os.environ.get("DATABASE_TEST_URL")


def update_settings(config_name="default"):
    global Settings
    config = {
        "development": DevSettings,
        "testing": TestSettings,
        "production": ProdSettings,
        "default": DevSettings,
    }
    for k in config[config_name].__dict__.keys():
        if not k.startswith("__"):
            setattr(Settings, k, config[config_name].__dict__[k])


def create_app(config_name="default"):
    print("CREATING APP")
    from src import login_manager, bootstrap
    from src.models import orm

    update_settings(config_name)
    app = Flask(__name__)
    app.config.from_object(Settings)

    # Flask Extensions
    bootstrap.init_app(app)
    login_manager.init_app(app)

    # Register blueprint
    print("IMPORTING CONTROLLERS...")
    from src.controllers import control  # noqa

    app.register_blueprint(control)

    # Start ORM Mappers
    orm.start_mappers()

    return app
