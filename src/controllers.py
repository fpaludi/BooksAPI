from flask import (
    render_template,
    url_for,
    redirect,
    jsonify,
    flash,
)
from flask_login import current_user, login_required, login_user, logout_user
from src.app import login_manager, auth, control
from src.forms.forms import FilterBookForm, BookReviewForm, LogInForm, SignInForm
from src.repositories import RepositoryContainer
from src.services import ServicesContainer
from src.services.logger import get_logger

logger = get_logger(__name__)

@control.route("/", methods=["GET", "POST"])
def index():
    auth_service = ServicesContainer.auth_service()
    form = LogInForm()

    logger.info("Start index")
    if form.validate_on_submit():
        msg, st, user = auth_service.login(form.username.data, form.password.data)
        flash(msg)
        if st:
            login_user(user, True)
            logger.info("logged in, redirecdting to search book")
            return redirect(url_for("app.search_book"))

    logger.info("rendering log in form")
    return render_template("forms.html", form=form, title_msg="Log In")


@control.route("/sign_in", methods=["GET", "POST"])
def sign_in():
    auth_service = ServicesContainer.auth_service()
    form = SignInForm()

    if form.validate_on_submit():
        msg, st = auth_service.signin(form.username.data, form.password.data, form.password2.data)
        flash(msg)
        if st:
            return redirect(url_for("app.index"))
    return render_template("forms.html", form=form, title_msg="Sign In")


@control.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for("app.index"))


@control.route("/book/search", methods=["GET", "POST"])
@login_required
def search_book():
    logger.info("Start search book")
    book_service = ServicesContainer.book_service()

    form = FilterBookForm()
    books = []
    if form.validate_on_submit():
        filter_sel = form.filter_sel.data
        filter_value = form.string.data
        books = book_service.get_books_by(filter_sel, filter_value)
        logger.info("looking for a book")

    return render_template("filter_book.html", form=form, books=books)


@control.route("/book/<int:book_id>", methods=["GET", "POST"])
@login_required
def show_book(book_id):
    book_service = ServicesContainer.book_service()
    api_service = ServicesContainer.api_service()

    form = BookReviewForm()
    book = book_service.get_books_by_id(book_id)
    goodread_results = api_service.get_json_from_goodreads(book.isbn)
    goodread_rating = goodread_results["books"][0]["average_rating"]
    
    if form.validate_on_submit():
        user_id = current_user.id
        msg, st = book_service.insert_book_review(
            book, current_user, form.review_value.data, "",)
        flash(msg)

    return render_template(
        "book_page.html", book=book, form=form, api_rating=goodread_rating
    )


@control.route("/api/<string:isbn>")
@auth.login_required
def get_goodread_data(isbn):
    goodread_results = services.get_json_from_goodreads(isbn)
    return jsonify(goodread_results), 200


@login_manager.user_loader
def load_user(user_id):
    repo = RepositoryContainer.repository()
    return repo.get_user_id(int(user_id))
