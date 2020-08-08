from flask import Flask
from flask_bootstrap import Bootstrap
from flask_httpauth import HTTPBasicAuth
from flask_login import LoginManager
from settings import Settings
from src.controllers import control

# Create app and
app = Flask(__name__)
app.config.from_object(Settings)

# Create Extensions
bootstrap = Bootstrap()
login_manager = LoginManager()
login_manager.login_view = "app.index"
auth = HTTPBasicAuth()

# Register Extensions and Blueprints
bootstrap.init_app(app)
login_manager.init_app(app)


app.register_blueprint(control)
