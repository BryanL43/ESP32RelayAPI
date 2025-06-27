from flask import Flask, jsonify, request
import os
import paho.mqtt.publish as publish

app = Flask(__name__);

API_TOKEN = os.environ.get("API_TOKEN");

@app.route("/toggle", methods=["POST"])
def toggle():
    token = request.headers.get("X-Auth-Token");
    if token != API_TOKEN:
        return jsonify({"error": "unauthorized"}), 403;

    publish.single(
        topic="esp32/relay",
        payload="toggle",
        hostname="broker.hivemq.com",
        port=1883
    );
    return jsonify({"status": "ok"});
