"""
view.py
Creates a GUI for theThing.py progam.
Author: Mitchell Hornsby
"""
from tkinter import *
from theThing import *

roomObjs = createRoomObjs(roomNames)
charObjs = createCharObjs(charNames, roomObjs)
permCharList = assignCharsToRooms(charObjs, roomObjs)
game = Control(roomObjs, permCharList)
game.setupGame()

class Window(Frame):
    """Object for the view window."""
    def __init__(self, master=None):
        """Creates the window, labels and buttons."""
        Frame.__init__(self, background = "grey")
        self.master.title("The Thing")
        self.master.bind("<Return>", self.submit)
        self.grid()
        
        self._game = game

        self.bind("<Return>", self.submit)

        self._outputLabel = Label(self, text=roomDict["Blair's Room"], relief="raised", anchor=NW, height=20, width=50, bg='white', wraplength=400, justify=LEFT)
        self._outputLabel.grid(row=0, column=1, rowspan= 3, columnspan=1, pady=10, padx = 5)

        self._inputLabel = Label(self, text = "Command: ", fg="white", bg="gray")
        self._inputLabel.grid(row=3, column=0)

        self._inputVar = StringVar()
        self._inputField = Entry(self, text="Press Submit to start.", width=50, textvariable=self._inputVar)
        self._inputField.grid(row=3, column=1, pady=5)

        self._submitButton = Button(self, text="Submit", command=self.submit)
        self._submitButton.grid(row=3, column=2, padx=3, sticky=W)

        self._turnLabel = Label(self, text="Turn "+str(game.getTurnCount())+"\n"+game.showPlayer()+"\n"+ str(game.getInfectedCount())+" infected", justify=CENTER, bg="gray", fg="white")
        self._turnLabel.grid(row=0, column=0, padx = 10)

        self._occupantLabel = Label(self, text="Occupants: \n"+str(game.occupants()), justify=LEFT, bg="gray", fg="white")
        self._occupantLabel.grid(row=1, column=0)

        self._mapButton = Button(self, text="Map", command=self.showMap)
        self._mapButton.grid(row=2, column=0)
        
        self._inventoryLabel = Label(self, text="Inventory: \n"+str(game.inventory()), justify=LEFT, bg="gray", fg="white")
        self._inventoryLabel.grid(row=2, column=2, sticky=NW, pady = 10, padx = 5)

        self._infectedLabel = Label(self, text="Tested positive: \n"+str(game.strInfected()), justify=LEFT, bg="gray", fg="white")
        self._infectedLabel.grid(row=0, column=2, sticky=NW, pady = 10, padx = 5)

        self._uninfectedLabel = Label(self, text="Tested negative: \n"+str(game.strUninfected()), justify=LEFT, bg="gray", fg="white")
        self._uninfectedLabel.grid(row=1, column=2, sticky=NW, pady = 10, padx = 5)
        
        
    def submit(self, event=None):
        """Takes text from the entry bar, sends it to the control, then displays it on the output label."""
        if self.checkGame() == False:
            self._outputLabel["text"] = game.getStats()
        else:
            command = self._inputField.get()
            if command == "" or command ==" ":
                return
            self._outputLabel["text"] = turn(self._game, command)
            self.updateTurn()
            self.updateChar()
            self.updateInv()
            self.updateInf()
            self.updateUninf()
            self._inputField.delete(0, END)
            return
    def updateTurn(self):
        """Updates the turn-count label."""
        self._turnLabel['text'] = "Turn " + str(game.getTurnCount())+"\n"+game.showPlayer()+"\n"+ str(game.getInfectedCount())+" infected"
        return
    def updateChar(self):
        """Updates the occupant label:"""
        self._occupantLabel['text'] = "Occupants: \n" + game.occupants()
        return
    def updateInv(self):
        self._inventoryLabel['text'] = "Inventory: \n"+ game.inventory()
        return
    def updateInf(self):
        self._infectedLabel['text'] = "Tested positive: \n" + game.strInfected()
        return
    def updateUninf(self):
        self._uninfectedLabel['text'] = "Tested negative: \n" + game.strUninfected()
        return
    def showMap(self):
        toplevel = Toplevel()
        mLabel = Label(toplevel, text=game.showMap(), font="Courier", background="White")
        mLabel.pack()
        return
    def checkGame(self):
        return game.continueGame()
    
def main():
    W = Window()
    W.mainloop()

if __name__ =="__main__":
    main()
    

