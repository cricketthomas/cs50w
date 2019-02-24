import os
import psycopg2
from flask import Flask, session, render_template, request, flash
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

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
    try:
        db.execute("INSERT INTO users (username, password) VALUES (:username, :password)",
                   {"username": username, "password": password})
        db.commit()
        return ("User account: " + username + " created.")
    except:
        return render_template("error.html", message="Error: username in use.")

# loggin in to an account


@app.route("/login", methods=["POST", "GET"])
def login():
    return render_template("login.html")


@app.route("/loggedin", methods=["POST", "GET"])
def loggedin():
    if request.method == 'POST':
        username = request.form.get("username").replace("'", "").strip()
        password = request.form.get("password")
        sql = "SELECT * FROM users WHERE username = :username AND password = :password"
        users = db.execute(
            sql, {'username': username, "password": password}).fetchall()
        if users:
            session['logged_in'] = True
            session['username'] = username
            message = "Hi, " + username + '!'
            return render_template("landing.html", message=message)
        else:
            flash('Error, username or password incorrect or does not exist.')
            return render_template("login.html")


@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    session.clear()
    return render_template('landing.html', message='bye')

    #db.execute('CREATE TABLE users (username VARCHAR PRIMARY KEY, password VARCHAR NOT NULL)')
# Search for books:


@app.route("/search", methods=["POST", "GET"])
def searchPage():
    return render_template("search.html")


@app.route("/results", methods=["POST", "GET"])
def results():
    textparams = request.form.get("search").replace(
        "'", "").strip().capitalize()
    params = request.form.get("params")
    if params == 'isbn':
        sql = """
        SELECT * FROM books WHERE isbn LIKE :textparams
        """
    elif params == "title":
        sql = """
        SELECT * FROM books WHERE title LIKE :textparams
        """
    elif params == "author":
        sql = """
        SELECT * FROM books WHERE author LIKE :textparams
        """
    else:
        sql = """
        SELECT * FROM books WHERE year LIKE :textparams
        """

    if db.execute(sql, {'textparams': '%'+textparams+'%'}).rowcount == 0:
        return render_template('landing.html', books="No results found.")
    books = db.execute(
        sql, {'textparams': '%'+textparams+'%'}).fetchall()

    return render_template('results.html', books=books, textparams=textparams, params=params, bookslen=len(books))
