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

charNames = ['MacReady','Blair','Copper','Childs']
roomNames = ['Kitchen', 'Experiment Room', 'Hangar', 'Dining Room']

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
               str(self._currentRoom)
    def getName(self):
        """Returns a string representation of the character's name."""
        return str(self._name)
    def setCurrentRoom(self, room):
        """Sets the character's current room"""
        self._currentRoom = room
    def changeRoom(self, room):
        self._currentRoom.removeOccupant(self)
        room.acceptChar(self)
        setCurrentRoom(room)
        
                
class room(object):
    """Represents the basic outline of a room."""
    def __init__(self, roomName):
        self._name = roomName
        self._occupants = []
    def __str__(self):
        """Returns string representation of the room objects"""
        return "Room: " + self._name + '\n' + "Occupants: " + "\n" \
               + self.occupantNames()
    def getName(self):
        """Adds a character to the room."""
        return self._name
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
            if char == self._occupants[x]:
                return x
        else:
            return char + " is not in the room."
        
        

def assignCharsToRooms(characterList, roomList):
    """Assigns every character to a room."""
    newCharList = []
    for x in range (len(characterList)):
        char = random.choice(characterList)
        room = random.choice(roomList)
        char.setCurrentRoom(room.getName())
        room.acceptChar(char)
        newCharList.append(char)
        characterList.remove(char)
    return newCharList

def createCharObjs(listOfCharacterNames):
    """Creates a list of character objects when given a list of names."""
    charObjects = []
    #Creates characters from information in charNames list
    for x in range(len(listOfCharacterNames)):
        char = person(listOfCharacterNames[x], False)
        charObjects.append(char)
    return charObjects
    
def createRoomObjs(listOfRoomNames):
    """Creates a list of room objects when gien a list of room names."""
    roomObjects = []
    #Creates characters from information in charNames list
    for x in range(len(listOfRoomNames)):
        r = room(listOfRoomNames[x])
        roomObjects.append(r)
    return roomObjects

def main():

    #Creates a list of character and room objects
    charObjs = createCharObjs(charNames)
    roomObjs = createRoomObjs(roomNames)

    #Puts the characters in their rooms.
    permCharList = assignCharsToRooms(charObjs, roomObjs)
    
    #Prints character objects
    for x in range(len(permCharList)):
        print(permCharList[x])
        print()
        
    print("------------------------------------------")
    print()

    #Prints room objects
    for x in range(len(roomObjs)):
        print(roomObjs[x])
        print()

    print("------------------------------------------")
    print()

    index = roomObjs[1].getChar("MacReady")
    roomObjs[1]._occupants[index].changeRoom(roomObj[0])

    #Prints room objects
    for x in range(len(roomObjs)):
        print(roomObjs[x])
        print()

if __name__ == '__main__':
    main()
