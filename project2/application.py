import os
import requests

from flask import Flask, render_template, request, flash, redirect, jsonify, url_for, session, jsonify
from flask_session import Session
from flask_socketio import SocketIO, emit

# Configure socket.io 
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


votes = {"yes": 0, "no": 0, "maybe": 0}

@app.route("/")
def index():
    message = "Flack App"
    return render_template("index.html", message=message,votes=votes)


@socketio.on("submit vote")
def vote(data):
    selection = data["selection"]
    votes[selection] += 1
    emit("vote totals", votes, broadcast=True)



@app.route("/channels", methods=["POST", "GET"])
def channels():
    return render_template('channels.html')
