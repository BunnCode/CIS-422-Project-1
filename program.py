###This file contains the GUI code and the main loop of the project.
###All databse management code should be done in databse.py

#import GUI library
import doctest
from tkinter import *
from tkinter import messagebox
from turtle import left
#import database file
import database as db
#import datastructures file
import datastructures as ds
#import gui state file
import gui_state as gs

"""@package docstring
The main code for the GUI Program
"""

class GuiWin():
    """
    Creates the main window for the app
    """

    def __init__(self, root):
        """
        Main window constructor
        Input: self, The object pointer
        Input: root, The main window
        """
        # Setting the root variable to root
        # Titling the window "Basic GUI"
        self.root = root
        root.title("Basic GUI")
        # Resizing the rows and column of the frame
        self.widgets()
        
        articleSelectionState = gs.ArticleSelectionState(root, [])
        
        self.state_controller = gs.StateController(articleSelectionState)
        change_s = Button(text="edit mode", command=self.state_controller.change_state(gs.ArticleEditState(root, [])))
        change_s.pack()

        
    def newfile():
        x = 0

    def save():
        x = 0

    def openfile():
        x = 0

    def deletefile():
        x = 0
    
    def exitprogram(self):
        """
        Exits program with yes/no prompt
        Warns about unsaved data
        """
        option = messagebox.askyesno("WARNING", "Your unsaved data may be lost. Do you still want to exit?")
        if option:
            self.root.quit()
        else:
            return
        
    # Creating a menu bar
    def widgets(self):
        menubar = Menu(root)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="New")
        filemenu.add_command(label="Open")
        filemenu.add_command(label="Save")
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.exitprogram)
        #filemenu.add_command(label="Edit mode", command=self.change(state))
        menubar.add_cascade(label="File", menu=filemenu)
        

        #viewmenu = Menu(menubar, tearoff=0)
        #viewmenu.add_command(label="Toggle Dark Mode", command=self.theme)
        #menubar.add_cascade(label="View", menu=viewmenu)

        root.config(menu = menubar)

# --- main ---
try:
    root = Tk()
    GuiWin(root)
    root.mainloop()
except Exception as e:
    messagebox.showerror('Python Error', e)
"""This is an example of how to load all articles"""

"""This is an example of how to load a specific article by ID"""
#article = db.load_article(1)

