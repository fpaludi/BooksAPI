from flask import g, jsonify
from flask_httpauth import HTTPBasicAuth
from src.repositories.unit_of_work import UnitOfWork
from src.repositories import RepositoryContainer

auth = HTTPBasicAuth()


class AuthenticationService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def login(self, username, password):
        with self.uow as uow:
            user = uow.repository.get_username(username)
        # Users.query.filter_by(username=username).first()
        if user is not None and user.validate_pass(password):
            return "Logged in successfully", True, user
        return "Username or password incorrect. Please try again", False, None

    def add_new_user(self, username, password):
        with self.uow as uow:
            user = uow.repository.get_username(username)
            if not user:
                user = dict(username=username, password=password)
                uow.repository.add_user(user)
                uow.commit()
                return 1
            return 0

    def signin(self, username, password, password2):
        if password == password2:
            new_user_status = self.add_new_user(username, password)
            if new_user_status:
                return "User signed up", True
            return "Username already exists, pick up another.", False
        return "Passwords are not equal. Try again", False


@auth.verify_password  # type: ignore
def api_verify_password(username, password):
    """
    HttpAuth callback function. Is is used to verify the password
    for an API call
    """
    uow = RepositoryContainer.uow()
    if username == "":
        return False
    with uow:
        user = uow.repository.get_username(username)
    if not user:
        return False
    g.current_user = user
    return user.validate_pass(password)


@auth.error_handler  # type: ignore
def auth_error():
    return jsonify({"msg": "Invalid Credentials"}), 401
