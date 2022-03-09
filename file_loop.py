from tkinter.filedialog import askdirectory
import os
'''
a template script to loop through the contents of a folder.
'''
def main():
    dirname = askdirectory() #opens a dialog box and asks for a folder
    file_loop(dirname)

def file_loop(dirname):
    files = os.listdir(dirname) #lists folder contents
    for file in files: #loops through contents
        do_thing(file)

def do_thing(file):
    print(file) #your code here 

if __name__ == '__main__':
    main()
    
