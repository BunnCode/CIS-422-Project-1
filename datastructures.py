from __future__ import annotations
import json
import re
from typing import Dict


class Serializable:
    #prefix given to serializable class names
    __PREFIX = "[s]"
    def __init__(self, vardict = []):
        """Converts from a dictionary to a serializable object

        Args:
            vardict (dict): Dictionary to process. Defaults to [].
        """

         #Iterate over attribute names
        for varname in iter(vardict):
            #pull out value
            value = vardict[varname]
            #Detect serialized objects by checking for the prefix
            if(varname.startswith(Serializable.__PREFIX)):
                #if we find it, unpack the serialized object (executes recursively)
                value = Serializable(value)
                #remove the prefix before setting the attr
                varname = varname.replace(Serializable.__PREFIX, "")

            #Set attribute 
            attr = setattr(self, varname, value)

    @staticmethod
    def from_json(jsonstr = "") -> Serializable:
        """Initialize serializable object from json

        Args:
            jsonstr (str, optional): JSON to parse. Defaults to "".

        Returns:
            Serializable: The deserialized object
        """

        #load attribute dictionary
        attrs = json.loads(jsonstr)
        return Serializable(attrs)

    def to_dict(self) -> Dict:
        """convert this serializable object to a dictionary
        
        Returns:
            Dict: the dictionary representation of this Serializable Object
        """
        
        #Get all members of this class, and then filter out default attributes and functions, leaving only variable names
        vars = [varname for varname in dir(self) if not "__" in varname and not callable(getattr(self, varname))]
        #Variable names are stored in a dict 
        vardict = {}
        for varname in vars:
            #attribute we are accessing
            attr = getattr(self, varname)

            #dereference value
            value = attr
            #Convert Serializable objects to dictionaries (recursion inits here)
            if  issubclass(type(attr), Serializable):
                #Swap out the serializable object for its dict representation
                value = attr.to_dict()
                #Add annotation to the type name for later deserialization
                varname = Serializable.__PREFIX + varname
            
            #Ensure that Serializables in lists are properly converted
            if type(value) is list:
                for i, item in enumerate(value):
                    if issubclass(type(item), Serializable):
                        value[i] = value[i].to_dict()
            
            #Ensure that Serializables in dicts are properly converted
            if type(value) is dict:
                for key in value:
                    if issubclass(type(value[key]), Serializable):
                        value[key] = value[key].to_dict()

            #add attribute to dict
            vardict[varname] = value

        return vardict
            

    """Return JSON
    """
    def __str__(self) -> str:
        outputdict = self.to_dict()
        return json.dumps(outputdict)

"""
General notes about what's happening here as far as succession

Chapter
|->Heading
|   |->Subheading
|   |   |->Page
|   |       |->Note
|   |       |->Note
|   |       |...
|   |->Note
|   |->Note
|   |...
|->Question   

Chapters store page numbers for sorting purposes but are not children of pages
"""
class Note(Serializable):
    def __init__(self, note_text : str):
        """A note on a specific page

        Args:
            note_text (str): The note 
        """
        self.note_text = note_text
        super(Note, self).__init__()

class Heading(Serializable):
    def __init__(self, name : str):
        """A heading in a specific chapter

        Args:
            name (str): Name of the heading
        """
        #Name of the heading
        self.name = name
        #Subheadings
        self.subheadings = []
        #Notes stored beneath this heading
        self.notes = []
        super(Heading, self).__init__()
    
    def add_subheading(self, name : str):
        """Add a subheading to this heading

        Args:
            name (str): Subheading name
        """
        self.subheadings.append(name)

class Page(Serializable):
    def __init__(self, page_num : str):
        """A page beneath a certain heading. 

        Args:
            page_num (str): page number
        """
        self.notes = []
        super(Page, self).__init__()
    
    def add_note(self, note : str):
        """add a new note to the page

        Args:
            note (str): text to add
        """
        self.notes.append(Note(note))
    
class Question(Serializable):
     def __init__(self, question_text : str):
        """A question about a certain chapter

        Args:
            note_text (str): The question to be answered
        """
        #Text in this note
        self.question_text = question_text
        super(Question, self).__init__()

class Chapter(Serializable):
    def __init__(self, page_num : int, title : str):
        """Initialize a new chapter in a specific article.

        Args:
            page_num (int): page number this chapter appears in
            title (str): title of this chapter
        """
        self.title = title
        self.page_num = page_num
        self.headings = []
        self.questions = []
        super(Chapter, self).__init__()

    def add_heading(self, heading_name : str):
        """add a heading to this chapter

        Args:
            heading_name (str): name of the heading to add 
        """
        self.headings.append(Heading(heading_name))
    
    def add_question(self, question_text : str):
        """add a new question to this chapter

        Args:
            question_text (str): question text
        """
        self.questions.append(Question(question_text))

class Article(Serializable):
    def __init__(self, title : str):
        """Initialize a new article

        Args:
            title (str): Title of the article
        """
        self.title = title
        self.chapters = []
        super().__init__()
    
    def add_chapter(self, chapter_name : str):
        """Add a new chapter to this article

        Args:
            chapter_name (str): Name of the chapter to add
        """
        self.chapters.append(Chapter(chapter_name))
    

#class Note(Serializable):
#    test = 1
#    pogwaa = "this is a sentence!"
#    a_collection_of_cuties = ["tom", "brady", "chelsea"]
#    def __init__ (self, flag):
#        super(Note, self).__init__()
#        if(flag):
#            self.subnote = Note(False)
#            self.subnote.extradata = "this is extra data owned by the child!"
        

#note = Note(True)
#notejson =  str(note)
#print("Note converted to json" + str(note))
#testjson = """{"a_collection_of_cuties": ["tom", "brady", "chelsea"], "pogwaa": "this is a sentence!", "test": "1"}"""
#note2 = Note.from_json(notejson)
#print("Note converted to json and back again" + str(note))

