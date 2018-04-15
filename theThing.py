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
            return False
        elif self.checkMove(self.findCharObj("MacReady").getRoomName(), userInput) == None:
            return None
        else:
            self.changeRoom("MacReady", userInput)
            return True
    def infect(self, characterName):
        """Infects a specified character."""
        self.findCharObj(characterName).setInfectedStatus()
    def showPlayer(self):
        """Finds and prints the current location of the player."""
        location = self.findCharObj("MacReady").getRoomName()
        return location
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
    def occupants(self):
        """Returns a formatted string of characters in MacReady's room."""
        mac = self.findCharObj("MacReady")
        occupants = self.findRoomObj(mac.getRoomName()).occupantNames()
        string = ""
        for char in range(len(occupants)):
            if self.findCharObj(occupants[char]).isAlive() == True:
                string += occupants[char] + " \n"
        return string
    def inventory(self):
        """Returns formatted string representing inventory items."""
        inv = self.findCharObj("MacReady").getInventory()
        strInv = ""
        if len(inv) == 0:
            return "Empty"
        for i in range(len(inv)):
            strInv += inv[i] + "\n"
        return strInv
    def strInfected(self):
        """Returns a formatted string representation of tested infected."""
        string = ''
        if len(self._knownInfected) > 0:
            for x in range(len(self._knownInfected)):
                status = self.findCharObj(self._knownInfected[x]).isAlive()
                if status == True:
                    string += self._knownInfected[x] +", Alive\n"
                else:
                    string += self._knownInfected[x]+", Dead\n"
            return string
        else:
            string = "No confirmed infected yet.\n"
            return string
    def strUninfected(self):
        """Returns string representation of people who have tested negative for being infected."""
        string = ''
        if len(self._possiblyHuman) > 0:
            for x in range(len(self._possiblyHuman)):
                status = self.findCharObj(self._possiblyHuman[x]).isAlive()
                if status == True:
                    string += self._possiblyHuman[x]+", Alive\n"
                else:
                    string += self._possiblyHuman[x]+", Dead\n"
            return string
        else:
            string = "No blood tests conducted yet.\n"
            return string
    def showMap(self):
        """Returns string map."""
        return baseMap2
    def getStats(self):
        """Gets and returns a formatted string for the end-game stats."""
        aHumans = ""
        aliveCount = 0
        dHumans = ""
        deadCount = 0
        aInfected = ""
        dInfected = ""
        for char in range(len(self._charList)):
            character = self._charList[char]
            name = character.getName()
            if character.isAlive() == True and character.getInfectedStatus() == False:
                aHumans += "   -"+name+"\n"
                aliveCount += 1
            if character.isAlive() == True and character.getInfectedStatus() == True:
                aInfected += "   -"+name+"\n"
            if character.isAlive() == False and character.getInfectedStatus() == False:
                dHumans += "   -"+name+"\n"
                deadCount += 1
            if character.isAlive() == False and character.getInfectedStatus() == True:
                dInfected += "   -"+name+"\n"
        score = (50*aliveCount)-(25*deadCount)-(.3*(self.getTurnCount()))
        if len(aInfected) == 0:
            score += 100
        if score > 0 and self.checkPlayer()==True:
            score = round(score)
        if score < 0 or self.checkPlayer()==False:
            score = 0
        return "Surviving humans:\n"+aHumans+"\nDead Humans: \n"+dHumans+"\nSurviving Things:\n"+aInfected+"\nDead Things:\n"+dInfected+"\nScore:"+str(score)
        
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

def newParse(string):
    """Improved parse function. Takes a string of words, returns a list of commands."""
    negate = ["TO", "FROM"]
    join = ["DINING","EXPERIMENT","VAN","DOG","BLAIR'S","THAWING","SECURITY","FUCHES'","WINDOWS'","COPPER'S","CHILDS'","BARCLAY'S","BENNINGS'","CLARKE'S","NORRIS'"\
            ,"VAN WALL'S","CONNANT'S"]
    words = []
    string = string.upper()
    string = string.strip()
    lyst = string.split(" ")
    print(lyst)
    for x in range(len(lyst)):
        if lyst[x] not in negate:
            print("Word: " + lyst[x])
            if lyst[x] == "VAN":
                newWord = lyst[x]+ " " + lyst[x+1]
                lyst[x+1] = ''
                words.append(newWord)
            else:
                words.append(lyst[x])
    if "" in words:
        words.remove('')
    for x in range(len(words)):
        if words[x] in join:
            newWord = words[x] + " " + words[x+1]
            words[x] = newWord
            words[x+1]= ""
    if "" in words:
        words.remove('')
    return words
    
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
        
def turn(g, userInput):
    """Controls the events that happen each turn."""
    MacReady = g.findCharObj("MacReady")
    occupants = g.findRoomObj(MacReady.getRoomName()).occupantNames()
    MacReady.addVisited()
    userInput = newParse(userInput)
    command = userInput[0].upper()
    if command == 'MOVE' or command == 'GO':
        if len(userInput) < 2:
            error = "Please specify the destination."+"\n"
            return desc + error
        attack = g.thingsAttack()
        if attack == True:
            death = str(random.choice(deathMessages)) + "\n\n"+"Macready died." + "\n\n" + "Press 'Enter' to view score."
            g.endGame()
            return desc + death
        move = g.changePlayerRoom(userInput[1])
        if MacReady.getRoomName() not in MacReady.getVisited():
            desc = str(roomDict[MacReady.getRoomName()]) + "\n\n"
        if MacReady.getRoomName() in MacReady.getVisited():
            desc = ""
        g.randomize()
        if move == True:
            g.incTurnCount()
            if MacReady.getRoomName() != "Blair's Room":
                moveOne = "Moved to the " + str(MacReady.getRoomName()) +"." + "\n\n"
                return moveOne + desc
            else:
                moveTwo = "Moved to " + str(MacReady.getRoomName())+"."+"\n\n"
                return moveTwo + desc
        if move == False:
            noMove = "Can't get there from here!" + "\n\n"
            return noMove + desc
        if move == None:
            noMove = "You're already there." + "\n\n"
            return noMove + desc
    if command == "KILL":
        if len(userInput) < 2:
            error = "Please specify the target." + "\n\n"
            return error
        char = fixCharName(userInput[1])
        if char == False:
            error = "That's not a character. Check spelling and try again." + '\n\n'
            return error
        if g.findCharObj(char).isAlive() == False:
            warning = char + " is already dead!" + "\n\n"
            return warning
        if char == "MacReady":
            warning = "You can't torch yourself!" + "\n\n"
            return warning
        if char == "Blair":
            warning = 'MacReady - "No! I need Blair to test blood."' + "\n\n"
            return warning
        target = g.findCharObj(char)
        macReadyRoom = MacReady.getRoomName()
        if target.getName() in occupants:
            target.kill()
            kill = "MacReady torched " + target.getName() + "." +"\n\n"
            attack = g.thingsAttack()
            if attack == True:
                death = str(random.choice(deathMessages)) + "\n\n"+"Macready died." + "\n\n" + "Press 'Enter' to view score."
                g.endGame()
                return death
            if g.getInfectedCount() == 1:
                kill += "There is " + str(g.getInfectedCount()) + " infected person in the base."+"\n\n"
            else:
                kill += "There are " + str(g.getInfectedCount()) + " infected people in the base." + "\n\n"
            g.randomize()
            g.incTurnCount()
            return kill
        else:
            miss = "Make sure target is in the room." + "\n\n"
            return miss
    if command == "TAKE":
        if len(userInput) < 2:
            error = "Please specify the item to be taken, or type a character's name to collect a blood sample." + "\n\n"
            return error
        item = userInput[1].upper()
        if item == "BLOOD":
            name = userInput[2].upper()
            name = fixCharName(name)
            print(name)
            if name == False:
                error = "Try again." + "\n\n"
                return error
            if name == "MacReady":
                error = '''MacReady - "Probably not necessary... I know I'm not infected."''' + "\n\n"
                return error
            if name == "Blair":
                error = '''MacReady - "Hmm... the old man's locked up pretty tight. I doubt he's infected."''' + "\n\n"
                return error
            if g.findCharObj(name).isAlive()== False:
                error = "They're too badly burned to collect any blood." + "\n\n"
                return error
            else:
                if name[-1] == 's':
                    add = MacReady.addInventory(name +"' blood")
                    if add == True:
                        attack = g.thingsAttack()
                        if attack == True:
                            death = str(random.choice(deathMessages)) + "\n\n"+"Macready died." + "\n\n" + "Press 'Enter' to view score."
                            g.endGame()
                            return death
                        yes = name + "' blood added to inventory." + "\n\n"
                        g.randomize()
                        g.incTurnCount()
                        return yes
                    if add == False:
                        no = "Inventory full." + "\n\n"
                        return no
                else:    
                    add = MacReady.addInventory(name +"'s blood")
                    if add == True:
                        attack = g.thingsAttack()
                        if attack == True:
                            death = str(random.choice(deathMessages)) + "\n\n"+"Macready died." + "\n\n" + "Press 'Enter' to view score."
                            g.endGame()
                            return death
                        yes = name + "'s blood added to inventory." + "\n\n"
                        g.randomize()
                        g.incTurnCount()
                        return yes
                    if add == False: 
                        no = "Inventory full." + "\n\n"
                        return no
        if item == "KEY":
            if MacReady.getRoomName() == "Security Room":
                if "Key" not in MacReady.getInventory():
                    attack = g.thingsAttack()
                    if attack == True:
                        death = str(random.choice(deathMessages)) + "\n\n"+"Macready died." + "\n\n" + "Press 'Enter' to view score."
                        g.endGame()
                        return death
                    MacReady.addInventory("Key")
                    yes = "Key added to inventory." + '\n\n'
                    g.randomize()
                    g.incTurnCount()
                    return yes
                else:
                    no = "You already have the key!" + "\n\n"
                    return no
            else:
                no = "There's no key here." + "\n\n"
                return no
    if command == "GIVE" or command == "TEST":
        if len(userInput) < 2:
            error = "Please which item to give." + "\n\n"
            return error
        if MacReady.getRoomName() != "Blair's Room":
            error = "You can only give items to Blair. Find him in Blair's Room!" + "\n\n"
            return error
        else:
            if "BLOOD" not in userInput[1].upper():
                error = "You can only give Blair blood for testing." + "\n\n"
                return error
            else:
                blood = userInput[1]
                charName = blood[:-6]
                if charName[-1] == "S":
                    charName = charName[:-2]
                if charName[-1] == "'":
                    charName = charName[:-1]
                charName = fixCharName(charName)
                upperInv = []
                for x in range(len(MacReady.getInventory())):
                    newItem = MacReady.getInventory()[x].upper()
                    upperInv.append(newItem)
                if blood in upperInv:
                    for x in range(len(upperInv)):
                        if blood == upperInv[x]:
                            MacReady.removeInventory(x)
                    result = "Gave Blair "+ charName + "blood." + "\n"
                    if g.isInfected(charName) == True:
                        infected = 'Blair - "' + charName + ' is infected!"' + "\n\n"
                        g.addKnownInfected(charName)
                        return infected
                    else:
                        notInfected = 'Blair - "'+charName + ' is not infected."' + "\n\n"
                        g.addKnownUninfected(charName)
                        return notInfected
                else:
                    nope = "You don't have that item!" + "\n\n"
                    return nope
    if command == "USE":
        if len(userInput) < 2:
            error = "Please specify which item to use." + "\n\n"
            return error
        item = userInput[1].upper()
        if item == "KEY":
            if MacReady.getRoomName() == "Foyer":
                if "Key" in MacReady.getInventory():
                    used = "Used the key to unlock the base's door. You escaped!" + "\n\n"
                    g.endGame()
                    return used
                else:
                    notUsed = "No key in inventory. Find it in the security room!" + "\n\n"
                    return notUsed
            else:
                if "Key" in MacReady.getInventory():
                    notUsed = "You can only use the key in the Foyer!" + "\n\n"
                    return notUsed
                else:
                    notUsed = "No key in inventory. Find it in the security room!" + "\n\n"
                    return notUsed
        else:
            notUsed = "You can't use that." + "\n\n"
            return notUsed
    if command == "WAIT":
        attack = g.thingsAttack()
        if attack == True:
            death = str(random.choice(deathMessages)) + "\n\n"+"Macready died." + "\n\n" + "Press 'Enter' to view score."
            g.endGame()
            return death
        wait = "MacReady waited around a while." +"\n\n" 
        g.randomize()
        g.incTurnCount()
        return wait
    if command == 'LOOK':
        desc = str(roomDict[MacReady.getRoomName()]) + "\n\n"
        if MacReady.getRoomName() == "Security Room" and "Key" not in MacReady.getInventory():
            key = "A rather large key is hanging on the wall." + "\n\n"
        else:
            key = ""
        return desc + key
    if command == "TALK":
        target = random.choice(occupants)
        if len(occupants) == 1:
            nope = "Nobody to talk to." + "\n\n"
            return nope
        if target == "MacReady" or g.findCharObj(target).isAlive() == False:
            for x in range(len(occupants)):
                target = occupants[x]
                if target != "MacReady" and g.findCharObj(target).isAlive() == True:
                    break
                else:
                    target = None
        if target == None:
            nope = "No one's alive to talk to." + "\n\n"
            return nope
        talk = target+' - '+random.choice(dialogue) + "\n\n"
        return talk
    if command == 'HELP':
        message = "Recognized commands and their effects are: \n\n" + \
        '- Move: Moves the player to an adjacent room.\n'+\
        '- Kill: Kills the specified character.\n'+\
        '- Take: Takes an item from the room or collects a blood sample.\n'+\
        '- Give: Gives blood from the inventory to Blair.\n'+\
        '- Use: Uses an item in the inventory (only the key, currently).\n'+\
        '- Wait: Passes one turn in the same room.\n'+\
        '- Look: Gives specifics around the room. Does not cost a turn.\n'+\
        '- Talk: Talks to someone in the room.\n'+\
        '- Help: Displays the commands and their effects.\n'+\
        '- Quit: MacReady ends it all...\n\n'
        return message
    if command == "QUIT":
        g.findCharObj("MacReady").kill()
        death = str(random.choice(deathMessages)) + "\n\n"+"Macready died." + "\n\n" + "Press 'Enter' to view score."
        g.endGame()
        return kill
    else:
        message = "Please try a different command. Recognized commands are:\n\n"+\
        '- Move\n'+\
        '- Kill\n'+\
        '- Take\n'+\
        '- Give\n'+\
        '- Use\n'+\
        '- Wait\n'+\
        '- Look\n'+\
        '- Talk\n'+\
        '- Help\n'+\
        '- Quit\n\n'
        return message
    
def main():
    """Runs test conditions and game."""
    roomObjs = createRoomObjs(roomNames)
    charObjs = createCharObjs(charNames, roomObjs)
    permCharList = assignCharsToRooms(charObjs, roomObjs)
    g = Control(roomObjs, permCharList)
    g.setupGame()

##    check = False
##    while check == False:
##        o = openingSequence()
##        if o == True:
##            check = True
##    print("--------------------| THE THING |--------------------")
##    while g.checkPlayer() == True and g.continueGame() == True:
##        turn(g)
##    if g.checkPlayer() == False:
##        print("Macready died.")
##        print()
##        g.printStats()
##        print()
##        print(creditMessage)
##        return
##    if g.checkPlayer() == True:
##        if g.getInfectedCount() > 0:
##            print("MacReady escaped, but so did The Thing.")
##            print()
##            g.printStats()
##            print()
##            print(creditMessage)
##            return
##        else:
##            if g.getAliveCount() > 2:
##                print("MacReady escaped with survivors. Best ending possible.")
##                print()
##                g.printStats()
##                print()
##                print(creditMessage)
##                return
##            else:
##                print("MacReady escaped without survivors. The world survives, but he is imprisoned for murder.")
##                print()
##                g.printStats()
##                print()
##                print(creditMessage)
##                return

    test1 = newParse("Move to dining room")
    print(test1)
    test2 = newParse("Take blood from blair")
    print(test2)
    test3 = newParse("Take blood from van wall")
    print(test3)
    test4 = newParse("Give blair's blood")
    print(test4)
    test5 = newParse("Give bennings' blood")
    print(test5)
    test6 = newParse("Give Van Wall's blood")
    print(test6)
if __name__ == '__main__':
    main()
