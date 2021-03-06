"""
person.py
File containing all person classes for theThing.py program.
Author: Mitchell Hornsby
"""
import random

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
        """Turns a person's infected status to true; 'Infects' them."""
        self._infectedStatus = True
    def setUninfected(self):
        """Makes a char's infected status false; onlu used when an infected char is killed."""
        self._infectedStatus = False
    def getInfectedStatus(self):
        """Returns True if person is infected, False if not."""
        return self._infectedStatus
    def isAlive(self):
        """Checks if a person is still alive."""
        return self._alive
    def kill(self):
        """Turns a person's self._alive status to false."""
        self._alive = False
    def attack(self, human):
        """Changes a human's status to false (kills them)."""
        human.kill()
        
class MacReady(Person):
    """Player controlled person instance."""
    def __init__(self):
        self._name = "MacReady"
        self._infectedStatus = False
        self._visitedRooms = []
        self._inventory = []
        self._alive = True
    def addVisited(self):
        """Adds the current room to the visited rooms list, if it has not been visited already."""
        if len(self._visitedRooms) == 9:
            return
        if self.getRoomName() not in self._visitedRooms:
            self._visitedRooms.append(self.getRoomName())
    def getVisited(self):
        """Returns list of visted rooms."""
        return self._visitedRooms
    def addInventory(self, item):
        """Adds an item to MacReady's inventory; returns True if the item is added."""
        if len(self._inventory) < 5:
            self._inventory.append(item)
            return True
        if len(self._inventory) >= 5:
            return False
    def popInventory(self, item):
        """Removes & returns an item from MacReady's inventory."""
        for i in range(len(self.getInventory())):
            if self.getInventory()[i] == item:
                return self._inventory.pop(i)
    def getInventory(self):
        """Returns items in MacReady's inventory."""
        return self._inventory
    def removeInventory(self, i):
        """Removes an item from MacReady's inventory at the ith position."""
        if type(i) != int:
            return False
        else:
            del self._inventory[i]
        
class Blair(Person):
    """Special character instance; provides guidance for the playable character."""
    def __init__(self):
        self._name = "Blair"
        self._infectedStatus = False
        self._alive = True
