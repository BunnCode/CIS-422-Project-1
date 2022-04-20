from __future__ import annotations
import json
import re
###This file will define the data types that we will use for storing notes. 
# Namely, the cascading book -> chapter -> heading -> subheading -> line -> notes tree. 


class Serializable:
    """Children of this serializable object
    """
    children : Serializable

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
        
            
    """Recursively serialize to JSON
    """
    def __str__(self) -> str:
        #Get all members of this class, and then filter out default attributes and functions, leaving only variable names
        vars = [varname for varname in dir(self) if not varname.startswith("__") and not callable(getattr(self, varname))]
        #Variable names are stored in a list of tuples of key value pairs
        var_tuple_list = []
        for varname in vars:
            #attribute we are accessing
            attr = getattr(self, varname)
            #Convert to string - this is the part that triggers the recursive call
            attrjson = str(attr)

            #If the attr is a string we have to make it json compatible
            #if type(attr) is list:
             #   attrjson = attrjson[1:-1]

            #add attribute to list of tuples
            var_tuple_list.append((varname, str(attrjson)))
        
        
        for var in var_tuple_list:

        #Regex to replace all single quotes that are not in strings with double quotes; sourced from https://stackoverflow.com/questions/39491420/python-jsonexpecting-property-name-enclosed-in-double-quotes
        #p = re.compile('(?<!\\\\)\'')
        
        #convert var dict to string and run the regex on it 
        #jsonoutput = p.sub('\"', str(vardict))

        #Conveniently, dictionary string representations include curly braces so we don't need to add them for the json
        #return "{0}".format(jsonoutput)
    
    


#class SerializableList(Serializable):
#    members : Serializable


class Note(Serializable):
    test = 1
    pogwaa = "this is a sentence!"
    a_collection_of_cuties = ["tom", "brady", "chelsea"]
    #def __init__ ():
        #do nothing
        #return

note = Note()
notejson =  str(note)
print("Note converted to json" + str(note))
testjson = """{"a_collection_of_cuties": ["tom", "brady", "chelsea"], "pogwaa": "this is a sentence!", "test": "1"}"""
note2 = Note(notejson)
print("Note converted to json and back again" + str(note))

