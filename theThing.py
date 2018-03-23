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
from person import Person, MacReady, Blair
from room import Room

charNames = ['Fuches','Windows','Copper','Childs',"Barclay","Bennings","Clarke","Norris","Van Wall","Connant"]
roomNames = ['Kitchen', 'Experiment Room', 'Hangar', 'Dining Room', "Blair's Room", "Foyer", "Dog Room","Thawing Room","Security Room"]

class Control(object):
    """Instance that controls the game mechanics."""
    def __init__(self, roomList, charList):
        self._roomList = roomList
        self._charList = charList
        self._turnCount = 1
        self._roomDescriptions = ["<Insert room description>"]
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
    def changePlayerRoom(self, roomName):
        """Moves the player object to a user-specified room"""
        userInput = cleanInput(roomName)
        if self.checkMove(self.findCharObj("MacReady").getRoomName(), userInput) == False:
            print("You can't move there!")
            return False
        else:
            if self.findCharObj("MacReady").getRoomName() not in self.findCharObj("MacReady").getVisited():
                print(str(self._roomDescriptions[0]))
            if userInput != "Blair's Room":
                self.changeRoom("MacReady", userInput)
                self.findCharObj("MacReady").addVisited()
                print("Moved to the " + userInput + ".")
                print(self.findCharObj("MacReady").getVisited())
            else:
                self.changeRoom("MacReady", userInput)
                self.findCharObj("MacReady").addVisited()
                print("Moved to " + userInput + ".")
                print(self.findCharObj("MacReady").getVisited())
            return True
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
        """Checks to see if MacReady is still alive."""
        player = self.findCharObj("MacReady")
        return player.isAlive()
    def checkMove(self, currentRoomName, nextRoomName):
        """Checks to see if the next move is viable."""
        blair = ["Experiment Room","Dining Room"]
        experiment = ["Blair's Room","Dining Room"]
        dining = ["Blair's Room","Experiment Room", "Hangar", "Kitchen", "Thawing Room"]
        hangar = ["Dining Room", "Dog Room", "Thawing Room"]
        dog = ["Hangar", "Security Room"]
        thawing = ["Dining Room","Hangar", "Kitchen", "Foyer"]
        foyer = ["Thawing Room"]
        security = ["Dog Room"]
        kitchen = ["Dining Room", "Thawing Room"]
        if currentRoomName == "Blair's Room":
            if nextRoomName not in blair: return False
            else: return True
        if currentRoomName == "Experiment Room":
            if nextRoomName not in experiment: return False
            else: return True
        if currentRoomName == "Dining Room":
            if nextRoomName not in dining: return False
            else: return True
        if currentRoomName == "Hangar":
            if nextRoomName not in hangar: return False
            else: return True
        if currentRoomName == "Dog Room":
            if nextRoomName not in dog: return False
            else: return True
        if currentRoomName == "Thawing Room":
            if nextRoomName not in thawing: return False
            else: return True
        if currentRoomName == "Foyer":
            if nextRoomName not in foyer: return False
            else: return True
        if currentRoomName == "Security Room":
            if nextRoomName not in security: return False
            else: return True
        if currentRoomName == "Kitchen":
            if nextRoomName not in kitchen: return False
            else: return True
        return True
    def randomize(self):
        """Tries to move people from one room to the next, randomly."""
        noMove = ["Blair","MacReady"]
        for char in range(len(self._charList)):
            charName = self._charList[char].getName()
            if charName not in noMove and self.isAlive(charName):
                currentRoom = self.findCharObj(charName).getRoomName()
                nextRoom = random.choice(self._roomList).getName()
                check = self.checkMove(currentRoom, nextRoom)
                if check ==True:
                    self.changeRoom(charName, nextRoom)
    def isAlive(self, characterName):
        """Checks if a character is alive or not; True for alive, False for dead."""
        return self.findCharObj(characterName).isAlive()

def parse(string):
    """Parses through a string, returns a list with a command and target."""
    twoWords = [""]
    command = string.split(" ")
    if (len(command) == 1):
        return command
    if command[1] == 'to':
        if len(command) == 3:
            verb = command[0]
            target = command[2]
            newList = [verb, target]
            return newList
        else:
            verb = command[0]
            target = " ".join([command[2], command[3]])
            newList = [verb, target]
            return newList
    else:
        if len(command) == 2:
            verb = command[0]
            target = command[1]
            newList = [verb, target]
            return newList
        else:
            verb = command[0]
            target = " ".join([command[1], command[2]])
            newList = [verb, target]
            return newList
    
def cleanInput(string):
    """Takes user input and normalizes it."""
    cleanString = string.upper()
    newString = ""
    if cleanString == "BLAIR'S ROOM" or cleanString == "BLAIRS ROOM":
        newString = "Blair's Room"
    elif cleanString == "EXPERIMENT ROOM":
        newString = "Experiment Room"
    elif cleanString == "DINING ROOM":
        newString = "Dining Room"
    elif cleanString == "HANGAR":
        newString = "Hangar"
    elif cleanString == "DOG ROOM" or cleanString == "DOGS ROOM" or cleanString == "DOG'S ROOM":
        newString = "Dog Room"
    elif cleanString == "THAWING ROOM":
        newString = "Thawing Room"
    elif cleanString == "FOYER":
        newString = "Foyer"
    elif cleanString == "SECURITY ROOM":
        newString = "Security Room"
    elif cleanString == "KITCHEN":
        newString = "Kitchen"
    else:
        print("Check command and try again")
        return ""
    return newString
        
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
        
def turn(g):
    """Controls the events that happen each turn."""
    userInput = str(input("What would you like to do? "))
    userInput = parse(userInput)
    command = userInput[0].upper()
    MacReady = g.findCharObj("MacReady")
    occupants = g.findRoomObj(MacReady.getRoomName()).occupantNames()
    if command == 'MOVE':
        if len(userInput) < 2:
            print("Check command and try again. Make sure the action preceeds the destination.")
            return
        move = g.changePlayerRoom(userInput[1])
        if move == True:
            g.incTurnCount()
            print()
            if MacReady.getRoomName() != "Blair's Room":
                print(str(occupants)+" are in the room.")
                g.randomize()
                return
            else:
                print(str(occupants)+" are in the room.")
                g.randomize()
                return
        if move == False:
            return
    if command == "WAIT":
        g.incTurnCount()
        print("MacReady waited around a while.")
        print(str(occupants)+" are in the room.")
        g.randomize()
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
    """Runs test conditions and game."""
    roomObjs = createRoomObjs(roomNames)
    charObjs = createCharObjs(charNames, roomObjs)
    permCharList = assignCharsToRooms(charObjs, roomObjs)
    g = Control(roomObjs, permCharList)
    g.setupGame()
    
    #print("---------(Setting up game)---------")
    #g.showRooms()
    #print("---------(Finding a character)---------")
    #print(g.findCharObj("Blair"))
    #print("---------(Finding a room)----------")
    #print(g.findRoomObj("Blair's Room"))
    #print("---------(Changing a character's room)---------")
    #g.changeRoom("Blair", "Blair's Room")
    #print(g.findCharObj("Blair"))
    #print()
    #print(g.findRoomObj("Blair's Room"))
    #print("----------(Kills a couple characters)---------")
    #g.findCharObj("Fuches").kill()
    #g.findCharObj("Windows").kill()
    #g.findCharObj("Childs").kill()
    #print("----------(Status before randomize)-----------")
    #g.showRooms()
    #print("----------(Randomize)---------")
    #g.randomize()
    #print("----------(Status after randomize)-----------")
    #g.showRooms()
    #print("----------(Infects a character)---------")
    #print(g.findCharObj('Childs'))
    #print()
    #g.infect("Childs")
    #print(g.findCharObj('Childs'))
    #print("----------(Find the player)----------")
    #g.showPlayer()
    print("----------(Test game)----------")
    print("The Thing")
    g.findCharObj("MacReady").addVisited()
    while g.checkPlayer() == True:
        print()
        print("Turn " + str(g.getTurnCount()))
        turn(g)

if __name__ == '__main__':
    main()
