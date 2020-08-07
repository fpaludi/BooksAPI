from werkzeug.security import generate_password_hash, check_password_hash

class Users():
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.confirmed = True

    # --------------------------------------------
    # UserMixin Properties
    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return self.id
    # --------------------------------------------
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_pass(self, password):
        return check_password_hash(self.password_hash, password)

