from __future__ import annotations
import json
import re
from typing import Dict


class Serializable:
    #prefix given to serializable class names
    __PREFIX = ""
    #ID given to objects that have not synced with the database yet
    __ERR_ID = -9
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
            if(varname.startswith(Serializable.__PREFIX) and issubclass(type(value), Dict)):
                #if we find it, unpack the serialized object (executes recursively)
                value = Serializable(value)
                #remove the prefix before setting the attr
                varname = varname.replace(Serializable.__PREFIX, "")

            #Set attribute 
            attr = setattr(self, varname, value)

    @staticmethod
    def from_json(jsonstr = ""):
        """Initialize serializable object(s) from json

        Args:
            jsonstr (str, optional): JSON to parse. Defaults to "".

        Returns:
            Serializable: The deserialized object
        """

        #load attribute dictionary
        attrs = json.loads(jsonstr)
        #Detect serialized objects by checking for the prefix
        if(issubclass(type(attrs), Dict)):
            #If the parent object is a serializable object, return it
            return Serializable(attrs)
        else:
            #if not, it's a collection or some other data type; return the data
            return attrs

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

class Page(Serializable):
    def __init__(self, page_num : str):
        """A page beneath a certain heading. 

        Args:
            page_num (str): page number
        """
        self.notes = []
        super(Page, self).__init__()
    
    def add_note(self, note : str) -> Note:
        """add a new note to the page

        Args:
            note (str): text to add
        """
        new_note = Note(note)
        self.notes.append(note)
        return new_note

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
        #pages stored beneath this heading
        self.pages = []
        super(Heading, self).__init__()
    
    def add_subheading(self, name : str) -> Heading:
        """Add a subheading to this heading

        Args:
            name (str): Subheading name
        """
        new_heading = Heading(name)
        self.subheadings.append(new_heading)
        return new_heading

    def add_page(self, page_num : int) -> Page:
        """Add a new page to this heading

        Args:
            page_num (int): page number

        Returns:
            Page: new page
        """
        new_page = Page(page_num)
        self.pages.append(new_page)
        return new_page
    
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

    def add_heading(self, heading_name : str) -> Heading:
        """add a heading to this chapter

        Args:
            heading_name (str): name of the heading to add 
        """
        new_heading = Heading(heading_name)
        self.headings.append(new_heading)
        return new_heading
    
    def add_question(self, question_text : str) -> Question:
        """add a new question to this chapter

        Args:
            question_text (str): question text
        """
        new_question = Question(question_text)
        self.questions.append(new_question)
        return new_question

class Article(Serializable):
    def __init__(self, article_name : str, article_id = -1):
        """Initialize a new article

        Args:
            article_name (str): Title of the article
        """
        self.article_name = article_name
        self.chapters = []
        self.article_id = article_id
        super().__init__()
    
    def add_chapter(self, chapter_name : str, page_num : int) -> Chapter:
        """Add a new chapter to this article

        Args:
            chapter_name (str): Name of the chapter to add
        """
        new_chapter = Chapter(page_num, chapter_name)
        self.chapters.append(new_chapter)
        return new_chapter

"""
Testing for structures below
"""
"""
test_article = Article("This is an article about guitars")
body = test_article.add_chapter("Body", 1)
neck = test_article.add_chapter("Neck", 4)
fretboard = test_article.add_chapter("Fretboard", 6)

materials = body.add_heading("Materials")
materials.add_subheading("Types of wood").add_page(1).add_note("This article says that Oak is common for guitar necks")
materials.add_subheading("Types of construction")

body.add_question("What are guiar necks made of?")

test_json = str(test_article)
print("Article converted to json:\n" + test_json)
article2 = Article.from_json(test_json)
print("Article converted to json and back again (and again):\n" + str(article2))

"""