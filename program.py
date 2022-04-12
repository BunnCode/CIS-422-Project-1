###This file contains the GUI code and the main loop of the project.
###All databse management code should be done in databse.py

#import GUI library
import tkinter as tk
#import database file
import database as db
#import datastructures file
import datastructures as ds

#Initialize the program window
window = tk.Tk()

#Create example text component
#Added text = as that is required for it to display
helloworld = tk.Label(text = "Hello, world!")

save = tk.Button(text = "Save", width=10, height=5, bg="white", fg="black")
#Initialize the component (this is not the only way to initialize but it is the simplest)
helloworld.pack()
save.pack()
#Adding the window mainloop to listen for events
window.mainloop()