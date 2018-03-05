"""
person.py
File containing all person classes for theThing.py program.
Author: Mitchell Hornsby
"""
class Person(object):
    """Parent class for every person, including the player ."""
    def __init__(self, personName, infectedStatus):
        self._name = personName
        self._infectedStatus = infectedStatus
        self._alive = True
        self._currentRoom = None
    def __str__(self):
        """Returns string representation of the people."""
        return "Name: " + self._name + '\n' + 'Infected Status: ' + \
               str(self._infectedStatus) + "\n" + 'Current room: ' + \
               self._currentRoom.getName() + "\n" +"Alive? " + str(self._alive)
    def getName(self):
        """Returns a string representation of the character's name."""
        return str(self._name)
    def setCurrentRoom(self, room):
        """Sets the character's current room"""
        self._currentRoom = room
    def getCurrentRoom(self):
        """Returns the room object the character is currently in."""
        return self._currentRoom
    def getRoomName(self):
        """Returns only the name of the character's room."""
        return self._currentRoom.getName()
    def setInfectedStatus(self):
        """Turns a person't infected status to true; 'Infects' them."""
        self._infectedStatus = True
    def getInfectedStatus(self):
        """Returns True if person is infected, False if not."""
        return self._infectedStatus
    def isAlive(self):
        """Checks if a person is still alive."""
        return self._alive
    def kill(self):
        "Turns a person's self._alive status to false."
        self._alive = False
        
class MacReady(Person):
    """Player controlled person instance."""
    def __init__(self):
        self._name = "MacReady"
        self._infectedStatus = False
        self._visitedRooms = []
        self._alive = True
    def addVisited(self):
        """Adds the current room to the visited rooms list, if it has not been visited already."""
        if self.getRoomName() not in self._visitedRooms:
            self._visitedRooms.append(self.getRoomName())
    def getVisited(self):
        """Returns list of visted rooms."""
        return self._visitedRooms

class Blair(Person):
    """Special character instance; provides guidance for the playable character."""
    def __init__(self):
        self._name = "Blair"
        self._infectedStatus = False
        self._alive = True
