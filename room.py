"""
room.py
File contains the room class to be used by the program theThing.py
Author: Mitchell Hornsby
"""
import random

class Room(object):
    """Represents the basic outline of a room."""
    def __init__(self, roomName):
        self._name = roomName
        self._occupants = []
    def __str__(self):
        """Returns string representation of the room objects."""
        return self._name + '\n' + str(self.occupantNames())
    def getName(self):
        """Returns the name of the room."""
        return str(self._name)
    def occupantNames(self):
        """Returns a list of names of all the characters in the room."""
        occupantNames = []
        for x in range(len(self._occupants)):
            occupantNames.append(self._occupants[x].getName())
        return occupantNames
    def acceptChar(self, char):
        """Adds a character to the room."""
        self._occupants.append(char)
    def removeOccupant(self, char):
        """Removes a character from the room."""
        if char in self._occupants:
            self._occupants.remove(char)
        return
    def getChar(self, characterName):
        """Returns a specified character within the room."""
        char = characterName
        for x in range(len(self._occupants)):
            if char == self._occupants[x].getName():
                return self._occupants[x]
        else:
            return char + " is not in the room."
    def thingsAttack(self):
        """Checks for infected characters in the room. Each infected character has a 10% chance to attack."""
        if len(self._occupants) == 0:
            return
        numOne = random.randint(1,2)
        if numOne == 1:
            personOne = random.choice(self._occupants)
            personTwo = random.choice(self._occupants)
            if personOne is personTwo:
                return
            elif personOne.getInfectedStatus() == personTwo.getInfectedStatus():
                return
            elif personOne.getInfectedStatus() == True and personOne.isAlive() == True:
                return personTwo.setInfectedStatus()
            elif personTwo.getInfectedStatus() == True and personTwo.isAlive() == True:
                return personOne.setInfectedStatus()
        else:
            return
        
