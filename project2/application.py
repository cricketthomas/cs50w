import os

from flask import Flask, render_template, request, flash, redirect, jsonify, url_for, session, jsonify
from flask_session import Session
from flask_socketio import SocketIO, emit


app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/", methods=["POST", "GET"])
def index():
    message = "Flack App"
    return render_template("index.html", message=message)


@app.route('/registered', methods=["POST"])
def registered():
    username = request.form.get("username")
    session['username'] = username
    session["logged_in"] = True
    return jsonify({"success": True, "username": username})


@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    session['logged_in'] = False
    return redirect(url_for('index'))


@app.route("/channels", methods=["POST", "GET"])
def channels():
    return render_template('channels.html')
