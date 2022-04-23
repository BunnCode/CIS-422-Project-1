###This file contains the GUI code and the main loop of the project.
###All databse management code should be done in databse.py

#import GUI library
import tkinter as tk
from tkinter import messagebox
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
        input: TK variable
        output: None
        """
        # Setting the master variable to master
        # Titling the window "Basic GUI"
        self.master = master
        master.title("Basic GUI")

        # Resizing the rows and column of the frame
        master.rowconfigure(0, minsize=800, weight=1)
        master.columnconfigure(1, minsize=800, weight=1)

        # Setting up the frame for text editing
        txt = tk.Text(master)
        # Creating the frame for buttons
        b_frame = tk.Frame(master, relief=tk.RAISED, bd=2)
        # Creating load and save as buttons
        new_file = tk.Button(b_frame, text="New")
        load_button = tk.Button(b_frame, text="Load")
        save_button = tk.Button(b_frame, text="Save As...")
        
        # Assiginging them to the grid and padding the borders
        # Sticky allows it to grow horizontally if the frame resizes
        new_file.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        load_button.grid(row=1, column=0, sticky="ew", padx=5)
        save_button.grid(row=2, column=0, stick="ew", padx=5)
        # Assigning the b_frame to the main window
        b_frame.grid(row=0, column=0, sticky="ns")
        # Assigning the text grid to the main window
        txt.grid(row=0, column=1, sticky="nsew")

        """This is an example of how to load all articles"""
        txt.insert(tk.END, db.get_articles())
        """This is an example of how to load a specific article by ID"""
        article = db.load_article(1)

# --- main ---
try:
    root = tk.Tk()
    gui = GuiWin(root)
    root.mainloop()
except Exception as e:
    messagebox.showerror('Python Error', e)