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
roomNames = ['Kitchen', 'Experiment Room', 'Hangar', 'Dining Room', "Blair's Room", "Foyer", "Dog Room","Thawing Room","Security Room"]

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
        return self._currentRoom.getName()
    def setInfectedStatus(self):
        self._infectedStatus = True
    def getInfectedStatus(self):
        """Returns True if person is infected, False if not."""
        return self._infectedStatus
    def isAlive(self):
        return self._alive
    def kill(self):
        self._alive = False
        
class MacReady(Person):
    """Player controlled person instance."""
    def __init__(self):
        self._name = "MacReady"
        self._infectedStatus = False
        self._visitedRooms = []
        self._alive = True
    def addVisited(self):
        self._visitedRooms.append(self.getCurrentRoom())

class Blair(Person):
    """Special character instance; provides guidance for the playable character."""
    def __init__(self):
        self._name = "Blair"
        self._infectedStatus = False
        self._alive = True

class Room(object):
    """Represents the basic outline of a room."""
    def __init__(self, roomName):
        self._name = roomName
        self._occupants = []
    def __str__(self):
        """Returns string representation of the room objects"""
        return self._name + '\n' + str(self.occupantNames())
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

class Control(object):
    """Instance that controls the game mechanics."""
    def __init__(self, roomList, charList):
        self._roomList = roomList
        self._charList = charList
        self._turnCount = 1
    def incTurnCount(self):
        """Increments the turn count by one."""
        self._turnCount += 1
    def getTurnCount(self):
        """Returns the current turn count."""
        return self._turnCount
    def setupGame(self):
        """Puts player and Blair in Blair's Room."""
        self.changeRoom("MacReady", "Blair's Room")
        self.changeRoom("Blair", "Blair's Room")   
    def showRooms(self):
        """Displays each room in the game along with its occupants"""
        for x in range(len(self._roomList)):
            print(self._roomList[x])
            print()
    def findCharObj(self, characterName):
        """Finds the object bearing the character name in the
           list of characters; returns a character object."""
        for char in range(len(self._charList)):
            if self._charList[char].getName() == characterName:
                return self._charList[char]
    def findRoomObj(self, roomName):
        """Finds the object bearing the room name in the
           list of rooms; returns a room object."""
        for room in range(len(self._roomList)):
            if self._roomList[room].getName() == roomName:
                return self._roomList[room]
    def changeRoom(self, characterName, targetRoomName):
        """Moves a character from one room to another."""
        roomObj = self.findCharObj(characterName).getCurrentRoom()
        charObj = self.findCharObj(characterName)
        targetRoomObj = self.findRoomObj(targetRoomName)
        roomObj.removeOccupant(charObj)
        charObj.setCurrentRoom(targetRoomObj)
        targetRoomObj.acceptChar(charObj)
    def changePlayerRoom(self):
        """Moves the player object to a user-specified room"""
        destination = str(input("Name a room to move to: "))
        if self.checkMove(destination) == False:
            print("You can't move there!")
        else: 
            self.changeRoom("MacReady", destination)
    def infect(self, characterName):
        """Infects a specified character."""
        self.findCharObj(characterName).setInfectedStatus()
    def showPlayer(self):
        """Finds and prints the current location of the player."""
        location = self.findCharObj("MacReady").getRoomName()
        if location != "Blair's Room":
            print("You are in the " + location + ".")
        else:
            print("You are in " + location + ".")
    def checkPlayer(self):
        player = self.findCharObj("MacReady")
        return player.isAlive()
    def checkMove(self, roomName):
        blair = ["Experiment Room","Dining Room"]
        experiment = ["Blair's Room","Dining Room"]
        dining = ["Blair's Room","Experiment Room", "Hangar", "Kitchen", "Thawing Room"]
        hangar = ["Dining Room", "Dog Room", "Thawing Room"]
        dog = ["Hangar", "Security Room"]
        thawing = ["Dining Room","Hangar", "Kitchen", "Foyer"]
        foyer = ["Thawing Room"]
        security = ["Dog Room"]
        kitchen = ["Dining Room", "Thawing Room"]
        if roomName == "Blair's Room":
            if roomName not in blair:
                return False
        return True
        

        
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
        char = Person(listOfCharacterNames[x], False)
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
        r = Room(listOfRoomNames[x])
        roomObjects.append(r)
    return roomObjects

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
        
def turn(g):
    """Controls the events that happen each turn."""
    userInput = str(input("What would you like to do? "))
    command = userInput.upper()
    if command == 'MOVE':
        g.changePlayerRoom()
        g.incTurnCount()
        print()
        print(g.findCharObj("MacReady"))
        return
    if command == "WAIT":
        g.incTurnCount()
        print("MacReady waited around a while.")
        return
    if command == 'STATUS':
        print()
        g.showRooms()
        return 
    if command == 'HELP':
        print("Commands are move, wait, status, help, and quit.")
        return
    if command == "QUIT":
        g.findCharObj("MacReady").kill()
        return
    if command != "MOVE" or "STATUS" or "HELP" or "QUIT":
        print("Commands are move, wait, status, help, and quit. Try again.")
        return
    
def main():
    roomObjs = createRoomObjs(roomNames)
    charObjs = createCharObjs(charNames, roomObjs)
    permCharList = assignCharsToRooms(charObjs, roomObjs)

    g = Control(roomObjs, permCharList)
    print("---------(Setting up game)---------")
    g.setupGame()
    g.showRooms()
    print("---------(Finding a character)---------")
    print(g.findCharObj("Blair"))
    print("---------(Finding a room)----------")
    print(g.findRoomObj("Blair's Room"))
    print("---------(Changing a character's room)---------")
    g.changeRoom("Blair", "Blair's Room")
    print(g.findCharObj("Blair"))
    print()
    print(g.findRoomObj("Blair's Room"))
    print("---------(Changing the player's room)--------")
    print(g.findCharObj("MacReady"))
    print()
    #g.changePlayerRoom()
    print("<Move player>")
    print()
    print(g.findCharObj("MacReady"))
    print("----------(Infects a character)---------")
    print(g.findCharObj('Childs'))
    print()
    g.infect("Childs")
    print(g.findCharObj('Childs'))
    print("----------(Find the player)----------")
    g.showPlayer()
    print("----------(Test game)----------")
    print("The Thing")
    while g.checkPlayer() == True:
        print()
        print("Turn " + str(g.getTurnCount()))
        turn(g)

if __name__ == '__main__':
    main()
