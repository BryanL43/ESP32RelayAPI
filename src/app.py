from flask import Flask, jsonify, request
import os
import paho.mqtt.publish as publish

app = Flask(__name__);

API_TOKEN = os.environ.get("API_TOKEN");

@app.route("/")
def home():
    return "API is LIVE!"

@app.route("/toggle", methods=["POST"])
def toggle():
    token = request.headers.get("X-Auth-Token");
    if token != API_TOKEN:
        return jsonify({"error": "unauthorized"}), 403;

    publish.single(
        topic="8cb124f8c277c16ec0b2ee00569fd151a08e342b/esp32/relay",
        payload="toggle",
        hostname="broker.hivemq.com",
        port=1883
    );
    return jsonify({"status": "ok"});
