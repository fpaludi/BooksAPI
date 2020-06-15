from flask import Flask
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .. import login_manager, db

class Users(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password_hash = db.Column(db.String, nullable=False)
    confirmed = db.Column(db.Boolean, default=False)
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_pass(self, password):
        return check_password_hash(self.password_hash, password)

    def add_user(self):
        if not Users.query.filter_by(username=self.username).first():
            self.confirmed = True
            db.session.add(self)
            db.session.commit()
            return 1, "User signed up"
        return 0, "Username already exists, pick up another"


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))
