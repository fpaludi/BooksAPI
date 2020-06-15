from flask import (
    Flask,
    session,
    Blueprint,
    render_template,
    url_for,
    redirect,
    jsonify,
    flash
)
from flask_login import current_user, login_required, login_user, logout_user
from .forms import FilterBookForm, BookReviewForm, LogInForm, SignInForm
from .models.books import Books
from .models.users import Users
from . import services

control = Blueprint("app", __name__, template_folder="templates")


@control.route("/", methods=["GET", "POST"])
def index():
    form = LogInForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()

        if user is not None and user.validate_pass(form.password.data):
            flash("Logged in succesfully")
            login_user(user, True)
            return redirect(url_for("app.search_book"))
        else:
            flash("Username or Password incorrect")
    return render_template("index.html", form=form)


@control.route("/sign_in", methods=["GET", "POST"])
def sign_in():
    form = SignInForm()
    if form.validate_on_submit():
        if form.password.data == form.password2.data:
            new_user = Users(username=form.username.data,
            password=form.password.data)
            status, msg = new_user.add_user()
            flash(msg)
            if status:
                return redirect(url_for("app.index"))
        else:
            flash("Passwords are not equals. Try again")
    return render_template("sign_in.html", form=form)

@control.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for("app.index"))


@control.route("/book/search", methods=["GET", "POST"])
@login_required
def search_book():
    form = FilterBookForm()

    books = []
    if form.validate_on_submit():
        filter_sel = form.filter_sel.data
        filter_value = form.string.data
        filter_dict = {filter_sel: filter_value}
        books = Books.query.filter(
            Books.__table__.columns[filter_sel].like(f"%{filter_value}%")
        ).all()
        # books = Books.query.filter_by(**filter_dict).all()
    return render_template("filter_book.html", form=form, books=books)


@control.route("/book/<int:book_id>", methods=["GET", "POST"])
@login_required
def show_book(book_id):
    form = BookReviewForm()
    book = Books.query.get(book_id)

    if form.validate_on_submit():
        user_id = current_user.id
        st, msg = book.insert_book_review(user_id, form.review_value.data, review_comment="")
        flash(msg)

    goodread_results = services.get_json_from_goodreads(book.isbn)
    goodread_rating = goodread_results["books"][0]["average_rating"]

    return render_template(
        "book_page.html", book=book, form=form, api_rating=goodread_rating
    )


@control.route("/api/<string:isbn>")
def get_goodread_data(isbn):
    goodread_results = services.get_json_from_goodreads(isbn)
    return jsonify(goodread_results)

