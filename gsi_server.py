from flask import Flask, request
import json

app = Flask(__name__)
current_state = {}

@app.route("/", methods=["POST"])
def receive():
    global current_state
    data = request.get_json(force=True, silent=True)
    if data:
        current_state = data
    return "ok"

def get_state():
    return current_state

def run_server():
    app.run(host="127.0.0.1", port=3000, debug=False, use_reloader=False)