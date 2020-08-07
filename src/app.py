from flask import Flask, Blueprint
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask import current_app
from flask_httpauth import HTTPBasicAuth
from settings import Settings

# Create app and
app = Flask(__name__)
app.config.from_object(Settings)

# Create Extensions
bootstrap = Bootstrap()
login_manager = LoginManager()
login_manager.login_view = "app.index"
auth = HTTPBasicAuth()

# Create Blueprints
control = Blueprint("app", __name__, template_folder="templates")

# Register Extensions and Blueprints
bootstrap.init_app(app)
login_manager.init_app(app)

# Register Blueprints
app.register_blueprint(control)
