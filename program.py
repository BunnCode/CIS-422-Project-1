###This file contains the GUI code and the main loop of the project.
###All databse management code should be done in databse.py

#import GUI library
from doctest import master
from tkinter import *
from tkinter import messagebox
from turtle import left
#import database file
import database as db
#import datastructures file
import datastructures as ds

"""@package docstring
The main code for the GUI Program
"""
class GuiWin():
    """
    Creates the main window for the app
    """
    def __init__(self, master):
        """
        Main window constructor
        Input: self, The object pointer
        Input: master, The main window
        """
        # Setting the master variable to master
        # Titling the window "Basic GUI"
        self.master = master
        master.title("Basic GUI")

        # Resizing the rows and column of the frame
        master.rowconfigure(0, minsize=800, weight=1)
        master.columnconfigure(1, minsize=800, weight=1)
        self.widgets()
        books = Label(text=self.samplebooks(), justify=LEFT)
        books.grid(row=0, column=0)

        # Setting up the frame for text editing
        txt = Text(master)
        # Assigning the text grid to the main window
        txt.grid(row=0, column=1, sticky="nsew")
        #txt.insert(END, db.get_articles())

    def newfile():
        x = 0

    def samplebooks(self):
        txt = ""
        for x in range(10):
            txt = txt + "Yikes\n"
        return txt
    

    def save():
        x = 0

    def openfile():
        x = 0

    def deletefile():
        x = 0
    
    def exitprogram(self):
        self.master.quit()
    
    def widgets(self):
        menubar = Menu(master)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="New")
        filemenu.add_command(label="Open")
        filemenu.add_command(label="Save")
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.exitprogram)
        menubar.add_cascade(label="File", menu=filemenu)
        root.config(menu = menubar)

        #viewmenu = tk.Menu(menubar, tearoff=0)


# --- main ---
try:
    root = Tk()
    gui = GuiWin(root)
    root.mainloop()
except Exception as e:
    messagebox.showerror('Python Error', e)
"""This is an example of how to load all articles"""

"""This is an example of how to load a specific article by ID"""
article = db.load_article(1)

