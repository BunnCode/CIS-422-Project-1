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
|   |->Note
|   |->Note
|   |...
|->Question  
|->Question
|... 

"""
class Note(Serializable):
    def __init__(self, page_num : int, note_text : str):
        """A note on a specific heading

        Args:
            note_text (str): The note 
            page (int): The page of the note
        """
        self.note_text = note_text
        self.page_num = page_num
        super(Note, self).__init__()
        
class Question(Serializable):
     def __init__(self, question_text : str):
        """A question about a certain chapter

        Args:
            note_text (str): The question to be answered
        """
        #Text in this note
        self.question_text = question_text
        super(Question, self).__init__()

class QuizAttempt(Serializable):
    def __init__(self, score :int, max_score : int):
        """Logs a quiz attempt

        Args:
            score (int): Score for this attempt
            max_score (int): Max score for this attempt
        """
        self.score = score
        self.max_score = max_score
        super(QuizAttempt, self).__init__()

class Chapter(Serializable):
    def __init__(self, page_num : int, title : str):
        """Initialize a new chapter in a specific article.

        Args:
            page_num (int): page number this chapter appears in
            title (str): title of this chapter
        """
        self.title = title
        self.page_num = page_num
        self.notes = []
        self.questions = []
        super(Chapter, self).__init__()
    
    def add_question(self, question_text : str) -> Question:
        """add a new question to this chapter

        Args:
            question_text (str): question text
        """
        new_question = Question(question_text)
        self.questions.append(new_question)
        return new_question

    def add_note(self, page_num : int, note_text : str) -> Note:
        """Add a new note to this chapter

        Args:
            page_num (int): page number that this note refers to
            note_text (str): Note to record

        Returns:
            Note: The new note
        """
        new_note = Note(page_num, note_text)
        self.notes.append(new_note)
        return new_note

class Article(Serializable):
    def __init__(self, article_name : str, article_id = -1):
        """Initialize a new article

        Args:
            article_name (str): Title of the article
        """
        self.article_name = article_name
        self.chapters = []
        self.article_id = article_id
        self.quiz_attempts = []
        super().__init__()
    
    def add_chapter(self, chapter_name : str, page_num : int) -> Chapter:
        """Add a new chapter to this article

        Args:
            chapter_name (str): Name of the chapter to add
        """
        new_chapter = Chapter(page_num, chapter_name)
        self.chapters.append(new_chapter)
        return new_chapter
    
    def add_quiz_attempt(self, score : int, max_score : int) -> QuizAttempt:
        """Add a new quiz attempt to this article

        Args:
            score (int): Score for this attempt
            max_score (int): Max possible score for this attempt
        """
        new_attempt = QuizAttempt(score, max_score)
        self.quiz_attempts.append(new_attempt)
        return new_attempt

