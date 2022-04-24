from __future__ import annotations
from sre_parse import State
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
        self.widgets = []
        self.root = root

    def start_state(self, prev_state : GUIState, controller : StateController):
        """Start a state and initialize its interface

        Raises:
            NotImplementedError: Not implemented override
        """
        self.controller = controller
    
    def leave_state(self):
        """Tear down this state and delete all unique GUI elements

        Raises:
            NotImplementedError: Not implemented
        """
        for w in reversed(self.widgets):
            w.destroy()    
        #blank the list
        self.widgets = []      

class StateController:
    def change_state(self, new_state : GUIState):
        if(self.current_state != None):
            #call the code to tear down the old UI
            self.current_state.leave_state()
            last_state = self.current_state
            #change the current state
            self.current_state = new_state
            #initialize the new state
            self.current_state.start_state(last_state, self)

    def __init__(self, initial_state : GUIState = None):
        self.current_state = initial_state
        self.current_state.start_state(None, self)

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

    def start_state(self, prev_state : GUIState, controller : StateController):
        """Override
        """
        #call this first to get that ref planted
        super(ArticleSelectionState, self).start_state(prev_state, controller)
        #reference the state controller to change states with self.controller.change_state(newstate)
        
        books = Label(text=samplebooks(), justify=LEFT)
        books.grid(row=0, column=0)
        self.widgets.append(books)

        # Setting up the frame for text editing
        txt = Text(self.root)
        self.widgets.append(txt)
        # Assigning the text grid to the main window
        txt.grid(row=0, column=1, sticky="nsew")
        #txt.insert(END, db.get_articles())
    
    def leave_state(self):
        """Override
        """
        #Call the base teardown of all widgets
        super(ArticleSelectionState, self).leave_state()

