@echo off
REM Replace with your ESP32's serial port
set ESP_PORT=COM4

REM List files on ESP32 and capture output
echo Checking ESP32 filesystem...
mpremote connect %ESP_PORT% fs ls > filelist.txt

REM Check if main.py exists
findstr /C:"main.py" filelist.txt > nul
IF %ERRORLEVEL% EQU 0 (
    echo main.py exists on ESP32. Deleting...
    mpremote connect %ESP_PORT% fs rm main.py
    
    echo Resetting ESP32 before upload...
    mpremote connect %ESP_PORT% reset
    timeout /t 2 /nobreak
) ELSE (
    echo main.py does not exist on ESP32. Proceeding...
)

del filelist.txt

REM Upload main.py
echo Uploading main.py to ESP32 on %ESP_PORT%...
mpremote connect %ESP_PORT% fs cp .\esp32\main.py :

REM Reset the ESP32
timeout /t 2 /nobreak
echo Resetting ESP32 on %ESP_PORT%...
mpremote connect %ESP_PORT% reset

echo Mount script completed.
