#!/bin/bash
ESP_PORT = "COM4" # Replace with your ESP32's serial port

# List files on ESP32 and capture output
echo "Checking ESP32 filesystem..."
mpremote connect ${ESP_PORT} fs ls > filelist.txt

# Check if main.py exists
if grep -q "main.py" filelist.txt; then
    echo "main.py exists on ESP32. Deleting..."
    mpremote connect ${ESP_PORT} fs rm main.py

    echo "Resetting ESP32 before upload..."
    mpremote connect ${ESP_PORT} reset
    sleep 2
else
    echo "main.py does not exist on ESP32. Proceeding..."
fi

rm ./filelist.txt

# Upload main.py
echo "Uploading main.py to ESP32 on ${ESP_PORT}..."
mpremote connect ${ESP_PORT} fs cp ./esp32/main.py :

# Reset the ESP32
echo "Resetting ESP32 on ${ESP_PORT}..."
mpremote connect ${ESP_PORT} reset

echo "Mount script completed."
