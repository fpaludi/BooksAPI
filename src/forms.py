from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, IntegerField, PasswordField
from wtforms.validators import DataRequired, NumberRange


class LogInForm(FlaskForm):
    username = StringField("Username: ", validators=[DataRequired()])
    password = PasswordField("Password: ", validators=[DataRequired()])
    submit = SubmitField("Log In")


class SignInForm(FlaskForm):
    username = StringField("Username: ", validators=[DataRequired()])
    password = PasswordField("Password: ", validators=[DataRequired()])
    password2 = PasswordField("Repeat Password: ", validators=[DataRequired()])
    submit = SubmitField("Sign In")


class FilterBookForm(FlaskForm):
    filter_choices = [("isbn", "isbn"), ("title", "title"), ("author", "author")]
    string = StringField("Search for ", validators=[DataRequired()])
    filter_sel = RadioField(
        "Search in: ", choices=filter_choices, default=filter_choices[0][0]
    )
    submit = SubmitField("Search!")


class BookReviewForm(FlaskForm):
    review_value = IntegerField(
        "Insert Review:",
        validators=[
            DataRequired(),
            NumberRange(1, 5, message="Insert a number between 1 and 5"),
        ],
    )
    submit = SubmitField("Insert!")
