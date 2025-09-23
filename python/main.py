import serial
import time
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


def setup_serial(port: str, baud: int, timeout: float):
    ser = serial.Serial(port, baud, timeout=timeout)
    time.sleep(2)
    return ser


def read_serial(ser):
    try:
        line = ser.readline().decode('utf-8').rstrip()  # read serial input
        return line
    except Exception as e:
        print(f"Received malformed data: {e}")
        return None
    

def set_table_plot(fig: Figure, name: str, masterTab: tk.Frame, xlim: int):  # set up a single plot in a given tab
    ax = fig.add_subplot(111)
    line, = ax.plot([], [], label=name,)
    ax.set_xlim(xlim)
    ax.legend()
    ax.set_xlim(0, 100)

    canvas = FigureCanvasTkAgg(fig, master=masterTab)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    return {"axis": ax, "line": line, "canvas": canvas}


def setup_UI(root):
    notebook = ttk.Notebook(root)
    tab_val = ttk.Frame(notebook)
    tab_ldr = ttk.Frame(notebook)
    tab_temp = ttk.Frame(notebook)
    tab_humidity = ttk.Frame(notebook)

    notebook.add(tab_val, text='Values')
    notebook.add(tab_ldr, text='LDR')
    notebook.add(tab_temp, text='Temperature')
    notebook.add(tab_humidity, text='Humidity')
    notebook.pack(expand=True, fill='both')

    fig = Figure(figsize=(6, 6), dpi=100) 
    axs_ldr = fig.add_subplot(311)  # LDR
    axs_temp = fig.add_subplot(312)  # Temp
    axs_humidity = fig.add_subplot(313)  # Humidity

    canvas = FigureCanvasTkAgg(fig, master=tab_val)  
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    tab_figLDR = Figure(figsize=(6, 4), dpi=100) 
    tab_figTEMP = Figure(figsize=(6, 4), dpi=100) 
    tab_figHUMIDITY = Figure(figsize=(6, 4), dpi=100)

    line_ldr, = axs_ldr.plot([], [], label='LDR')
    line_temp, = axs_temp.plot([], [], label='Temp')
    line_humidity, = axs_humidity.plot([], [], label='Humidity')
    
    tab_ax = []
    tab_lines = []
    tab_canvas = []

    for name, fig, tab in zip(['LDR', 'Temp', 'Humidity'], [tab_figLDR, tab_figTEMP, tab_figHUMIDITY], [tab_ldr, tab_temp, tab_humidity]):
        plot = set_table_plot(fig, name, tab, 100)
        tab_ax.append(plot['axis'])
        tab_lines.append(plot['line'])
        tab_canvas.append(plot['canvas'])

    for ax in [axs_ldr, axs_temp, axs_humidity]:
        ax.legend()
        ax.set_xlim(0, 100)
        
    return {"fig": fig, "axes": (axs_ldr, axs_temp, axs_humidity),
            "lines": [line_ldr, line_temp, line_humidity],
            "canvas": canvas, "canvas_tabs": tab_canvas,
            "ax_tabs": tab_ax, "lines_tabs": tab_lines}


class DatabloggerApp:
    def __init__(self, root):
        self.ser = setup_serial("COM3", 9600, 1)
        
        # Initialize UI
        self.root = root
        
        UI = setup_UI(root)

        # set up main tab plot
        self.canvas = UI['canvas']
        self.axes = UI['axes']
        self.lines = UI['lines']

        # set up individual tabs plots
        self.tab_canvas = UI['canvas_tabs']
        self.tab_axes = UI['ax_tabs']
        self.tab_lines = UI['lines_tabs']

        self.val_history = [list() for _ in range(3)]  # ldr,temp,humidity
        self.errors = 0  # count serial errors in a row
        self.update_interval_ms = 200

        self.update()
    
    def update(self):
        line = read_serial(self.ser)
        if line:
            try:
                sensor = map(float, line.split(','))
                for i, val in enumerate(sensor):
                    self.val_history[i].append(val)
                self.errors = 0
            
            except ValueError:  # if malformed data received
                print("Received malformed data:", line)
                self.errors += 1
                if self.errors > 5:
                    print("Too many errors, stopping.")
                    self.ser.close()
                    self.root.quit()

        for data_line, val, ax, tab_line, tab_ax, tab_canvas in zip(self.lines, self.val_history, self.axes, self.tab_lines, self.tab_axes, self.tab_canvas):
            data_line.set_data(range(len(val[-100:])), val[-100:])  # change Artist of main tab
            
            tab_line.set_data(range(len(val[-100:])), val[-100:])  # change Artist of individual tab

            ax.draw_artist(data_line)  
            ax.relim()
            ax.autoscale()
            
            tab_ax.draw_artist(tab_line)
            tab_ax.relim()
            tab_ax.autoscale()
            tab_canvas.draw_idle()
    
        self.canvas.draw_idle()
        self.root.after(self.update_interval_ms, self.update)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Mini Datablogger")
    app = DatabloggerApp(root)
    root.mainloop()
