###This file contains the GUI code and the main loop of the project.
###All databse management code should be done in databse.py

#import GUI library
import tkinter as tk
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
        buttons = tk.Frame(master, relief=tk.RAISED, bd=2)
        # Creating open and save as buttons
        open_button = tk.Button(buttons, text="Open")
        save_button = tk.Button(buttons, text="Save As...")
        # Assiginging them to the grid and padding the borders
        # Sticky allows it to grow horizontally if the frame resizes
        open_button.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        save_button.grid(row=1, column=0, stick="ew", padx=5)
        # Assigning the buttons frame to the main window
        buttons.grid(row=0, column=0, sticky="ns")
        # Assigning the text grid to the main window
        txt.grid(row=0, column=1, sticky="nsew")


# --- main ---
root = tk.Tk()
gui = GuiWin(root)
root.mainloop()