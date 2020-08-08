from flask import g, jsonify
from src.app import auth


class AuthenticationService:
    def __init__(self, repository):
        self._repository = repository

    def login(self, username, password):
        user = self._repository.get_username(username)
        # Users.query.filter_by(username=username).first()
        if user is not None and user.validate_pass(password):
            return "Logged in successfully", True, user
        return "Username or password incorrect. Please try again", False, None

    def add_new_user(self, username, password):
        user = dict(username=username, password=password)
        self._repository.add_user(user)

    def signin(self, username, password, password2):
        if password == password2:
            user = self._repository.get_username(username)
            if not user:
                self.add_new_user(username, password)
                return "User signed up", True
            return "Username already exists, pick up another.", False
        return "Passwords are not equal. Try again", False

    @auth.verify_password  # type: ignore
    def api_verify_password(self, username, password):
        """
        HttpAuth callback function. Is is used to verify the password
        for an API call
        """
        if username == "":
            return False
        user = self._repository.get_username(username)
        if not user:
            return False
        g.current_user = user
        return user.validate_pass(password)

    @auth.error_handler  # type: ignore
    def auth_error(self):
        return jsonify({"msg": "Invalid Credentials"}), 401
