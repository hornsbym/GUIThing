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
        self._knownInfected = []
        self._possiblyHuman = []
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
        score = (50*len(aHumans))-(25*len(dHumans))-(.3*(self.getTurnCount()))
        if len(aInfected) == 0:
            score += 100
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
        print()
        if score > 0 and self.checkPlayer()==True:
            print("Score: "+str(round(score)))
        if score < 0 or self.checkPlayer()==False:
            print("Score: 0")
    def getInfectedCount(self):
        """Returns how many characters are infected."""
        count = 0
        for char in range(len(self._charList)):
            if self._charList[char].getInfectedStatus() == True and self._charList[char].isAlive() == True:
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
            if self._charList[x].getInfectedStatus() == True and self._charList[x].isAlive() == True:
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
            print("You can't get there from here!")
            print()
            return False
        elif self.checkMove(self.findCharObj("MacReady").getRoomName(), userInput) == None:
            print("But you're already there...")
            print()
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
            return None
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
        return False
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
                    return True
                else:
                    self.infect(infectedName)
    def showInventory(self, inventory):
        """Displays MacReady's inventory."""
        print("Inventory:")
        if len(inventory) == 0:
            print("    -Empty")
            return
        for item in range(len(inventory)):
            print("    -" + str(inventory[item]))
    def addKnownInfected(self, thing):
        """Adds the name of a person who is definitely infected to a list."""
        if thing in self._knownInfected:
            return
        else:
            self._knownInfected.append(thing)
            if thing in self._possiblyHuman:
                self._possiblyHuman.remove(thing)
            return
    def addKnownUninfected(self, person):
        """Adds the name of a person who tested not infected."""
        if person in self._possiblyHuman:
            return
        else:
            self._possiblyHuman.append(person)
            return
    def showKnownInfected(self):
        """Shows people who have tested positive for being infected."""
        if len(self._knownInfected) > 0:
            print("Tested positive: ")
            for x in range(len(self._knownInfected)):
                status = self.findCharObj(self._knownInfected[x]).isAlive()
                if status == True:
                    print("   -"+self._knownInfected[x]+", Alive")
                else:
                    print("   -"+self._knownInfected[x]+", Dead")
            print()
            return
        else:
            print("No confirmed infected yet.")
            print()
            return
    def showKnownUninfected(self):
        """Shows people who have tested negative for being infected."""
        if len(self._possiblyHuman) > 0:
            print("Tested negative: ")
            for x in range(len(self._possiblyHuman)):
                status = self.findCharObj(self._possiblyHuman[x]).isAlive()
                if status == True:
                    print("   -"+self._possiblyHuman[x]+", Alive")
                else:
                    print("   -"+self._possiblyHuman[x]+", Dead")
            print()
            return
        else:
            print("No blood tests conducted yet.")
            print()
            return

def openingSequence():
    """Initializes the game."""
    print(openingMessage)
    print()
    command = input("Press enter to begin.")
    print()
    command = command.upper()
    if command == "":
        return True
    if command == "CREDITS":
        print(creditMessage)
        print()
        return False
    else:
        print("Type 'Credits' or just press enter.")
        print()
        return False

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
    occupants = g.findRoomObj(MacReady.getRoomName()).occupantNames()
    if MacReady.getRoomName() not in MacReady.getVisited():
        print()
        print(roomDict[MacReady.getRoomName()])
        print()
    MacReady.addVisited()
    print("---------<Turn " + str(g.getTurnCount()) + ", "+MacReady.getRoomName()+">---------")
    print("People in room: ")
    for x in range(len(occupants)):
        if g.findCharObj(occupants[x]).isAlive() == True:
            print("   - "+occupants[x])
    print()
    userInput = str(input("What would you like to do? "))
    print()
    userInput = parse(userInput)
    command = userInput[0].upper()
    if command == 'MOVE' or command == 'GO':
        if len(userInput) < 2:
            print("Please specify the destination.")
            print()
            return
        attack = g.thingsAttack()
        if attack == True:
            print(random.choice(deathMessages))
            print()
            return
        move = g.changePlayerRoom(userInput[1])
        g.randomize()
        if move == True:
            g.incTurnCount()
            if MacReady.getRoomName() != "Blair's Room":
                print("Moved to the " + MacReady.getRoomName()+".")
                print()
                return
            else:
                print("Moved to " + MacReady.getRoomName()+".")
                print()
                return
        if move == False:
            return
    if command == "KILL":
        if len(userInput) < 2:
            print("Please specify the target.")
            print()
            return
        char = fixCharName(userInput[1])
        if char == False:
            print("That's not a character. Check spelling and try again.")
            print()
            return
        if g.findCharObj(char).isAlive() == False:
            print(char + " is already dead!")
            print()
            return
        if char == "MacReady":
            print("You can't torch yourself!")
            print()
            return
        if char == "Blair":
            print('MacReady - "No! I need Blair to test blood."')
            print()
            return
        target = g.findCharObj(char)
        macReadyRoom = MacReady.getRoomName()
        if target.getName() in occupants:
            target.kill()
            print("MacReady torched " + target.getName() + ".")
            print()
            attack = g.thingsAttack()
            if attack == True:
                print(random.choice(deathMessages))
                print()
                return
            if g.getInfectedCount() == 1:
                print("There is " + str(g.getInfectedCount()) + " infected person in the base.")
            else:
                print("There are " + str(g.getInfectedCount()) + " infected people in the base.")
            print()
            g.randomize()
            g.incTurnCount()
            return
        else:
            print("Make sure target is in the room.")
            print()
            return
    if command == "TAKE":
        if len(userInput) < 2:
            print("Please specify the item to be taken, or type a character's name to collect a blood sample.")
            return
        item = userInput[1].upper()
        if item == "BLOOD":
            name = input('MacReady - "Whose blood should I collect?" ')
            print()
            name = fixCharName(name)
            if name == False:
                print("Try again.")
                print()
                return
            if name == "MacReady":
                print('''MacReady - "Probably not necessary... I know I'm not infected."''')
                print()
                return
            if name == "Blair":
                print('''MacReady - "Hmm... the old man's locked up pretty tight. I doubt he's infected."''')
                print()
                return
            if g.findCharObj(name).isAlive()== False:
                print("They're too badly burned to collect any blood.")
                print()
                return
            else:
                if name[-1] == 's':
                    add = MacReady.addInventory(name +"' blood")
                    if add == True:
                        attack = g.thingsAttack()
                        if attack == True:
                            print(random.choice(deathMessages))
                            print()
                            return
                        print(name + "' blood added to inventory.")
                        print()
                        g.randomize()
                        g.incTurnCount()
                        return
                    if add == False:
                        print("Inventory full.")
                        print()
                else:    
                    add = MacReady.addInventory(name +"'s blood")
                    if add == True:
                        attack = g.thingsAttack()
                        if attack == True:
                            print(random.choice(deathMessages))
                            print()
                            return                        
                        print(name + "'s blood added to inventory.")
                        print()
                        g.randomize()
                        g.incTurnCount()
                        return
                    if add == False: 
                        print("Inventory full.")
                        print()
                return
        if item == "KEY":
            if MacReady.getRoomName() == "Security Room":
                if "Key" not in MacReady.getInventory():
                    attack = g.thingsAttack()
                    if attack == True:
                        print(random.choice(deathMessages))
                        print()
                        return   
                    MacReady.addInventory("Key")
                    print("Key added to inventory.")
                    print()
                    g.randomize()
                    g.incTurnCount()
                    return
                else:
                    print("You already have the key!")
                    print()
                    return
            else:
                print("There's no key here.")
                print()
                return
    if command == "GIVE":
        if len(userInput) < 2:
            print("Please specify the item to be given.")
            print()
            return
        if MacReady.getRoomName() != "Blair's Room":
            print("You can only give items to Blair. Find him in Blair's Room!")
            print()
            return
        else:
            if userInput[1].upper() != "BLOOD":
                print("You can only give Blair blood for testing.")
                print()
                return
            else:
                char = input('Blair - "Whose blood would you like to test?": ')
                print()
                char = fixCharName(char)
                if char == False or char == None:
                    print("Try again.")
                    print()
                    return
                if str(char+"'s blood") in MacReady.getInventory():
                    charName = MacReady.popInventory(char+"'s blood")
                    print("Gave Blair "+charName+" to test.")
                    print()
                    charName = fixBlood(charName)
                    if g.isInfected(charName) == True:
                        print('Blair - "' + charName + ' is infected!"')
                        print()
                        g.addKnownInfected(charName)
                    else:
                        print('Blair - "'+charName + ' is not infected."')
                        print()
                        g.addKnownUninfected(charName)
                    return
                elif str(char+"' blood") in MacReady.getInventory():
                    charName = MacReady.popInventory(char+"' blood")
                    print("Gave Blair "+charName+" to test.")
                    charName = fixBlood(charName)
                    if g.isInfected(charName) == True:
                        print('Blair - "' + charName + ' is infected!"')
                        print()
                        g.addKnownInfected(charName)
                    else:
                        print('Blair - "'+charName + ' is not infected."')
                        print()
                        g.addKnownUninfected(charName)
                    return
                else:
                    print("You don't have that item!")
                    print()
                    return 
    if command == "USE":
        if len(userInput) < 2:
            print("Please specify which item to use.")
            print()
            return
        item = userInput[1].upper()
        if item == "KEY":
            if MacReady.getRoomName() == "Foyer":
                if "Key" in MacReady.getInventory():
                    print("Used the key to unlock the base's door. You escaped!")
                    print()
                    g.endGame()
                    return
                else:
                    print("No key in inventory. Find it in the security room!")
                    print()
                    return
            else:
                if "Key" in MacReady.getInventory():
                    print("You can only use the key in the Foyer!")
                    print()
                    return
                else:
                    print("No key in inventory. Find it in the security room!")
                    print()
                    return
        else:
            print("You can't use that.")
            print()
            return
    if command == "WAIT":
        attack = g.thingsAttack()
        if attack == True:
            print(random.choice(deathMessages))
            print()
            return
        print("MacReady waited around a while.")
        print()
        g.randomize()
        g.incTurnCount()
        return
    if command == 'STATUS':
        print("...[Opening File]...")
        print()
        print("      Name: R.J. MacReady")
        print("Occupation: Meteorologist")
        print("  Location: Antarctic Research Base, " + MacReady.getRoomName())
        print("    Status: Alive")
        print("  Infected: Negative")
        print()
        g.showInventory(MacReady.getInventory())
        print()
        g.showKnownInfected()
        g.showKnownUninfected()
        if g.getInfectedCount() == 1:
            print("There is " + str(g.getInfectedCount()) + " infected person in the base.")
        else:
            print("There are " + str(g.getInfectedCount()) + " infected people in the base.")
        print("There are " + str(g.getAliveCount()) + " people still alive in the base.")
        print()
        return
    if command == 'LOOK':
        g.showPlayer()
        print()
        print(roomDict[MacReady.getRoomName()])
        print()
        g.showCharsInRoom()
        print()
        if MacReady.getRoomName() == "Security Room" and "Key" not in MacReady.getInventory():
            print("A rather large key is hanging on the wall.")
            print()
        return
    if command == "TALK":
        target = random.choice(occupants)
        if len(occupants) == 1:
            print("There's nobody here!")
            print()
            return
        if target == "MacReady" or g.findCharObj(target).isAlive() == False:
            for x in range(len(occupants)):
                target = occupants[x]
                if target != "MacReady" and g.findCharObj(target).isAlive() == True:
                    break
                else:
                    target = None
        if target == None:
            print("There's no one alive to talk to.")
            print()
            return
        print(target+' - '+random.choice(dialogue))
        print()
        return
    if command == "MAP":
        print(baseMap)
        print()
        return
    if command == 'HELP':
        print("Recognized commands and their effects are:")
        print() 
        print('-   Move: Moves the player to an adjacent room.')
        print('-   Kill: Kills the specified character.')
        print('-   Take: Takes an item from the room or collects a blood sample.')
        print('-   Give: Gives an item in the inventory to Blair. Only to be used with blood samples.')
        print('-    Use: Uses an item in the inventory (only the key, currently).')
        print('-   Wait: Passes one turn in the same room.')
        print("- Status: Displays the player's inventory. Does not cost a turn.")
        print('-   Look: Gives specifics around the room. Does not cost a turn.')
        print('-    Map: Displays a map of the base.')
        print('-   Talk: Talks to someone in the room.')
        print('-   Help: Displays the commands and their effects. Does not cost a turn.')
        print('-   Quit: The player ends it all...')
        print()
        return
    if command == "QUIT":
        g.findCharObj("MacReady").kill()
        print(random.choice(quitMessages))
        print()
        return
    else:
        print("Please try a different command. Recognized commands are:")
        print('   - Move to <name of adjacent room>')
        print('   - Kill <name of character in room>')
        print('   - Take <item or blood>')
        print('   - Give <item in inventory>')
        print('   - Use <item in inventory>')
        print('   - Wait')
        print('   - Status')
        print('   - Look')
        print('   - Map')
        print('   - Talk')
        print('   - Help')
        print('   - Quit')
        print()
        return
    
def main():
    """Runs test conditions and game."""
    roomObjs = createRoomObjs(roomNames)
    charObjs = createCharObjs(charNames, roomObjs)
    permCharList = assignCharsToRooms(charObjs, roomObjs)
    g = Control(roomObjs, permCharList)
    g.setupGame()

    check = False
    while check == False:
        o = openingSequence()
        if o == True:
            check = True
    print("--------------------| THE THING |--------------------")
    while g.checkPlayer() == True and g.continueGame() == True:
        turn(g)
    if g.checkPlayer() == False:
        print("Macready died.")
        print()
        g.printStats()
        print()
        print(creditMessage)
        return
    if g.checkPlayer() == True:
        if g.getInfectedCount() > 0:
            print("MacReady escaped, but so did The Thing.")
            print()
            g.printStats()
            print()
            print(creditMessage)
            return
        else:
            if g.getAliveCount() > 2:
                print("MacReady escaped with survivors. Best ending possible.")
                print()
                g.printStats()
                print()
                print(creditMessage)
                return
            else:
                print("MacReady escaped without survivors. The world survives, but he is imprisoned for murder.")
                print()
                g.printStats()
                print()
                print(creditMessage)
                return
        
if __name__ == '__main__':
    main()
