from flask import (
    Flask,
    session,
    Blueprint,
    render_template,
    url_for,
    redirect,
    jsonify,
    flash,
    current_app
)
from flask_login import current_user, login_required, login_user, logout_user
from .forms import FilterBookForm, BookReviewForm, LogInForm, SignInForm
from .authentication import auth
from .adapters.repository import Repository 
from .logger import get_logger
from . import login_manager
from . import services
from . import get_session

control = Blueprint("app", __name__, template_folder="templates")
logger = get_logger(__name__)

@control.route("/", methods=["GET", "POST"])
def index():
    logger.info("Start index")
    session = get_session()
    repo = Repository(session)

    form = LogInForm()
    if form.validate_on_submit():
        msg, st, user = services.login(form.username.data, form.password.data, repo)
        flash(msg)
        if st:
            login_user(user, True)
            logger.info("logged in, redirecdting to search book")
            return redirect(url_for("app.search_book"))

    logger.info("rendering log in form")
    return render_template("forms.html", form=form, title_msg="Log In")


@control.route("/sign_in", methods=["GET", "POST"])
def sign_in():
    session = get_session()
    repo = Repository(session)

    form = SignInForm()
    if form.validate_on_submit():
        msg, st = services.signin(form.username.data, form.password.data, form.password2.data, repo, session)
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
    session = get_session()
    repo = Repository(session)

    form = FilterBookForm()
    books = []
    if form.validate_on_submit():
        filter_sel = form.filter_sel.data
        filter_value = form.string.data
        books = services.get_books_by(filter_sel, filter_value, repo)
        logger.info("looking for a book")

    return render_template("filter_book.html", form=form, books=books)


@control.route("/book/<int:book_id>", methods=["GET", "POST"])
@login_required
def show_book(book_id):
    session = get_session()
    repo = Repository(session)

    form = BookReviewForm()
    book = services.get_books_by_id(book_id, repo)
    goodread_results = services.get_json_from_goodreads(book.isbn)
    goodread_rating = goodread_results["books"][0]["average_rating"]
    
    if form.validate_on_submit():
        user_id = current_user.id
        msg, st = services.insert_book_review(
            book, current_user, form.review_value.data, "",
            repo, session
        )
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
    session = get_session()
    repo = Repository(session)
    return repo.get_user_id(int(user_id))
