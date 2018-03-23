"""
view.py
Creates a GUI for theThing.py progam.
Author: Mitchell Hornsby
"""
from tkinter import *
from theThing import *

class Window(Frame):
    """Object for the view window."""
    def __init__(self):
        """Creates the window, labels and buttons."""
        Frame.__init__(self, background = "grey")
        self.master.title("The Thing")
        self.grid()
        
        #self._game = Control()

        self._outputLabel = Label(self, text="Output", relief="raised", anchor=W, height=8, width=50, bg='white')
        self._outputLabel.grid(row=0, column=1, rowspan= 3, columnspan=2, pady=10, padx = 5)

        self._inputLabel = Label(self, text = "Command: ", fg="white", bg="gray")
        self._inputLabel.grid(row=3, column=0)

        self._inputVar = StringVar()
        self._inputField = Entry(self, width=50, textvariable=self._inputVar)
        self._inputField.grid(row=3, column=1, pady=5)

        self._submitButton = Button(self, text="Submit", command=self.submit())
        self._submitButton.grid(row=3, column=2, padx=3)

        self._turnLabel = Label(self, text="Turn #", bg="gray", fg="white")
        self._turnLabel.grid(row=0, column=0)

        self._occupantLabel = Label(self, text="Occupants: ", bg="gray", fg="white")
        self._occupantLabel.grid(row=1, column=0)

        self._mapButton = Button(self, text="Map")
        self._mapButton.grid(row=2, column=0)

    def submit(self):
        """Takes text from the entry bar, sends it to the control, then displays it on the output label."""
        command = self._inputVar.get()
        self._outputLabel["text"] = command 
        
w = Window()

