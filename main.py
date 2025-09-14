import serial
import time

# Openinig serial connection 
ser =serial.Serial('COM3', 9600, timeout=1)
time.sleep(2)  # wait for the serial connection to initialize

while True:
    line = ser.readline().decode('utf-8').rstrip()
    if line:
        try:
            ldr, temp, hum =map(float, line.split(','))
            print(f"LDR: {ldr}, Temperature: {temp}, Humidity: {hum}")
        except ValueError:
            print("Received malformed data:", line)