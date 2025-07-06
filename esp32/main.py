from umqtt.simple import MQTTClient
import network
import time
import machine
from machine import Pin
import _thread
import ubinascii

# WIFI CREDENTIALS
SSID = "<YOUR_WIFI_SSID>";
PASSWORD = "<YOUR_WIFI_PASSWORD>";

# ADAFRUIT CREDENTIALS
ADAFRUIT_USERNAME = "<YOUR_ADAFRUIT_USERNAME>";
ADAFRUIT_AIO_KEY = "<YOUR_ADAFRUIT_AIO_KEY>";

# MQTT INFO
MQTT_TOPIC = "<YOUR_MQTT_TOPIC>"; # Format: <username>/feeds/<topic_name>

# PIN CONFIG
RELAY_PIN = Pin(4, Pin.OUT);
RELAY_PIN.value(0);

TOUCH_PIN = Pin(34, Pin.IN);

# GLOBAL VARIABLES
relay_lock = _thread.allocate_lock();

def turn_on():
    with relay_lock:
        print("Relay triggered");
        RELAY_PIN.value(1);
        time.sleep(0.5);
        RELAY_PIN.value(0);

def shutdown():
    with relay_lock:
        print("Shutting down...");
        RELAY_PIN.value(1);
        time.sleep(5);
        RELAY_PIN.value(0);

def on_message(topic, msg):
    """Callback function for MQTT messages to trigger events."""
    if msg == b"toggle":
        turn_on();
    elif msg == b"shutdown":
        shutdown();
    else:
        print("Ignoring unexpected message:", msg);

def connect_wifi():
    wlan = network.WLAN(network.STA_IF);
    wlan.active(True);

    reset_counter = 0;

    while not wlan.isconnected():
        # Reset ESP32 if connection fails 10 times (5 minutes).
        # Potential unresponsiveness after days of inactivity.
        if reset_counter >= 10:
            print("\nWiFi connection failed. Resetting...");
            reset_counter = 0;
            machine.reset();

        print("Attempting to connect to WiFi...", end="");
        wlan.connect(SSID, PASSWORD);

        # Wait for connection. Maximum of 10 seconds.
        retry_count = 0;
        while not wlan.isconnected() and retry_count < 10:
            print(".", end="");
            time.sleep(1);
            retry_count += 1;

        if wlan.isconnected():
            print("\nWiFi connected:", wlan.ifconfig());
            break;
        else:
            print("\nWiFi connection failed. Retrying in 30 seconds...");
            reset_counter += 1;
            time.sleep(30);

def setup_mqtt():
    """Setup MQTT connection and subscribe to topic."""

    # Generate unique client ID
    chip_id = ubinascii.hexlify(machine.unique_id()).decode();
    client_id = f"esp32_{chip_id}";

    while True:
        try:
            # Establish MQTT Broker connection and subscribe
            client = MQTTClient(
                client_id=client_id,
                server="io.adafruit.com",
                port=1883,
                user=ADAFRUIT_USERNAME,
                password=ADAFRUIT_AIO_KEY,
                keepalive=30
            );
            client.set_callback(on_message);
            client.connect();
            client.subscribe(MQTT_TOPIC);
            print("Subscribed to topic:", MQTT_TOPIC);

            # Wait for messages
            while True:
                client.check_msg();
                time.sleep(1);
        
        except OSError as e:
            print("MQTT connection error:", e);
            print("Reconnecting...");
            time.sleep(2);

def touch_thread():
    """Thread to handle TTP223B Capacitive Touch Switch Module."""
    touch_active = False;
    touch_start = 0;

    while True:
        if TOUCH_PIN.value(): # Sensor detected touch
            if not touch_active:
                # Touch just started
                touch_active = True;
                touch_start = time.ticks_ms();
                print("Hold started...");
        else: # Sensor did not detect touch/was released
            if touch_active:
                # Touch just ended
                duration = time.ticks_diff(time.ticks_ms(), touch_start);
                print("Touch duration:", duration, "ms");

                if duration >= 2000:
                    print("Long hold: shutting down...");
                    shutdown()
                elif duration >= 50:
                    print("Quick hold: turning on...");
                    turn_on()

                touch_active = False;

        time.sleep(0.01);


connect_wifi();
_thread.start_new_thread(setup_mqtt, ());
_thread.start_new_thread(touch_thread, ());

# Prevent main thread from exiting
while True:
    if not network.WLAN(network.STA_IF).isconnected():
        print("Main thread: WiFi disconnected. Reconnecting...");
        connect_wifi();
    
    time.sleep(5);