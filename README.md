# ESP32RelayAPI

## Overview
API service and hardware code to remotely power/shutdown my PC using ESP32 with a relay module. It uses [Render](https://render.com/) to host the simple web service API for remote calling. It also uses [adafruit](https://io.adafruit.com/) as the MQTT broker for establishing publisher/subscriber communication.


## Hardware Specs

### Microcontroller
```
ESP32 (any) with WiFi
```

### Relay Module
```
5V One Channel Relay Module Relay Switch
```

### Touch Sensor (Optional)
```
TTP223B Capacitive Touch Switch Module
```


### Hardware Diagram

![alt text](https://github.com/BryanL43/ESP32RelayAPI/blob/main/assets/Hardware_Diagram.png "Hardware Diagram")


## Microcontroller Installation

1. **Clone the repository:**
```sh
git clone <your-repo-url>
cd <your-repo-name>
```

2. **Installing Python tools (not in virtual environment):**

Ensure Python (preferably latest version) is installed on your device beforehand.
```sh
pip install esptool mpremote
```

3. **Erase flashing microcontroller at specified port:**

Change `<COM_PORT>` to the port your microcontroller is connected to. For Window, you can find it under `Device Manager > Ports (COM & LPT)`.
```sh
python -m esptool --port <COM_PORT> erase_flash
```

4. **Flash MicroPython to the microcontroller:**

Change `<COM_PORT>` to the port your microcontroller is connected to. For Window, you can find it under `Device Manager > Ports (COM & LPT)`.

**Note:** If you want to use a different MicroPython version, you can find it [here](https://micropython.org/download/ESP32_GENERIC/). Ensure to change the command's directory path for the downloaded `.bin`.
```sh
python -m esptool --chip esp32 --port <COM_PORT> --baud 460800 write_flash -z 0x1000 ./ESP32_GENERIC-20250415-v1.25.0.bin
```

5. **Set up adafruit MQTT broker & create a `Feed` for free at:**
```
https://io.adafruit.com/
```

6. **Set up global variables (credentials/mqtt info/GPIO pin) in `esp32/main.py`:**

Look for all `<VALUES>` in the code and change values to your credentials.

7. **Mounting program to microcontroller**
```sh
./mount.sh # On Windows use `.\mount.bat`
```


## Render Installation

1. **Set Source Code via method of your choice.**

2. **Set Root Directory to:**
```
src
```

3. **Set up environment variables:**
```sh
ADAFRUIT_USERNAME="your_adafruit_username"
ADAFRUIT_AIO_KEY="your_adafruit_aio_key"
API_TOKEN="your_private_curl_token" # A password of your choice for the curl command
MQTT_TOPIC="your_adafruit_feed" # Format: <username>/feeds/<topic_name>
```

## Usage

**Note:** Using Render.com free version typically takes around a minute to reboot after 15 minutes of idle. Be patient and do not spam the command/Ctrl+C.

### Powering on PC

**Window Powershell:**
```sh
Invoke-WebRequest -Uri "https://<render_link>/toggle" -Method POST -Headers @{ "X-Auth-Token" = "<your_private_curl_token>" }
```

**Curl:**
```sh
curl -X POST -H "X-Auth-Token: <your_private_curl_token>" https://<render_link>/toggle
```

### Force PC to power off (in case of crashes)

**Window Powershell:**
```sh
Invoke-WebRequest -Uri "https://<render_link>/shutdown" -Method POST -Headers @{ "X-Auth-Token" = "<your_private_curl_token>" }
```

**Curl:**
```sh
curl -X POST -H "X-Auth-Token: <your_private_curl_token>" https://<render_link>/shutdown
```


## Troubleshooting
- Ensure WiFi credentials are correct.
- Ensure all global variables are configured to your settings.
- Ensure MQTT Information is correct.
- Remount code if necessary.
- Run the Emergency stop microcontroller command.

**Emergency stop microcontroller command:**
```sh
mpremote connect COM4 fs rm main.py
mpremote connect COM4 reset
```


## License
This project is licensed under the MIT License.