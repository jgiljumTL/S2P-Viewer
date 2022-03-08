import tkinter as tk
from tkinter.filedialog import askopenfilename
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)

#To Do
#put the GUI into classes, apparently that is best practice

def main():
    root = tk.Tk()
    fname = askopenfilename()
    root.wm_title(fname)
    header, data = read_s2p(fname)
    
    frame = tk.Frame(root)
    frame.grid(row=0, column=0, sticky="n")
    
    opt1_val = tk.StringVar()
    opt1_val.set("freq")
    opt2_val = tk.StringVar()
    opt2_val.set("s11db")
    
    label1 = tk.Label(frame, text="X axis").grid(row=0, column=1, sticky="nw")
    label2 = tk.Label(frame, text="Y axis").grid(row = 1, column=1, sticky="w")
    
    option1 = tk.OptionMenu(frame, opt1_val, *Datum.attributes())
    option1.grid(row=0, column=0, sticky="nwe")
    option2 = tk.OptionMenu(frame, opt2_val, *Datum.attributes())
    option2.grid(row=1, column=0, sticky="we")
    opt1_val.trace('w', lambda*_:change_dropdown(data, opt1_val.get(), opt2_val.get(), fname, canvas))
    opt2_val.trace('w', lambda*_:change_dropdown(data, opt1_val.get(), opt2_val.get(), fname, canvas))
##    update_button = tk.Button(frame, text="Update", command=lambda:change_dropdown(data, opt1_val.get(), opt2_val.get(), fname, canvas)).grid(row=2, column=0, sticky="we")

    root.columnconfigure(2, weight = 1)
    root.rowconfigure(0, weight=1)

    plot(data, opt1_val.get(), opt2_val.get(), fname)
    fig = plt.gcf()
    
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=2, sticky="nsew")

    

    
    root.mainloop()
def change_dropdown(data, opt1, opt2, fname, canvas, *args):
    plt.clf()
    plot(data, opt1, opt2, fname)
    canvas.draw()
    
def read_s2p(fname):
    with open(fname, 'r') as f:
        lines = f.readlines()

    count = 0
    header = []
    header_length = 9 #hardcoded
    data = []
    for line in lines:
        if count < header_length - 1:
            header.append(line)
        else:
            freq, s11db, s11a, s21db, s21a, s12db, s12a, s22db, s22a = line.split()
            temp = Datum(freq, s11db, s11a, s21db, s21a, s12db, s12a, s22db, s22a)
            data.append(temp)
        count += 1
    return header, data

def list_attribute(data, attr):
    return [getattr(datum, attr) for datum in data]

def plot_attributes(data, attr1, attr2, **kwargs):
    x = list_attribute(data, attr1)
    y = list_attribute(data, attr2)

    plot2d = plt.plot(x, y, **kwargs)
    return

def plot(data, attr1, attr2, fname, **kwargs):
    plot2d = plot_attributes(data, attr1, attr2, color='green')
    plt.xlabel(attr1)
    plt.ylabel(attr2)
    plt.title(fname)

class Datum:
    def __init__(self, freq, s11db, s11a, s21db, s21a, s12db, s12a, s22db, s22a ):
        self.freq = float(freq)
        self.s11db = float(s11db)
        self.s11a = float(s11a)
        self.s21db = float(s21db)
        self.s21a = float(s21a)
        self.s12db = float(s12db)
        self.s12a = float(s12a)
        self.s22db = float(s22db)
        self.s22a = float(s22a)
    def __repr__(self):
        return "<Datum freq:{freq} s11db:{s11db} s11a:{s11a} s21db:{s21db} s12a:{s12a} s22db:{s22db} s22a:{s22a}".format(freq = self.freq, s11db = self.s11db, s11a = self.s11a, s21db = self.s21db, s21a = self.s21a, s12db = self.s12db, s12a=self.s12a, s22db=self.s22db, s22a=self.s22a)
    def attributes():
        return ["freq", "s11db", "s11a", "s21db", "s21a", "s12db", "s12a", "s22db", "s22a"]

if __name__ == '__main__':
    main()
