import os
from flask import current_app as app
from flask import jsonify, g
from flask_httpauth import HTTPBasicAuth
from .models.users import Users
from . import db

auth = HTTPBasicAuth()

@auth.verify_password
def api_verify_password(username, password):
    """
    HttpAuth callback function. Is is used to verify the password
    for an API call
    """
    if username == "":
        return False
    user = Users.query.filter_by(username=username).first()
    if not user:
        return False
    g.current_user = user
    return user.validate_pass(password)


@auth.error_handler
def auth_error():
    return jsonify({"msg": "Invalid Credentials"}), 401