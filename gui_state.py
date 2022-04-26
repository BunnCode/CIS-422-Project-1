from __future__ import annotations
from sre_parse import State
#import datastructures file
import datastructures as ds
from tkinter import *
from tkinter import messagebox
from turtle import left
import database as db

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
        selected_option = StringVar(self.root)
        a_names = []
        if len(self.articles) == 0:
            self.articles.append("New Article")
            selected_option.set(self.articles[0])
            a_names.append("New Article")
        else:
            selected_option.set(self.articles[0].article_name)
            [a_names.append(x.article_name) for x in self.articles]
        drop_menu = OptionMenu(self.root, selected_option, *a_names)
        self.widgets.append(drop_menu)
        drop_menu.pack()
        select_button = Button(self.root, text="Select", command= lambda : self.select_article(selected_option.get()))
        self.widgets.append(select_button)
        select_button.pack()


    def leave_state(self):
        """Override
        """
        #Call the base teardown of all widgets
        super(ArticleSelectionState, self).leave_state()
    
    def select_article(self, option):
        if option == "New Article":
            self.controller.change_state(ArticleEditState(self.root, db.new_article("New Article")))
        else:
            load_a = None
            for x in self.articles:
                if x.article_name == option:
                    load_a = x
            self.controller.change_state(ArticleEditState(self.root, load_a))

class ArticleEditState(GUIState):
    """The text edit state
    """
    def __init__(self, root : Widget, articles):
        """Initialize the default state with some articles defined by params

        Args:
            root (Widget): Root of this GUI window 
            articles (list): Loaded articles. Defaults to []
        """
        self.articles = articles
        super(ArticleEditState, self).__init__(root)

    def start_state(self, prev_state : GUIState, controller : StateController):
        """Override
        """
        #call this first to get that ref planted
        super(ArticleEditState, self).start_state(prev_state, controller)
        #reference the state controller to change states with self.controller.change_state(newstate)
        


        # Setting up the frame for text editing
        top_frame = Frame(self.root)
        top_frame.pack(side= TOP, expand= True, fill=BOTH)
        text_frame = Frame(self.root)
        text_frame.pack(side= BOTTOM, expand= True, fill=BOTH)
        notes = Text(text_frame)
        artic_name = Entry(top_frame)
        ch_name = Entry(top_frame)
        if self.articles != None:
            notes.insert("end", self.articles.chapters[0].notes[0].note_text)
            artic_name.insert("end", self.articles.article_name)
            ch_name.insert("end", self.articles.chapters[0].title)
        self.widgets.append(notes)
        self.widgets.append(artic_name)
        self.widgets.append(ch_name)
        # Assigning the text grid to the main window
        
        artic_name.pack(expand = True, side = LEFT, fill= X)
        ch_name.pack(side = RIGHT, expand= True, fill= X)
        notes.pack(expand= True, fill= BOTH)
    
    def leave_state(self):
        """Override
        """
        #Call the base teardown of all widgets
        super(ArticleEditState, self).leave_state()

class ArticleQuizState(GUIState):
    """The quiz state
    """
    def __init__(self, root : Widget, articles = []):
        """Initialize the default state with some articles defined by params

        Args:
            root (Widget): Root of this GUI window 
            articles (list): Loaded articles. Defaults to []
        """
        self.articles = articles
        super(ArticleQuizState, self).__init__(root)

    def start_state(self, prev_state : GUIState, controller : StateController):
        """Override
        """
        #call this first to get that ref planted
        super(ArticleQuizState, self).start_state(prev_state, controller)
        #reference the state controller to change states with self.controller.change_state(newstate)
        

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
        super(ArticleQuizState, self).leave_state()