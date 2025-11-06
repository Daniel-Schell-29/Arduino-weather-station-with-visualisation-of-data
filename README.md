# Arduino-weather-station-with-visualisation-of-data
This project records enviromental data(temperature, humidity and brightness) using an Arduino Uno and visualises it in a real-time python interface.
This project makes a complete data pipeline, from sensor input through serial communication to live data visualisation.

## Features
- real time visualisation of data
- Tab UI: *a tab showing all values and 3 seperate tabs showing each individuall value*
- Serial coumminication with error cases
- modular code(easily expandable)

## System Overview
The arduino reads the sensor data and sends it to the PC in a CSV Style over the serial connection. 
The Python script reads the data using **pySerial**, parses it, and creates a live graph using **Matplotlib** and **tkinter**.

## Hardware used
- Arduino Uno R3
- *DHT11 Temperature and Humidity sensor*
- *Photo resistor*
- USB Connection
- Breadboard



