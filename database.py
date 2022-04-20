###This file contains all databse code for the program.
###All GUI Code should be executed in program.py
import datastructures as ds

###These are stubs. Please feel free to modify them. I just wrote some stuff out to give a scaffold for us to work from since time is so short. 
"""Connect to the MongoDB instance given "url"
"""
def init_db_connection(url: str):
    #Initialize the connection to the database. Remember that this cannot require a password as per project instructions.
    #todo: This is a stub and IS NOT complete.
    client = MongoClient(url)
    return client 

"""load and return all information from database "client" for a given user defined by "user" on chapter "chapter"
"""
def load_chapter_notes_from_db(client: MongoClient, chapter:int, user: str):
    #Should this be recursive somehow? Each individual heading and subheading can also have notes.
    #This will ultimately return a value from "datastructures.py"
    return None

"""save all information from database "client" for a given user defined by "user" on chapter "chapter"
"""
#def save_chapter_notes_to_db(client: MongoClient, chapter:int, user: str):
#This function will take in the data structure defined in "datastructures.py"