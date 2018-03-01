"""
Mitchell Hornsby
theThing.py
Text-based game. You play as MacReady, an antarctic researcher locked in with
several others. Two of them have been taken over by a parasite known only as "The
Thing", which looks and acts exactly like its host. Your goal is to either
identify and kill every infected researcher and escape, or destroy the base along
with yourself. The camp's scientist, Blair, has been locked away from the others,
and will help you identify who might be infected. But be warned... Not everything
is as it seems!
"""
import random

charNames = ['Fuches','Windows','Copper','Childs',"Barclay","Bennings","Clarke","Norris","Van Wall","Connant"]
roomNames = ['Kitchen', 'Experiment Room', 'Hangar', 'Dining Room', "Blair's Room", "Foyer", "Dog Room","Thawing Room"]

class person(object):
    """Parent class for every person, including the player ."""
    def __init__(self, personName, infectedStatus):
        self._name = personName
        self._infectedStatus = infectedStatus
        self._currentRoom = None
    def __str__(self):
        """Returns string representation of the people."""
        return "Name: " + self._name + '\n' + 'Infected Status: ' + \
               str(self._infectedStatus) + "\n" + 'Current room: ' + \
               self._currentRoom.getName()
    def getName(self):
        """Returns a string representation of the character's name."""
        return str(self._name)
    def setCurrentRoom(self, room):
        """Sets the character's current room"""
        self._currentRoom = room
    def getCurrentRoom(self, room):
        """Returns the room object the character is currently in."""
        return self._currentRoom
    def getRoomName(self):
        return self._currentRoom.getName()
    
    def getInfectedStatus(self):
        """Returns True if person is infected, False if not."""
        return self._infectedStatus 
                
class room(object):
    """Represents the basic outline of a room."""
    def __init__(self, roomName):
        self._name = roomName
        self._occupants = []
    def __str__(self):
        """Returns string representation of the room objects"""
        return "Room: " + self._name + '\n' + "Occupants: " + str(self.occupantNames())
    def getName(self):
        """Adds a character to the room."""
        return str(self._name)
    def occupantNames(self):
        """Returns a list of names of all the characters in the room."""
        occupantNames = []
        for x in range(len(self._occupants)):
            occupantNames.append(self._occupants[x].getName())
        return str(occupantNames)
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
        
class MacReady(person):
    """Player controlled person instance."""
    def __init__(self):
        self._name = "MacReady"
        self._infectedStatus = False
        self._visitedRooms = []
    def addVisited(self):
        self._visitedRooms.append(self.getCurrentRoom())

class Blair(person):
    """Special character instance; provides guidance for the playable character."""
    def __init__(self):
        self._name = "Blair"
        self._infectedStatus = False

def assignCharsToRooms(characterList, roomList):
    """Assigns every character to a room."""
    newCharList = []
    for x in range (len(characterList)):
        char = random.choice(characterList)
        room = random.choice(roomList)
        char.setCurrentRoom(room)
        room.acceptChar(char)
        newCharList.append(char)
        characterList.remove(char)
    return newCharList

def createCharObjs(listOfCharacterNames, roomList):
    """Creates a list of character objects when given a list of names."""
    charObjects = []
    #Creates characters from information in charNames list
    for x in range(len(listOfCharacterNames)):
        char = person(listOfCharacterNames[x], False)
        charObjects.append(char)
    player = MacReady()
    blair = Blair()
    charObjects.append(player)
    charObjects.append(blair)
    return charObjects
    
def createRoomObjs(listOfRoomNames):
    """Creates a list of room objects when gien a list of room names."""
    roomObjects = []
    #Creates characters from information in charNames list
    for x in range(len(listOfRoomNames)):
        r = room(listOfRoomNames[x])
        roomObjects.append(r)
    return roomObjects

def changeRoom(characterName, targetRoomName, listOfRooms):
    """Moves a character from one room to another."""
    prevRoomObj = findCharacterRoom(characterName, listOfRooms)
    charObj = findCharObj(characterName, prevRoomObj)
    targetRoomObj = findRoomObj(targetRoomName, listOfRooms)
    prevRoomObj.removeOccupant(charObj)
    charObj.setCurrentRoom(targetRoomObj)
    targetRoomObj.acceptChar(charObj)

def findCharObj(characterName, characterRoom):
    """Finds the object bearing the character name in the \
    list of rooms; returns a character object."""
    return characterRoom.getChar(characterName)

def findCharacterRoom(characterName, roomList):
    """Takes the name of a character, then returns the room \
    with that character in it; returns a room object."""
    for x in range(len(roomList)):
        if characterName in roomList[x].occupantNames():
            return roomList[x]
    print("Character not in any room.")

def findRoomObj(roomName, roomList):
    """Takes the name of a room, then \
    returns the room object of that name."""
    for room in range(len(roomList)):
        if roomList[room].getName() == roomName:
            return roomList[room]
        
def displayRoomStatus(roomList):
    """Takes a list of rooms and prints each room's status."""
    #Prints room objects
    for x in range(len(roomList)):
        print(roomList[x])
        print()

def displayCharStatus(characterList):
    """Takes a list of characters and prints each of their status."""
    #Prints character objects
    for x in range(len(characterList)):
        print(characterList[x])
        print()

def changePlayerRoom(listOfRooms):
    """Change's MacReady's (player's) room."""
    #Gets input and corrects it for spelling errors
    targetRoom= str(input("Where would you like to move to? "))
    '''if targetRoom.upper() == "DINING ROOM":
        targetRoom = "Dining Room"
    if targetRoom.upper() == "BLAIR'S ROOM":
        targetRoom = "Blair's Room"
    if targetRoom.upper() == "EXPERIMENT ROOM":
        targetRoom = "Experiment Room"
    if targetRoom.upper() == "KITCHEN":
        targetRoom = "Kitchen"
    if targetRoom.upper() == "DOG ROOM":
        targetRoom = "Dog Room"
    if targetRoom.upper() == "HANGAR":
        targetRoom = "Hangar"
    if targetRoom.upper() == "FOYER":
        targetRoom = "Foyer"
    if targetRoom.upper() == "THAWING ROOM":
        targetRoom = "Thawing Room"
    else:
        print("I couldn't understand that...")
        return False'''
    changeRoom("MacReady", targetRoom, listOfRooms)
    return True

def setup(listOfRooms):
    """Puts Blair and Macready (player) into their start room"""
    changeRoom("MacReady", "Blair's Room", listOfRooms)
    changeRoom("Blair", "Blair's Room", listOfRooms)
    print("The Thing")
    print("Created by Mitchell Hornsby")
    print()
    print('You play as MacReady, an antarctic researcher locked in an underground\
 research base with \
several others. Two of them have been taken over by a parasite known only\
as "The Thing", which looks and acts exactly like its host. Your goal is \
to either identify and kill every infected researcher and escape, or destroy\
 the base along with yourself. The camp scientist, Blair, has been locked away\
from the others, and will help you identify who might be infected. But be \
warned... Not everything is as it seems!')
    print()
    start = input("Press enter to start!")
    print("---------------------")
    if start == "":
        return
    else:
        return

def checkMove(currentRoom, nextRoom):
    """Takes a room object, then checks to see what other rooms are accessible from that room"""
    if currentRoom.getName() == "Blair's Room":
        if nextRoom.getName() == "Experiment Room" or nextRoom.getName() == "Dining Room":
            return True
        else:
            return False
    if currentRoom.getName() == "Experiment Room":
        if nextRoom.getName() == "Blair's Room":
            return True
        else:
            return False
    if currentRoom.getName() == "Dining Room":
        if nextRoom.getName() == "Blair's Room" or nextRoom.getName() == "Kitchen" or nextRoom.getName() == "Hangar" or nextRoom.getName() == "Thawing Room":
            return True
        else:
            return False
    return True
    if currentRoom.getName() == "Hangar":
        if nextRoom.getName() == "Dining Room" or nextRoom.getName() == "Dog Room":
            return True
        else:
            return False
    if currentRoom.getName() == "Dog Room":
        if nextRoom.getName() == "Hangar":
            return True
        else:
            return False
    if currentRoom.getName() == "Thawing Room":
        if nextRoom.getName() == "Hangar" or nextRoom.getName() == "Foyer" or nextRoom.getName() == "Kitchen":
            return True
        else:
            return False
    if currentRoom.getName() == "Kitchen":
        if nextRoom.getName() == "Dining Room" or nextRoom.getName() == "Thawing Room":
            return True
        else:
            return False
    if currentRoom.getName() == "Foyer":
        if nextRoom.getName() == "Thawing Room":
            return True
        else:
            return False  
        
def turn(listOfRooms, listOfChars):
    """Controls the events that happen each turn."""
    rooms = listOfRooms
    chars = listOfChars
    stateLocation('MacReady', rooms)
    print()
    userInput = str(input("What would you like to do? "))
    command = userInput.upper()
    if command == 'MOVE':
        return changePlayerRoom(rooms)
    if command == "WAIT":
        print("MacReady waited around a while.")
        return True
    if command == 'STATUS':
        print()
        displayRoomStatus(rooms)
        return False
    if command == 'HELP':
        print("Commands are move, wait, status, and help.")
        return False
    if command != "MOVE" or "STATUS" or "HELP":
        print("Commands are move, wait, status and help. Try again.")
        return False
            

def stateLocation(playerName, listOfRooms):
    """Gives the player's location"""
    player = findCharObj(playerName, findCharacterRoom(playerName, listOfRooms))
    if findCharacterRoom(playerName, listOfRooms).getName() == "Blair's Room":        
        print("You are in " + player.getRoomName() + ".")
    else:
        print("You are in the " + player.getRoomName() + ".")
    
def main():
    #Creates a list of character and room objects
    roomObjs = createRoomObjs(roomNames)
    charObjs = createCharObjs(charNames, roomObjs)

    #Puts the characters in their rooms.
    permCharList = assignCharsToRooms(charObjs, roomObjs)

    setup(roomObjs)

    turnCount = 0
    while True:
        print()
        print("Turn "+str(turnCount))
        print()
        turn(roomObjs, permCharList)
    
if __name__ == '__main__':
    main()
