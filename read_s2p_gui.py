import tkinter as tk
from tkinter.filedialog import askopenfilename
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)

#To Do
#modify to plot multiple axes on the same figure
#having issues updating the canvas after updating the axes. line 52

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
        self.opt2_val.set("s21db")
        #canvas needs to be created after opt1_val and opt2_val have been initialized
        #and before trace calls change_dropdown)        
        canvas = self.create_canvas(file, 0, 2)
        print(self.files_axs.keys())
        print(self.files_axs.values())
        #create and place the labels 
        self.label1 = tk.Label(self, text="X axis").grid(row=0, column=1, sticky="nw")
        self.label2 = tk.Label(self, text="Y axis").grid(row = 1, column=1, sticky="w")
        #create and place the option menus. Use trace to track the currently selected option
        self.option1 = tk.OptionMenu(self, self.opt1_val, *Datum.attributes())
        self.option1.grid(row=0, column=0, sticky="nwe")
        self.option2 = tk.OptionMenu(self, self.opt2_val, *Datum.attributes())
        self.option2.grid(row=1, column=0, sticky="we")
        self.opt1_val.trace('w', lambda*_:self.change_dropdown(self.files_axs))
        self.opt2_val.trace('w', lambda*_:self.change_dropdown(self.files_axs))
        #trace lets the plot auto-update. For a vintage feel, this update button can created and placed:
    ##    self.update_button = tk.Button(frame, text="Update", command=lambda:change_dropdown(data, opt1_val.get(), opt2_val.get(), fname, canvas)).grid(row=2, column=0, sticky="we")
        
        

    def change_dropdown(self, fax_dict, *args):
        for file in fax_dict.keys(): #this allows for multiple canvases
            fax_dict[file].clear()
            ax = file.plot(self.opt1_val.get(), self.opt2_val.get(),fax_dict[file])
            fax_dict.update({file:ax})
            #plt.show()#this gives me what I want so the issue must be with the gui not displaying the new plot
            #plt.gcf()
            self.canvas.draw()  #OFFENDING LINE
            

    def create_canvas(self, file, row, col):
        #changing the weight of the cell the canvas is in gives it priority when resizing the window
        self.master.columnconfigure(col, weight = 1)
        self.master.rowconfigure(row, weight=1)
        #create the plot and get the figure object
        self.add_file(file)
        self.fig = plt.gcf()
        #create the canvas, display it, and place it
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=row, column=col, sticky="nsew")
        return self.canvas
    
    def add_file(self, file):
        ax = file.plot(self.opt1_val.get(), self.opt2_val.get())
        self.files_axs.update({file: ax})

    def __init__(self, master = None, fname = None):
        self.fname = fname
        self.files_axs = {}
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
    def plot_attributes(self, attr1, attr2, ax=None, **kwargs):
        x = self.list_attribute(attr1)
        y = self.list_attribute(attr2)
        if ax is None:
            fig, ax = plt.subplots() 
        ax.plot(x, y, **kwargs)
        return ax
    def plot(self, attr1, attr2, ax=None, **kwargs):
        ax = self.plot_attributes(attr1, attr2, **kwargs)
        ax.set_xlabel(attr1)
        ax.set_ylabel(attr2)
        #when the code can read multiple files the next line may be an issue
        ax.set_title(self.fname)
        return ax
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
