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
from descriptions import *

charNames = ['Fuches','Windows','Copper','Childs',"Barclay","Bennings","Clarke","Norris","Van Wall","Connant"]
roomNames = ['Kitchen', 'Experiment Room', 'Hangar', 'Dining Room', "Blair's Room", "Foyer", "Dog Room","Thawing Room","Security Room"]

class Control(object):
    """Instance that controls the game mechanics."""
    def __init__(self, roomList, charList):
        self._roomList = roomList
        self._charList = charList
        self._turnCount = 1
        self._continue = True
    def continueGame(self):
        """Determines whether a game can be continued."""
        return self._continue
    def endGame(self):
        """Ends the game without killing MacReady."""
        self._continue = False
        return 
    def printStats(self):
        """Gets and prints end-game stats."""
        aHumans = []
        dHumans = []
        aInfected = []
        dInfected = []
        for char in range(len(self._charList)):
            character = self._charList[char]
            name = character.getName()
            if character.isAlive() == True and character.getInfectedStatus() == False:
                aHumans.append(name)
            if character.isAlive() == True and character.getInfectedStatus() == True:
                aInfected.append(name)
            if character.isAlive() == False and character.getInfectedStatus() == False:
                dHumans.append(name)
            if character.isAlive() == False and character.getInfectedStatus() == True:
                dInfected.append(name)
        print("Surviving humans: ")
        for human in range(len(aHumans)):
            print("     -"+aHumans[human])
        print()
        print("Dead humans: ")
        for dHuman in range(len(dHumans)):
            print("     -"+dHumans[dHuman])
        print()
        print("Surviving Things: ")
        for thing in range(len(aInfected)):
            print("     -"+aInfected[thing])
        print()
        print("Dead Things: ")
        for dthing in range(len(dInfected)):
            print("     -"+dInfected[dthing])
    def getInfectedCount(self):
        """Returns how many characters are infected."""
        count = 0
        for char in range(len(self._charList)):
            if self._charList[char].getInfectedStatus() == True:
                count += 1
        return count
    def getAliveCount(self):
        """Returns how many characters are alive."""
        count = 0
        for char in range(len(self._charList)):
            if self._charList[char].isAlive() == True:
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
            self.infect(infectedOne.getName())
        if infectedTwo.getName() != "Blair" and infectedTwo.getName() != "MacReady":
            self.infect(infectedTwo.getName())
        if infectedThree.getName() != "Blair" and infectedThree.getName() != "MacReady":
            self.infect(infectedThree.getName())
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
        userInput = fixRoomName(roomName)
        if userInput == False:
            return False
        elif self.checkMove(self.findCharObj("MacReady").getRoomName(), userInput) == False:
            return False
        else:
            self.changeRoom("MacReady", userInput)
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
        if currentRoomName == nextRoomName:
            return False
        elif currentRoomName == "Blair's Room":
            if nextRoomName not in blair:
                return False
            else:
                return True
        elif currentRoomName == "Experiment Room":
            if nextRoomName not in experiment:
                return False
            else:
                return True
        elif currentRoomName == "Dining Room":
            if nextRoomName not in dining:
                return False
            else:
                return True
        elif currentRoomName == "Hangar":
            if nextRoomName not in hangar:
                return False
            else:
                return True
        elif currentRoomName == "Dog Room":
            if nextRoomName not in dog:
                return False
            else:
                return True
        elif currentRoomName == "Thawing Room":
            if nextRoomName not in thawing:
                return False
            else:
                return True
        elif currentRoomName == "Foyer":
            if nextRoomName not in foyer:
                return False
            else:
                return True
        elif currentRoomName == "Security Room":
            if nextRoomName not in security:
                return False
            else:
                return True
        elif currentRoomName == "Kitchen":
            if nextRoomName not in kitchen:
                return False
            else:
                return True
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
    def isInfected(self, characterName):
        """Checks if a character is infected or not; True for infected, False for not."""
        return self.findCharObj(characterName).getInfectedStatus()
    def thingsAttack(self):
        """Called every turn, allows infected characters to attack."""
        for room in range(len(self._roomList)):
            infectedName = self._roomList[room].thingsAttack()
            if infectedName != None:
                if infectedName == "MacReady":
                    self.findCharObj("MacReady").kill()
                else:
                    self.infect(infectedName)
    def showInventory(self, inventory):
        """Displays MacReady's inventory."""
        print("Inventory...")
        if len(inventory) == 0:
            print("Nothing!")
            return
        for item in range(len(inventory)):
            print("     -" + str(inventory[item]))

def parse(string):
    """Parses through a string, returns a list with a command and target."""
    twoWords = [""]
    string = string.strip()
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
        return False
    return newCharName
    
def fixRoomName(string):
    """Takes room name input and normalizes it."""
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
    elif cleanString == "DOG ROOM" or cleanString == "DOGS ROOM" or cleanString == "DOG'S ROOM" or cleanString =="DOGROOM":
        newString = "Dog Room"
    elif cleanString == "THAWING ROOM":
        newString = "Thawing Room"
    elif cleanString == "FOYER":
        newString = "Foyer"
    elif cleanString == "SECURITY ROOM" or cleanString == "SECURITYROOM":
        newString = "Security Room"
    elif cleanString == "KITCHEN":
        newString = "Kitchen"
    else:
        print("Make sure you spell room names correctly.")
        return False
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

def fixBlood(string):
    """Takes a blood string and assigns it to a person."""
    chars = ['Fuches','Windows','Copper','Childs',"Barclay","Bennings","Clarke","Norris","Van Wall","Connant"]
    blood = string
    for c in range(len(chars)):
        if blood == (chars[c]+"'s blood") or blood == (chars[c]+"' blood"):
            return chars[c]

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
    """Creates a list of room objects when given a list of room names."""
    roomObjects = []
    #Creates characters from information in charNames list
    for x in range(len(listOfRoomNames)):
        r = Room(listOfRoomNames[x])
        roomObjects.append(r)
    return roomObjects
        
def turn(g):
    """Controls the events that happen each turn."""
    MacReady = g.findCharObj("MacReady")
    if MacReady.getRoomName() not in MacReady.getVisited():
        print(roomDict[MacReady.getRoomName()])
        print()
    MacReady.addVisited()
    if g.getInfectedCount() == 1:
        print("There is " + str(g.getInfectedCount()) + " infected person in the base.")
    else:
        print("There are " + str(g.getInfectedCount()) + " infected people in the base.")
    print()
    print("---------<Turn " + str(g.getTurnCount()) + ">---------")
    userInput = str(input("What would you like to do? "))
    print()
    userInput = parse(userInput)
    command = userInput[0].upper()
    occupants = g.findRoomObj(MacReady.getRoomName()).occupantNames()
    if command == 'MOVE':
        if len(userInput) < 2:
            print("Please specify the destination.")
            return
        move = g.changePlayerRoom(userInput[1])
        g.thingsAttack()
        g.randomize()
        if move == True:
            g.incTurnCount()
            if MacReady.getRoomName() != "Blair's Room":
                print("Moved to the " + MacReady.getRoomName()+".")
                print()
                g.showCharsInRoom()
                print()
                return
            else:
                print("Moved to " + MacReady.getRoomName()+".")
                print()
                g.showCharsInRoom()
                print()
                return
        if move == False:
            return
    if command == "KILL":
        if len(userInput) < 2:
            print("Please specify the target.")
            return
        char = fixCharName(userInput[1])
        if char == False:
            print("That's not a character. Check spelling and try again.")
            return
        if g.findCharObj(char).isAlive() == False:
            print(char + " is already dead!")
            return
        if char == "MacReady":
            print("You can't torch yourself!")
            return
        target = g.findCharObj(char)
        macReadyRoom = MacReady.getRoomName()
        if target.getName() in occupants:
            print("MacReady torched " + target.getName() + ".")
            target.kill()
            target.setUninfected()
            g.thingsAttack()
            g.randomize()
            g.incTurnCount()
            return
        else:
            print("Make sure target is in the room.")
            return
    if command == "TAKE":
        if len(userInput) < 2:
            print("Please specify the item to be taken, or type a character's name to collect a blood sample.")
            return
        item = userInput[1].upper()
        if item == "BLOOD":
            name = input('MacReady - "Whose blood should I collect?"')
            name = fixCharName(name)
            if name == False:
                print("Try again.")
                return
            else:
                if name[-1] == 's':
                    add = MacReady.addInventory(name +"' blood")
                    if add == True:
                        print(name + "' blood added to inventory.")
                    if add == False:
                        print("Inventory full.")
                else:    
                    add = MacReady.addInventory(name +"'s blood")
                    if add == True:
                        print(name + "'s blood added to inventory.")
                    if add == False: 
                        print("Inventory full.")
                return
        if item == "KEY":
            if MacReady.getRoomName() == "Security Room":
                if "Key" not in MacReady.getInventory():
                    MacReady.addInventory("Key")
                    print("Key added to inventory.")
                    return
                else:
                    print("You already have the key!")
                    return
            else:
                print("There's no key here.")
                return
    if command == "GIVE":
        if len(userInput) < 2:
            print("Please specify the item to be given.")
            return
        if MacReady.getRoomName() != "Blair's Room":
            print("You can only give items to Blair. Find him in Blair's Room!")
            return
        else:
            if userInput[1].upper() != "BLOOD":
                print("You can only give Blair blood from other characters.")
                return
            else:
                char = input('Blair - "Whose blood would you like to test?": ')
                char = fixCharName(char)
                if str(char+"'s blood") in MacReady.getInventory():
                    charName = MacReady.popInventory(char+"'s blood")
                    print("Gave Blair "+charName+" to test.")
                    charName = fixBlood(charName)
                    if g.isInfected(charName) == True:
                        print('Blair - "' + charName + " has been infected!")
                    else:
                        print('Blair - "'+charName + " has not been infected.")
                    return
                elif str(char+"' blood") in MacReady.getInventory():
                    charName = MacReady.popInventory(char+"' blood")
                    print("Gave Blair "+charName+" to test.")
                    charName = fixBlood(charName)
                    if g.isInfected(charName) == True:
                        print('Blair - "' + charName + " has been infected!")
                    else:
                        print('Blair - "'+charName + " has not been infected.")
                    return
                else:
                    print("You don't have that item!")
                    return 
    if command == "USE":
        if len(userInput) < 2:
            print("Please specify which item to use.")
            return
        item = userInput[1].upper()
        if item == "KEY":
            if MacReady.getRoomName() == "Foyer":
                if "Key" in MacReady.getInventory():
                    print("Used the key to unlock the base's door. You escaped!")
                    g.endGame()
                    return
                else:
                    print("No key in inventory. Find it in the security room!")
                    return
            else:
                if "Key" in MacReady.getInventory():
                    print("You can only use the key in the Foyer!")
                    return
                else:
                    print("No key in inventory. Find it in the security room!")
                    return
        else:
            print("You can't use that.")
            return
    if command == "WAIT":
        g.incTurnCount()
        g.thingsAttack()
        g.randomize()
        print("MacReady waited around a while.")
        print()
        g.showCharsInRoom()
        print()
        return
    if command == 'STATUS':
        g.showInventory(MacReady.getInventory())
        print()
        return
    if command == "INFECTED":
        print()
        g.showInfectedChars()
        return
    if command == 'LOOK':
        g.showPlayer()
        g.showCharsInRoom()
        print(roomDict[MacReady.getRoomName()])
        print()
        return
    if command == 'HELP':
        print("Recognized commands and their effects are:")
        print('     - Move to <name of adjacent room>: Moves the player to an adjacent room.')
        print('     - Kill <name of character in room>: Kills the specified character.')
        print('     - Take <item or name of character in room>: Takes an item from the room or collects a blood sample.')
        print('     - Give <item in inventory>: Gives an item in the inventory to Blair. Only to be used with blood samples.')
        print('     - Use <item in inventory>: Uses an item in the inventory (only the key, currently).')
        print('     - Wait: Passes one turn in the same room.')
        print("     - Status: Displays the player's inventory. Does not cost a turn.")
        print('     - Look: Gives specifics around the room. Does not cost a turn.')
        print('     - Help: Displays the commands and their effects. Does not cost a turn.')
        print('     - Quit: The player ends it all...')
        print()
        return
    if command == "QUIT":
        g.findCharObj("MacReady").kill()
        print(random.choice(quitMessages))
        print()
        return
    else:
        print("Please try a different command. Recognized commands are:")
        print('     - Move to <name of adjacent room>')
        print('     - Kill <name of character in room>')
        print('     - Take <item or name of character in room>')
        print('     - Give <item in inventory>')
        print('     - Use <item in inventory>')
        print('     - Wait')
        print('     - Status')
        print('     - Look')
        print('     - Help')
        print('     - Quit')
        print()
        return
    
def main():
    """Runs test conditions and game."""
    roomObjs = createRoomObjs(roomNames)
    charObjs = createCharObjs(charNames, roomObjs)
    permCharList = assignCharsToRooms(charObjs, roomObjs)
    g = Control(roomObjs, permCharList)
    g.setupGame()
    
##    print("---------(Setting up game)---------")
##    g.showRooms()
##    print("---------(Finding a character)---------")
##    print(g.findCharObj("Blair"))
##    print("---------(Finding a room)----------")
##    print(g.findRoomObj("Blair's Room"))
##    print("---------(Changing a character's room)---------")
##    g.changeRoom("Blair", "Blair's Room")
##    print(g.findCharObj("Blair"))
##    print()
##    print(g.findRoomObj("Blair's Room"))
##    print("----------(Kills a couple characters)---------")
##    g.findCharObj("Fuches").kill()
##    g.findCharObj("Windows").kill()
##    g.findCharObj("Childs").kill()
##    print("----------(Status before randomize)-----------")
##    g.showRooms()
##    print("----------(Randomize)---------")
##    g.randomize()
##    print("----------(Status after randomize)-----------")
##    g.showRooms()
##    print("----------(Infects a character)---------")
##    print(g.findCharObj('Childs'))
##    print()
##    g.infect("Childs")
##    print(g.findCharObj('Childs'))
##    print("----------(Find the player)----------")
##    g.showPlayer()
##    print("----------(Things Attack)----------")
##    testTurn = 1
##    while g.checkPlayer() == True:        
##        g.thingsAttack()
##        g.randomize()
##        print("Turn " + "%2s" % (str(testTurn)) + ": " + str(g.getInfectedCount()) + " infected.")
##        testTurn += 1
##    print("___________")
##    print(testTurn)
##    print(g.checkPlayer())
##    print('----------(Fix Char Name Func)---------')
##    childs = fixCharName('ChIlDs')
##    print(childs)
##    fuches = fixCharName("fuches")
##    print(fuches)
##    vanwall = fixCharName("VanWall")
##    print(vanwall)
    print("----------(Test game)----------")
    while g.checkPlayer() == True and g.continueGame() == True:
        turn(g)
    if g.checkPlayer() == False:
        print("Macready died.")
        g.printStats()
        return
    if g.checkPlayer() == True:
        if g.getInfectedCount() > 0:
            print("MacReady escaped, but so did The Thing.")
            g.printStats()
            return
        else:
            if g.getAliveCount() > 1:
                print("MacReady escaped with survivors. Best ending possible.")
                g.printStats()
                return
            else:
                print("MacReady escaped without survivors. The world survives, but he is imprisoned for murder.")
                g.printStats()
                return
    
    
        
if __name__ == '__main__':
    main()
