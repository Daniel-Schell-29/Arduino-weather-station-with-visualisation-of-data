import serial
import time
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure


def setupSerial(port=str,baud= int, timeout=float):
    ser =serial.Serial(port,baud, timeout=timeout)
    time.sleep(2)
    return ser

def readSerial(ser):
    try:
        line = ser.readline().decode('utf-8').rstrip()  #read serial input
        return line
    except Exception as e:
        print("Received malformed data: {e}")
        return None

def set_table_plot(fig=Figure(),name=str,masterTab=tk.Frame,xlim=int): #set up a single plot in a given tab
    ax=fig.add_subplot(111)
    line,= ax.plot([], [], label=name,)
    ax.set_xlim(xlim)
    ax.legend()
    ax.set_xlim(0, 100)

    canvas= FigureCanvasTkAgg(fig, master=masterTab)
    canvas_widget= canvas.get_tk_widget()
    canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    return {"axis":ax,"line":line,"canvas":canvas}



def setupUI(root):
        notebook = ttk.Notebook(root)
        tabVAL= ttk.Frame(notebook)
        tabLDR= ttk.Frame(notebook)
        tabTEMP= ttk.Frame(notebook)
        tabHUMIDITY= ttk.Frame(notebook)

        notebook.add(tabVAL, text='Values')
        notebook.add(tabLDR, text='LDR')
        notebook.add(tabTEMP, text='Temperature')
        notebook.add(tabHUMIDITY, text='Humidity')
        notebook.pack(expand=True, fill='both')

        fig= Figure(figsize=(6, 6), dpi=100) 
        axsLDR = fig.add_subplot(311) #LDR
        axsTEMP = fig.add_subplot(312) #Temp
        axsHUMIDITY = fig.add_subplot(313) #Humidity

        

        canvas= FigureCanvasTkAgg(fig, master=tabVAL)  
        canvas_widget= canvas.get_tk_widget()
        canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        tab_figLDR= Figure(figsize=(6, 4), dpi=100) 
        tab_figTEMP= Figure(figsize=(6, 4), dpi=100) 
        tab_figHUMIDITY= Figure(figsize=(6, 4), dpi=100)


        lineLDR, = axsLDR.plot([], [], label='LDR')
        lineTEMP, = axsTEMP.plot([], [], label='Temp')
        lineHUMDITY, = axsHUMIDITY.plot([], [], label='Humidity')
        
        tab_ax=[]
        tab_lines=[]
        tab_canvas=[]

        for name,fig,tab in zip(['LDR','Temp','Humidity'],[tab_figLDR,tab_figTEMP,tab_figHUMIDITY],[tabLDR,tabTEMP,tabHUMIDITY]): 
            plot= set_table_plot(fig,name,tab,100)
            tab_ax.append(plot['axis'])
            tab_lines.append(plot['line'])
            tab_canvas.append(plot['canvas'])
 
        for ax in [axsLDR, axsTEMP, axsHUMIDITY]:
            ax.legend()
            ax.set_xlim(0, 100)
            

        return {"fig" :fig,"axes" :(axsLDR, axsTEMP, axsHUMIDITY), "lines":[lineLDR, lineTEMP, lineHUMDITY],"canvas": canvas, "canvasTabs": tab_canvas, "axTabs": tab_ax, "linesTabs": tab_lines}


class DatabloggerApp:
    def __init__(self, root):
        self.ser = setupSerial("COM3", 9600, 1)
        
        # Initialize UI
        self.root = root
        
        UI= setupUI(root)

        #set up main tab plot
        self.canvas= UI['canvas']
        self.axes= UI['axes']
        self.lines= UI['lines']

        #set up individual tabs plots
        self.tab_canvas= UI['canvasTabs']
        self.tab_axes= UI['axTabs']
        self.tab_lines= UI['linesTabs']

        self.val_history=[list() for _ in range(3)]#ldr,temp,humidity
        self.errors=0 #count serial errors in a row
        self.update_interval_ms = 200  

        self.update()
    
    def update(self):
        line = readSerial(self.ser)
        if line:
            try:
                sensor= map(float, line.split(','))
                for i, val in enumerate(sensor):
                    self.val_history[i].append(val)
                self.errors=0
            
            except ValueError:  #if malformed data received
                print("Received malformed data:", line)
                self.errors += 1
                if self.errors > 5:
                    print("Too many errors, stopping.")
                    self.ser.close()
                    self.root.quit()

        for dataline,val,ax,tabLine,tabAx,tabCanvas in zip(self.lines, self.val_history, self.axes, self.tab_lines,self.tab_axes,self.tab_canvas):
            dataline.set_data(range(len(val[-100:])),val[-100:])    #change Artist of main tab
            
            tabLine.set_data(range(len(val[-100:])),val[-100:]) #change Artist of individual tab

            ax.draw_artist(dataline)    
            ax.relim()
            ax.autoscale()
            
            tabAx.draw_artist(tabLine)
            tabAx.relim()
            tabAx.autoscale()
            tabCanvas.draw_idle()
    
        self.canvas.draw_idle()
        self.root.after(self.update_interval_ms, self.update)


if __name__ == "__main__":
    root= tk.Tk()
    root.title("Mini Datablogger")
    app= DatabloggerApp(root)
    root.mainloop()
