import os
import psycopg2
import requests
import json
from flask import Flask, session, render_template, request, flash, redirect
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

# API Requests


def avg_rating(isbn):
    res = requests.get("https://www.goodreads.com/book/review_counts.json",
                       params={"key": "vT29hZVdtYRjuLVoVPw", "isbns": isbn})
    data = res.json()
    return data['books']


@app.route("/")
def index():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        currentUser = session.get('username')
        return render_template("landing.html", currentUser=currentUser)

# creating an account
@app.route("/register", methods=["POST", "GET"])
def register():
    return render_template("register.html")


@app.route('/registered', methods=["POST"])
def registered():
    session['username'] = request.form.get("username")
    username = session['username']
    password = request.form.get("password")
    password_hash = generate_password_hash(password)
    try:
        db.execute("INSERT INTO users (username, password) VALUES (:username, :password)",
                   {"username": username, "password": password_hash})
        db.commit()
        session['logged_in'] = True

        return render_template("landing.html", message=username + "account created")
    except:
        return render_template("404.html", message="Error: username in use.")

# loggin in to an account


@app.route("/login", methods=["POST", "GET"])
def login():
    return render_template("login.html")

# Test login with password hashing
@app.route("/loggedin", methods=["POST", "GET"])
def loggedin():
    if request.method == 'POST':
        username = request.form.get("username").replace("'", "").strip()
        password = request.form.get("password")
        sql = "SELECT * FROM users WHERE username = :username"
        users = db.execute(sql, {'username': username}).fetchone()
        if users is not None:
            x = [x for x in users]
            hash_resolved = check_password_hash(x[1], password)
            if users and hash_resolved:
                session['logged_in'] = True
                session['username'] = username
                message = "Hi, " + username + '!'
                return render_template("search.html", message=message)
            elif users and not hash_resolved:
                flash('Error, is password incorrect.')
                return render_template("login.html")
        else:
            flash('Error, username or password incorrect or does not exist.')
            return render_template("login.html")


@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    session.clear()
    return render_template('login.html', message='bye')


# Search for books:
@app.route("/search", methods=["POST", "GET"])
def searchPage():
    if not session.get('logged_in'):
        return render_template('login.html')
    return render_template("search.html")


@app.route("/results", methods=["POST"])
def results():
    if not session.get('logged_in'):
        return render_template('login.html')
    textparams = request.form.get("search").replace(
        "'", "").strip().capitalize()
    params = request.form.get("params")
    if params == '':
        sql = """SELECT * FROM books WHERE isbn LIKE '%""" + textparams + """%' OR title  LIKE '%""" + textparams + """%'
        OR author LIKE '%""" + textparams + """%' OR year  LIKE '%""" + textparams + """%'"""
        books = db.execute(sql).fetchall()
    else:
        sql = """ SELECT * FROM books WHERE """ + params + """ LIKE :textparams """
        books = db.execute(sql, {'textparams': '%'+textparams+'%'}).fetchall()
    if len(books) == 0:
        flash("No Results for: " + textparams)
        return render_template('search.html')
    return render_template('results.html', books=books, textparams=textparams, params=params, bookslen=len(books))


@app.route("/results/<string:book_id>")
def book(book_id):
    if not session.get('logged_in'):
        return render_template('login.html')
    book = db.execute("SELECT * FROM books WHERE isbn = :isbn",
                      {"isbn": book_id}).fetchone()
    if book is None:
        return render_template("404.html", message=" We could not locate that book.")
    all_reviews = db.execute(
        "SELECT * FROM reviews WHERE book = :book", {"book": book.isbn}).fetchall()
    current_review = db.execute(
        "SELECT * FROM reviews WHERE book = :book AND reviewer_id = :reviewer_id", {"book": book.isbn, "reviewer_id": session['username']}).fetchone()
    good_reads = avg_rating(book.isbn)

    return render_template("book.html", book=book, all_reviews=all_reviews, current_review=current_review, good_reads=good_reads)


@app.route("/results/<string:book_id>/reviewed", methods=["POST", "GET"])
def review(book_id):
    if not session.get('logged_in'):
        return render_template('login.html')
    review = request.form.get("review")
    review_score = request.form.get("review_score")
    good_reads = avg_rating(book_id)
    book = db.execute("SELECT * FROM books WHERE isbn = :isbn",
                      {"isbn": book_id}).fetchone()
    all_reviews = db.execute(
        "SELECT * FROM reviews WHERE book = :book", {"book": book.isbn}).fetchall()

    current_review = db.execute("SELECT * FROM reviews WHERE book = :book AND reviewer_id = :reviewer_id", {
                                "book": book.isbn, "reviewer_id": session['username']}).fetchone()
    try:
        review = db.execute("INSERT INTO reviews (reviewer_id, book, review, review_score, date) VALUES (:reviewer_id, :book, :review, :review_score, :date)", {
                            "reviewer_id": session['username'], "book": book.isbn, "review": review, "review_score": review_score, "date": "now()"})
        db.commit()
        current_review = db.execute("SELECT * FROM reviews WHERE book = :book AND reviewer_id = :reviewer_id",
                                    {"book": book.isbn, "reviewer_id": session['username']}).fetchone()
        all_reviews = db.execute(
            "SELECT * FROM reviews WHERE book = :book", {"book": book.isbn}).fetchall()
        flash("Review Submitted Sucessfully.")
        return render_template("book.html", book=book, all_reviews=all_reviews, current_review=current_review, good_reads=good_reads)
    except:
        flash("Review Submission Failed. Only one review per user allowed.")
        return render_template("book.html", book=book, all_reviews=all_reviews, current_review=current_review, good_reads=good_reads)

@app.route("/api/<string:isbn>")
def api(isbn):
    return "api access"

@app.errorhandler(404)
def notFound(e):
    message = e
    return render_template('404.html', message=message), 404


@app.errorhandler(403)
def forbidden(e):
    message = e
    return render_template('404.html', message=message), 403


@app.errorhandler(500)
def serverError(e):
    message = e
    return render_template('404.html', message=message), 403


@app.errorhandler(400)
def badRequest(e):
    message = e
    return render_template('404.html', message=message), 400

