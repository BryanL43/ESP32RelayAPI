from flask import Flask, jsonify, request
import os
import paho.mqtt.client as mqtt

app = Flask(__name__);

API_TOKEN = os.environ.get("API_TOKEN");
ADAFRUIT_USERNAME = os.environ.get("ADAFRUIT_USERNAME");
ADAFRUIT_AIO_KEY = os.environ.get("ADAFRUIT_AIO_KEY");

MQTT_BROKER = "io.adafruit.com";
MQTT_PORT = 1883;
# MQTT_TOPIC = "8cb124f8c277c16ec0b2ee00569fd151a08e342b/esp32/relay";
MQTT_TOPIC = "BryanL43/feeds/relay";

@app.route("/")
def home():
    return "API is LIVE!";

@app.route("/toggle", methods=["POST"])
def toggle():
    token = request.headers.get("X-Auth-Token");
    if token != API_TOKEN:
        return jsonify({"error": "unauthorized"}), 403;

    try:
        client = mqtt.Client();
        client.username_pw_set(ADAFRUIT_USERNAME, ADAFRUIT_AIO_KEY);
        client.connect(MQTT_BROKER, MQTT_PORT, 60);
        client.publish(MQTT_TOPIC, payload="toggle");
        client.loop();
        client.disconnect();

        return jsonify({"status": "ok"}), 200;
    except Exception as e:
        return jsonify({"error": str(e)}), 500;

@app.route("/shutdown", methods=["POST"])
def shutdown():
    token = request.headers.get("X-Auth-Token");
    if token != API_TOKEN:
        return jsonify({"error": "unauthorized"}), 403;

    try:
        client = mqtt.Client();
        client.connect(MQTT_BROKER, MQTT_PORT, 60);
        client.publish(MQTT_TOPIC, payload="shutdown");
        client.loop();
        client.disconnect();

        return jsonify({"status": "ok"}), 200;
    except Exception as e:
        return jsonify({"error": str(e)}), 500;