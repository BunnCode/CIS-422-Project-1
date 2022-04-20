from __future__ import annotations
import json
import re
from typing import Dict
###This file will define the data types that we will use for storing notes. 
# Namely, the cascading book -> chapter -> heading -> subheading -> line -> notes tree. 


class Serializable:
    #prefix given to serializable class names
    __PREFIX = "[s]"

    """Initialize serializable object. If provided, will load values from json.
    """
    def __init__(self, jsonstr = ""):
        if len(jsonstr) == 0:
            return
        #load attribute dictionary
        attrs = json.loads(jsonstr)
        #Iterate over attribute names
        for attributename in iter(attrs):
            setattr(self, attributename, attrs[attributename])
        return
        
    """convert this serializable object to a dictionary
    """
    def to_dict(self) -> Dict:
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
    
    """Converts from a dictionary to a serializable object
    """
    def from_dict(self) -> Serializable:

    """Return JSON
    """
    def __str__(self) -> str:
        outputdict = self.to_dict()
        return json.dumps(outputdict)
    
    


#class SerializableList(Serializable):
#    members : Serializable


class Note(Serializable):
    test = 1
    pogwaa = "this is a sentence!"
    a_collection_of_cuties = ["tom", "brady", "chelsea"]
    def __init__ (self, flag):
        super(Note, self).__init__()
        if(flag):
            self.subnote = Note(False)
            self.subnote.extradata = "this is extra data owned by the child!"
        

note = Note(True)
notejson =  str(note)
print("Note converted to json" + str(note))
testjson = """{"a_collection_of_cuties": ["tom", "brady", "chelsea"], "pogwaa": "this is a sentence!", "test": "1"}"""
note2 = Note(notejson)
print("Note converted to json and back again" + str(note))

