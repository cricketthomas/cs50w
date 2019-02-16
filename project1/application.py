import os
from flask import Flask, session, render_template, request
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
    return render_template("landing.html")

@app.route("/register", methods=["POST","GET"])
def register():
    return render_template("register.html")

@app.route('/registered', methods=["POST"])
def registered():
    username = request.form.get("username")
    password = request.form.get("password")



    try:
        db.execute("INSERT INTO users (username, password) VALUES (:username, :password)",
            {"username": username, "password": password})
        db.commit()
        return ("User account: " + username +" created.")
    except:
        return render_template("error.html", message="Error: username in use.")

    #db.execute('CREATE TABLE users (username VARCHAR PRIMARY KEY, password VARCHAR NOT NULL)')
