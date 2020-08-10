from flask_bootstrap import Bootstrap
from flask_login import LoginManager

bootstrap = Bootstrap()
login_manager = LoginManager()
login_manager.login_view = "app.index"
