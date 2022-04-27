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
        artic_dict = db.get_articles()
        #print(artic_dict)
        # Getting the actual article objects from the server
        self.artic_list = []
        for x in artic_dict:
            self.artic_list.append(db.load_article(x.get("article_id")))
        # sending articles into state machine
        articleSelectionState = gs.ArticleSelectionState(root, self.artic_list)
        # Creating state controller to start the gui
        self.state_controller = gs.StateController(articleSelectionState)
        # Creating the menu bar
        self.menu_bar()

        
    def update_list(self):
        """ Updates article list
        Args: None

        Returns: None
        """
        data_articles = db.get_articles()
        #print(data_articles)
        # clears the article list
        self.artic_list.clear()
        # loading the srticles into the list
        for x in data_articles:
            self.artic_list.append(db.load_article(x.get("article_id")))
        
    def newfile(self):
        """
        Creates a new article to be edited

        Args: None

        Returns: None
        """
        # Creates an article with a default name
        artic = db.new_article("New Article")
        self.new_chapter(artic)
        # Changes state to edit new article
        self.state_controller.change_state(gs.ArticleEditState(self.root, artic))

    def new_chapter(self, article):
        """
        Creates a new chapter in current article

        Args: None

        Returns: None
        """
        if(isinstance(self.state_controller.current_state, gs.ArticleEditState)):
            db.new_chapter(self.state_controller.current_state.articles, "New Chapter", self.state_controller.current_state.current_chap + 1)
            db.new_note(article, article.chapters[-1], 1)

    def save(self):
        """ Saves current article being worked on

        Args: None

        Return: None
        """
        # Checks if current state is article edit state
        if isinstance(self.state_controller.current_state, gs.ArticleEditState):
            # Grabs the article being worked on
            saving_artic = self.state_controller.current_state.articles
            
            #print(saving_artic)
            # Updates the name of the article
            saving_artic.article_name = self.state_controller.current_state.widgets[1].get()
            # updates the chapter being worked on
            print(saving_artic.chapters)
            print(saving_artic.chapters[self.state_controller.current_state.current_chap])
            print(self.state_controller.current_state.widgets[2].get())
            saving_artic.chapters[self.state_controller.current_state.current_chap].title = self.state_controller.current_state.widgets[2].get()
            saving_artic.chapters[self.state_controller.current_state.current_chap].notes[0]["note_text"] = self.state_controller.current_state.widgets[0].get("1.0", "end")
            # saves it to database
            db.save_article(saving_artic)
        else:
            return

    def home(self):
        """ Returns to the selection screen
        Args: article_item : Article

        Returns: None
        """
        # Saves the article before changing back
        self.save()
        # Updates article list
        self.update_list()
        # Changes state
        self.state_controller.change_state(gs.ArticleSelectionState(self.root, self.artic_list))

    def deletefile(self):
        """ Prompts user if they want to delete the current item
        Args: None

        Returns: None
        """
        if(isinstance(self.state_controller.current_state, gs.ArticleEditState)):
            option = messagebox.askyesno("WARNING", "You are about to delete this entry. Do you still want to continue?")
            if option:
                # tells the article to get deleted from db
                db.delete_article(self.state_controller.current_state.articles)
                # calls update list to update the article list
                self.update_list()
                # Updates the state back to the initial
                self.state_controller.change_state(gs.ArticleSelectionState(self.root, self.artic_list))
        else:
            return

    def clear_db(self):
        """
            Only Press in case of emergency
            Clears the entire Data base

            Args: None

        """
        option = messagebox.askyesno("WARNING", "You are about to delete all saved files. Do you still want to continue?")
        if option:
            for x in self.artic_list:
                db.delete_article(x)
        # calls update list to update the article list
            self.update_list()
        # Updates the state back to the initial
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
        # Initial setting of the menu bar
        menubar = Menu(self.root)
        # All options under file
        filemenu = Menu(menubar, tearoff=0)
        # Sub menu to make new book or chapter
        new_menu = Menu(filemenu, tearoff=0)
        # Items to make new books and chapter
        new_menu.add_command(label="Book", command= lambda : self.newfile())
        new_menu.add_command(label="Chapter", command= lambda : self.new_chapter(self.state_controller.current_state.articles))
        # Returns to selection state
        filemenu.add_command(label="Home", command= lambda : self.home())
        # New menu with sub menu options
        filemenu.add_cascade(label="New", menu=new_menu)
        # Saves the current article
        filemenu.add_command(label="Save", command= lambda : self.save())
        filemenu.add_separator()
        # Deletes current Article
        filemenu.add_command(label="Delete", command= lambda : self.deletefile())
        filemenu.add_separator()
        filemenu.add_command(label="WIPE DATA BASE", foreground="red", command= lambda : self.clear_db())
        filemenu.add_separator()
        # Exits the program
        filemenu.add_command(label="Exit", command=self.exitprogram)

        menubar.add_cascade(label="File", menu=filemenu)

        self.root.config(menu = menubar)

# --- main ---
try:
    root = Tk()
    GuiWin(root)
    root.mainloop()
except Exception as e:
    messagebox.showerror('Python Error', e)


