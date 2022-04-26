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

        #Initialize article tracking with a delay of 5 seconds between validations
        #db.ArticleValidator.initialize_tracking(5)
        


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
        #txt.insert(tk.END, db.get_articles())
        """This is an example of how to load a specific article by ID"""
        #article = db.load_article(1)
        new_article = db.new_article("How to tame dragons v2")
        new_chapter = db.new_chapter(new_article, "Choosing a bridle", 0)
        new_question = db.new_question(new_article, new_chapter, "What makes a good bridle?", "it's up to personal preference")
        new_quiz_attempt = db.record_quiz_attempt(new_article, 10, 10)
        new_note = db.new_note(new_article, new_chapter, 1)

        """examples of how to use stuff on """
        new_article.article_name = "new name"
        db.save_article(new_article)
        #db.save_chapter(new_article, new_chapter)
        #db.save_question(new_article, new_question)
        #db.save_note(new_article, new_note)
        db.delete_question(new_article, new_chapter, new_question)
        db.delete_note(new_article, new_chapter, new_note)
        db.delete_article(new_article)
        tomato = False
# --- main ---
#try:
root = tk.Tk()
gui = GuiWin(root)
root.mainloop()
#except Exception as e:
#    messagebox.showerror('Python Error', e)