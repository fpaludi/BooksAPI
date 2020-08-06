import os
from flask import current_app
from flask import jsonify, g
from flask_httpauth import HTTPBasicAuth
from .adapters.repository import Repository
from . import get_session

auth = HTTPBasicAuth()
#get_session = create_db(current_app)

@auth.verify_password
def api_verify_password(username, password):
    """
    HttpAuth callback function. Is is used to verify the password
    for an API call
    """
    session = get_session()
    repo = Repository(session)
    if username == "":
        return False
    user = repo.get_username(username)
    if not user:
        return False
    g.current_user = user
    return user.validate_pass(password)


@auth.error_handler
def auth_error():
    return jsonify({"msg": "Invalid Credentials"}), 401