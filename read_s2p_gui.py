import tkinter as tk
from tkinter.filedialog import askopenfilename
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)

#To Do
#refactor application class now that file class exists

def main():
    root = tk.Tk()
    fname = askopenfilename()
    root.wm_title(fname)
    app = Application(master=root, fname=fname)
    app.mainloop()


class Application(tk.Frame):
    def create_widgets(self):
        file = File(self.fname)
        
        #initialize string variables and set deafults for drop down menus
        self.opt1_val = tk.StringVar()
        self.opt1_val.set("freq")
        self.opt2_val = tk.StringVar()
        self.opt2_val.set("s11db")
        #canvas needs to be created after opt1_val and opt2_val have been initialized
        #and before trace calls change_dropdown)        
        canvas1 = self.create_canvas(file, 0, 2)
        canvas2 = self.create_canvas(file, 1, 2)
        canvases = [canvas1, canvas2]
        #create and place the labels 
        self.label1 = tk.Label(self, text="X axis").grid(row=0, column=1, sticky="nw")
        self.label2 = tk.Label(self, text="Y axis").grid(row = 1, column=1, sticky="w")
        #create and place the option menus. Use trace to track the currently selected option
        self.option1 = tk.OptionMenu(self, self.opt1_val, *Datum.attributes())
        self.option1.grid(row=0, column=0, sticky="nwe")
        self.option2 = tk.OptionMenu(self, self.opt2_val, *Datum.attributes())
        self.option2.grid(row=1, column=0, sticky="we")
        self.opt1_val.trace('w', lambda*_:self.change_dropdown(file, canvases))
        self.opt2_val.trace('w', lambda*_:self.change_dropdown(file, canvases))
        #trace lets the plot auto-update. For a vintage feel, this update button can created and placed:
    ##    self.update_button = tk.Button(frame, text="Update", command=lambda:change_dropdown(data, opt1_val.get(), opt2_val.get(), fname, canvas)).grid(row=2, column=0, sticky="we")
        
        

    def change_dropdown(self, file, canvases, *args):
        for canvas in canvases:
            plt.clf()
            file.plot(self.opt1_val.get(), self.opt2_val.get())
            canvas.draw()

    def create_canvas(self, file, row, col):
        #changing the weight of the cell the canvas is in gives it priority when resizing the window
        self.master.columnconfigure(col, weight = 1)
        self.master.rowconfigure(row, weight=1)
        #create the plot and get the figure object
        file.plot(self.opt1_val.get(), self.opt2_val.get())
        self.fig = plt.gcf()
        #create the canvas, display it, and place it
        canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        canvas.draw()
        canvas.get_tk_widget().grid(row=row, column=col, sticky="nsew")
        return canvas

    def __init__(self, master = None, fname = None):
        self.fname = fname
        tk.Frame.__init__(self, master)
        self.grid(row=0, column=0, sticky="n")
        self.create_widgets()
        

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

class File:
    def __init__(self, fname):
        self.fname = fname
        self.header, self.data = self.read_s2p(self.fname)
    def list_attribute(self, attr):
        return [getattr(datum, attr) for datum in self.data]
    def plot_attributes(self, attr1, attr2, **kwargs):
        x = self.list_attribute(attr1)
        y = self.list_attribute(attr2)
        plot2d = plt.plot(x, y, **kwargs)
        return
    def plot(self, attr1, attr2, **kwargs):
        plot2d = self.plot_attributes(attr1, attr2, color='green')
        plt.xlabel(attr1)
        plt.ylabel(attr2)
        plt.title(self.fname)
    def read_s2p(self, fname):
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

if __name__ == '__main__':
    main()
