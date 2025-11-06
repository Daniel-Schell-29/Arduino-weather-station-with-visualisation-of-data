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
- *Light dependent resistor*
- USB Connection
- Breadboard

### Build:
![Picture of Circuit](/docs/Circuit Picture.jpg)

## How to run it
To run the project follow these steps:
- Have Python 3.9 or higher installed
- Build the curcuit and connect it to your PC
- Change the COM in the py script to the COM your Arduino uses
- Upload the ![main.ino script](/arduino code/main.ino) to your arduino
- run the ![main.py script](/python/main.py)
- open the new window to see the values


