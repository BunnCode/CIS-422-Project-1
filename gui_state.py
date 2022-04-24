#import datastructures file
import datastructures as ds
from tkinter import *
from tkinter import messagebox
from turtle import left

"""Temporary, remove when done"""
def samplebooks():
    txt = ""
    for x in range(10):
        txt = txt + "Yikes\n"
    return txt

"""end temp"""

class GUIState:
    """Defines a GUI state. 
    """
    def __init__(self, root : Widget):
        self.root = root

    def start_state(self):
        """Start a state and initialize its interface

        Raises:
            NotImplementedError: Not implemented override
        """
        #code to spawn GUI will be overridden here
        raise NotImplementedError()
    
    def leave_state(self):
        """Tear down this state and delete all unique GUI elements

        Raises:
            NotImplementedError: Not implemented
        """
        #code to tear down GUI will be overridden here
        raise NotImplementedError()

class StateController:
    def change_state(self, new_state : GUIState):
        if(self.current_state != None):
            #call the code to tear down the old UI
            self.current_state.leave_state()
            #change the current state
            self.current_state = new_state
            #initialize the new state
            self.current_state.start_state()

    def __init__(self, initial_state : GUIState = None):
        self.current_state = initial_state
        self.current_state.start_state()

class ArticleSelectionState(GUIState):
    """The default state
    """
    def __init__(self, root : Widget, articles = []):
        """Initialize the default state with some articles defined by params

        Args:
            root (Widget): Root of this GUI window 
            articles (list): Loaded articles. Defaults to []
        """
        self.articles = articles
        super(ArticleSelectionState, self).__init__(root)

    def start_state(self):
        """Override
        """
        books = Label(text=samplebooks(), justify=LEFT)
        books.grid(row=0, column=0)

        # Setting up the frame for text editing
        txt = Text(self.root)
        # Assigning the text grid to the main window
        txt.grid(row=0, column=1, sticky="nsew")
        #txt.insert(END, db.get_articles())

