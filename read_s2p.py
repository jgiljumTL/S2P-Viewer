import tkinter as tk
from tkinter.filedialog import askopenfilename
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)

#To Do
#put plot into a gui to allow for changing the plot on the fly

def main():
    root = tk.Tk()
    fname = askopenfilename()
    root.wm_title(fname)
    header, data = read_s2p(fname)
    
    attr1 = "freq"
    attr2 = "s11db"
    
    plot(data, attr1, attr2, fname)
    fig = plt.gcf()
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    root.mainloop()

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


if __name__ == '__main__':
    main()
