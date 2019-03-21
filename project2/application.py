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
import json
from flask_socketio import SocketIO, emit, send
from werkzeug.utils import secure_filename


# Configure socket.io
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

# for image uploads
UPLOAD_FOLDER = 'project2/static/images'


channels = ["Default"]
messages = {}


@app.route("/")
def index():
    message = "Flack App"
    return render_template("index.html", message=message, channels=channels)


@app.route("/channel/<string:channel_name>")
def current_channel(channel_name):
    return render_template(
        "current_channel.html", channel_name=channel_name, messages=messages
    )


# SOCKET.IO


@socketio.on("submit message")
def message(data):

    # A bit repetitive, but it creates a default channel name for the channel,
    # then appends the message, or removes the first mesaage then appends the last one only storing the last 100.
    messages.setdefault(data["channel"], [])

    if len(messages[data["channel"]]) >= 100:
        messages[data["channel"]].pop(0)
        messages.setdefault(data["channel"], []).append(
            {"message": data["message"], "user": data["user"], "time": data["time"], "image": data["image"]})

    else:
        messages.setdefault(data["channel"], []).append(
            {"message": data["message"], "user": data["user"], "time": data["time"], "image": data["image"]})

    # print(json.dumps(messages))
    # all_messages = json.dumps(messages)
    emit("announce message", data, broadcast=True)


@socketio.on("submit channel")
def add_channel(data):
    channels.append(data["channel"])
    emit("announce channel", data, broadcast=True)
    print("channel added")


if __name__ == "__main__":
    socketio.run(app, debug=False)
