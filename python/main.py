import serial
import time
import matplotlib.pyplot as plt


# Opening serial connection 
ser =serial.Serial('COM3', 9600, timeout=1)
time.sleep(2)  # wait for the serial connection to initialize

val_history=[list() for _ in range(3)]#ldr,temp,humidity
labels= ['LDR','Temp','Humidity']

plt.ion()
fig, axs = plt.subplots(3, 1, figsize=(8, 8)) #3 rows, 1 column

errors=0 #count errors in a row
while True:
    line = ser.readline().decode('utf-8').rstrip()  #read serial input
    if line:
        try:
            
            sensor =list( map(float, line.split(',')))  #put serial input in list
            for data_list, val in zip(val_history, sensor):
                data_list.append(val)
            errors=0 #reset error count
            print(val_history)
            

        except ValueError:  #stop programm if data is malformed
            print("Received malformed data:", line)
            errors+=1
            if errors>5: #after more than 5 errors in a row stop programm
                print("Too many errors, stopping.")
                ser.close()
                break
            continue

  
        for i,( data_list, name) in enumerate(zip(val_history , labels)):  #add Data to each plot
            axs[i].clear() 
            axs[i].plot(data_list[-100:],label=name)
            axs[i].legend()
            plt.pause(0.1)
            
            
        if plt.get_fignums()== []:   #stop porgramm when plot window closed
            ser.close()
            break
