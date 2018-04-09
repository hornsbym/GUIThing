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
    def getInfectedCount(self):
        """Returns how many characters are infected."""
        count = 0
        for char in range(len(self._charList)):
            if self._charList[char].getInfectedStatus() == True:
                count += 1
        return count
    def incTurnCount(self):
        """Increments the turn count by one."""
        self._turnCount += 1
    def getTurnCount(self):
        """Returns the current turn count."""
        return self._turnCount
    def setupGame(self):
        """Puts player and Blair in Blair's Room; infects between 1-3 other characters."""
        self.changeRoom("MacReady", "Blair's Room")
        self.changeRoom("Blair", "Blair's Room")
        infectedOne = random.choice(self._charList)
        infectedTwo = random.choice(self._charList)
        infectedThree = random.choice(self._charList)
        print(infectedOne.getName())
        print(infectedTwo.getName())
        print(infectedThree.getName())
        if infectedOne.getName() != "Blair" and infectedOne.getName() != "MacReady":
            infectedOne.setInfectedStatus()
        if infectedTwo.getName() != "Blair" and infectedTwo.getName() != "MacReady":
            infectedTwo.setInfectedStatus()
        if infectedThree.getName() != "Blair" and infectedThree.getName() != "MacReady":
            infectedThree.setInfectedStatus()
    def showRooms(self):
        """Displays each room in the game along with its occupants"""
        for x in range(len(self._roomList)):
            if len(self._roomList[x].occupantNames()) > 0:
                print(self._roomList[x])
                print()
    def showInfectedChars(self):
        """Displays each player, their room, and their infected status."""
        infected = []
        for x in range(len(self._charList)):
            if self._charList[x].getInfectedStatus() == True:
                infected.append(self._charList[x].getName())
        print(infected)
        print()
    def showCharsInRoom(self):
        """Prints all characters in the room."""
        playerRoom = self.findRoomObj(self.findCharObj('MacReady').getRoomName())
        for char in range(len(playerRoom.occupantNames())):
            charName = playerRoom.occupantNames()[char]
            charStatus = self.findCharObj(charName).isAlive()
            if charName != "MacReady" and charStatus == True:  
                print(charName + " is in the room.")
        for char in range(len(playerRoom.occupantNames())):
            charName = playerRoom.occupantNames()[char]
            charStatus = self.findCharObj(charName).isAlive()
            if charName != "MacReady" and charStatus == False:
                print(charName + "'s charred remains are in the room.")
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
    def thingsAttack(self):
        """Called every turn, allows infected characters to attack."""
        for room in range(len(self._roomList)):
            self._roomList[room].thingsAttack()
        
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

def fixCharName(string):
    """Normalizes a character's name."""
    charName = string.upper()
    newCharName = ""
    if charName == "BLAIR":
        newCharName = "Blair"
    elif charName == "MACREADY":
        newCharName = "MacReady"
    elif charName == "FUCHES":
        newCharName = "Fuches"
    elif charName == "WINDOWS":
        newCharName = "Windows"
    elif charName == "COPPER":
        newCharName = "Copper"
    elif charName == "CHILDS":
        newCharName = "Childs"
    elif charName == "BARCLAY":
        newCharName = "Barclay"
    elif charName == "BENNINGS":
        newCharName = "Bennings"
    elif charName == "CLARKE":
        newCharName = "Clarke"
    elif charName == "NORRIS":
        newCharName = "Norris"
    elif charName == "VAN" or charName == "VAN WALL" or charName == "VANWALL":
        newCharName = "Van Wall"
    elif charName == "CONNANT":
        newCharName = "Connant"
    else:
        print("That's not a character.")
        return False
    return newCharName
    
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
        g.thingsAttack()
        g.randomize()
        if move == True:
            g.incTurnCount()
            print()
            if MacReady.getRoomName() != "Blair's Room":
                g.showCharsInRoom()
                g.showRooms()
                return
            else:
                g.showCharsInRoom()
                g.showRooms()
                return
        if move == False:
            return
    if command == "KILL":
        char = fixCharName(userInput[1])
        if char == None:
            return
        target = g.findCharObj(char)
        macReadyRoom = MacReady.getRoomName()
        if target.getName() in occupants:
            print("MacReady torched " + target.getName() + ".")
            target.kill()
            g.thingsAttack()
            g.randomize()
            g.incTurnCount()
            return
        else:
            print("Make sure target is in the room.")
            return
    if command == "TAKE":
        item = userInput[1].upper()
        if item == "BLOOD":
            name = input("Whose blood would you like to collect?")
            name = fixCharName(name)
            if name == False:
                print("Try again.")
                return
            else:
                add = MacReady.addInventory(name)
                print("add = " + str(add))
                if add == True:
                    print("Inventory added.")
                if add == False: 
                    print("Inventory full.")
                return
    if command == "WAIT":
        g.incTurnCount()
        g.thingsAttack()
        g.randomize()
        print("MacReady waited around a while.")
        g.showCharsInRoom()
        return
    if command == 'STATUS':
        print()
        g.showRooms()
        print("Inventory: "+str(MacReady.getInventory()))
        return
    if command == "INFECTED":
        print()
        g.showInfectedChars()
        return
    if command == 'LOOK':
        print()
        g.showPlayer()
        g.showCharsInRoom()
        return
    if command == 'HELP':
        print("Commands are move, kill, look, wait, status, help, and quit.")
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
    #print("----------(Things Attack)----------")
    #testTurn = 1
    #while g.getInfectedCount() != 12:        
    #    g.thingsAttack()
    #    g.randomize()
    #    print("Turn " + "%2s" % (str(testTurn)) + ": " + str(g.getInfectedCount()))
    #    testTurn += 1
    #print("___________")
    #print(testTurn)
    #print('----------(Fix Char Name Func)---------')
    #childs = fixCharName('ChIlDs')
    #print(childs)
    #fuches = fixCharName("fuches")
    #print(fuches)
    #vanwall = fixCharName("VanWall")
    #print(vanwall)
    print("----------(Test game)----------")
    g.findCharObj("MacReady").addVisited()
    while g.checkPlayer() == True:
        print('')
        print("---------<Turn " + str(g.getTurnCount()) + ">---------")
        if g.getInfectedCount() == 1:
            print("There is " + str(g.getInfectedCount()) + " infected person in the base.")
        else:
            print("There are " + str(g.getInfectedCount()) + " infected people in the base.")
        print('')
        #g.showRooms()
        turn(g)
        
if __name__ == '__main__':
    main()
