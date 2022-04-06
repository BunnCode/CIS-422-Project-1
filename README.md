# CIS 422 Project 1; Notetaking app for [INSERT READING METHOD HERE]

## How to set up the environment
This project uses Python3 and tkinter for GUI. To get everything set up properly, run the following commands.
```
#Install the virtual environment
python3 -m pip install --user virtualenv

#Please name your virtual environment 'env' so that git properly ignores it
python3 -m venv venv

#Execute the virtual environment. On windows, use ".\env\Scripts\activate"
source env/bin/activate

#Once in the virtual environment, run the following commands.
pip3 install tk
pip3 install pymongo

#To exit the virtual environment when you are done working on the project, run this command
deactivate
```

## Project organization

The source is divided into three files:

### program.py
Contains the main program loop and GUI code.

### database.py
Contains all code pertaining to database connection.

### datastructures.py
Contains data structures used by the two above files.