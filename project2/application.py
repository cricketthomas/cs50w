import os
import requests
from flask import (
    Flask,
    render_template,
    request,
    flash,
    redirect,
    jsonify,
    url_for,
    session,
    jsonify,
)

from flask_socketio import SocketIO, emit, send

# Configure socket.io
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)


channels = ["Default"]


@app.route("/")
def index():
    message = "Flack App"
    return render_template("index.html", message=message, channels=channels)


@app.route("/channel")
def channel():
    return render_template("channels.html")


@app.route("/new_channel", methods=["POST"])
def new_channel():
    new_channel = request.form.get("channel_name")
    channels.append(new_channel)
    return render_template("channels.html", channels=channels)


@app.route("/channel/<string:channel_name>")
def current_channel(channel_name):
    channel_name = channel_name
    return render_template(
        "current_channel.html", channel_name=channel_name, votes=votes
    )


# SOCKET.IO
votes = {"yes": 0, "no": 0, "maybe": 0}


@socketio.on("submit vote")
def vote(data):
    selection = data["selection"]
    votes[selection] += 1
    emit("vote totals", votes, broadcast=True)


@socketio.on("submit message")
def message(data):
    emit("announce message", data, broadcast=True)


@socketio.on("submit channel")
def add_channel(data):
    channels.append(data["channel"])
    emit("announce channel", data, broadcast=True)
    print("channel added")


if __name__ == "__main__":
    socketio.run(app, debug=False)
