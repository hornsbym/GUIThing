"""
view.py
Creates a GUI for theThing.py progam.
Author: Mitchell Hornsby
"""
from breezypythongui import EasyFrame
from theThing import *

class Window(EasyFrame):
    """Object for the view window."""
    def __init__(self):
        """Creates the window, labels and buttons."""
        EasyFrame.__init__(self, "The Thing", width = 575, height = 400, resizable = False, background = "grey")
        #self.came = Control()
        outputPanel = self.addPanel(row = 1, column = 1, background = "gray")
        inputPanel = self.addPanel(row = 2, column = 1, background = "blue")
        buttonPanel = self.addPanel(row = 2, column = 2, background = "green")
        commandField = inputPanel.addTextField(row = 1, column = 1, text = "Test", columnspan = 2)
        
w = Window()

