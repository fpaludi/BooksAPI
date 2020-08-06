import os 
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask import current_app

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.adapters import orm

# db = SQLAlchemy()
bootstrap = Bootstrap()
login_manager = LoginManager()
login_manager.login_view = "app.index"

orm.start_mappers()
URI = os.getenv("DATABASE_URL")
get_session = sessionmaker(bind=create_engine(URI))
