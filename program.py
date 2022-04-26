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
        # Loading articles from server
        self.artic_list = []
        # sending articles into state machine
        articleSelectionState = gs.ArticleSelectionState(root, [])
        # Creating state controller to start the gui
        self.state_controller = gs.StateController(articleSelectionState)
        # Creating the menu bar
        self.menu_bar()

        

        
    def newfile(self):
        """
        Creates a new article to be edited

        Args: None

        Returns: None
        """
        # Creates an article with a default name
        artic = db.new_article("New Article")
        
        db.new_chapter(artic, "New chapter", )
        # Changes state to edit new article
        self.state_controller.change_state(gs.ArticleEditState(self.root, artic))

    #def new_chapter(self):
        """
        Creates a new chapter in current article

        Args: None

        Returns: None
        """
        #if(isinstance(self.state_controller.current_state, gs.ArticleEditState)):
            #self.state_controller.current_state.

    def save(self):
        """ Saves current article being worked on

        Args: None

        Return: None
        """
        # Checks if current state is article edit state
        if isinstance(self.state_controller.current_state, gs.ArticleEditState):
            # Grabs the article being worked on
            artic = self.state_controller.current_state.articles
            # saves is
            db.save_article(artic)
        else:
            return

    def openfile(self, article_item):
        """ Loads an article to be edited
        Args: article_item : Article

        Returns: None
        """
        self.state_controller.change_state(gs.ArticleEditState(self.root, article_item))

    def deletefile(self):
        """ Prompts user if they want to delete the current item
        Args: None

        Returns: None
        """
        if(isinstance(self.state_controller.current_state, gs.ArticleEditState)):
            option = messagebox.askyesno("WARNING", "You are about to delete this entry. Do you still want to continue?")
            if option:
                db.delete_article(self.state_controller.current_state.article)
                self.state_controller.change_state(gs.ArticleSelectionState(self.root, self.artic_list))
        else:
            return
    
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
    def menu_bar(self):
        """ Creates the menu bar of the program
        Args: None
        Returns: None
        """
        menubar = Menu(self.root)
        filemenu = Menu(menubar, tearoff=0)
        new_menu = Menu(filemenu, tearoff=0)
        new_menu.add_command(label="Book", command= lambda : self.newfile())
        new_menu.add_command(label="Chapter", command= lambda : self.new_chapter())
        recent_menu = Menu(filemenu, tearoff=0)
        for item in self.artic_list:
            new_menu.add_command(label=item.article_name, command=self.openfile(item))
        filemenu.add_cascade(label="New", menu=new_menu)
        filemenu.add_cascade(label="Open", menu=recent_menu)
        filemenu.add_command(label="Save", command=self.save)
        filemenu.add_separator()
        filemenu.add_command(label="Delete", command=self.deletefile())
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command= lambda : self.exitprogram)

        menubar.add_cascade(label="File", menu=filemenu)
        

        edit_menu = Menu(menubar, tearoff=0)
        edit_menu.add_command(label="yeet")
        menubar.add_cascade(label="Edit", menu=edit_menu)

        self.root.config(menu = menubar)

# --- main ---
try:
    root = Tk()
    GuiWin(root)
    root.mainloop()
except Exception as e:
    messagebox.showerror('Python Error', e)


