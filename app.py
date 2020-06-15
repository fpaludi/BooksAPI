import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from factory_app import create_app

app = create_app(os.getenv("FLASK_CONFIG") or "default")

if __name__ == "__main__":
    app.run(use_debugger=False, use_reloader=False, passthrough_errors=True)
