"""
Mitchell Hornsby
test.py
The sole purpose of this file is to hold test cases for theThing.py
"""

    
    print("---------(Setting up game)---------")
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
    print("----------(Kills a couple characters)---------")
    g.findCharObj("Fuches").kill()
    g.findCharObj("Windows").kill()
    g.findCharObj("Childs").kill()
    print("----------(Status before randomize)-----------")
    g.showRooms()
    print("----------(Randomize)---------")
    g.randomize()
    print("----------(Status after randomize)-----------")
    g.showRooms()
    print("----------(Infects a character)---------")
    print(g.findCharObj('Childs'))
    print()
    g.infect("Childs")
    print(g.findCharObj('Childs'))
    print("----------(Find the player)----------")
    g.showPlayer()
    print("----------(Things Attack)----------")
    testTurn = 1
    while g.checkPlayer() == True:        
        g.thingsAttack()
        g.randomize()
        print("Turn " + "%2s" % (str(testTurn)) + ": " + str(g.getInfectedCount()) + " infected.")
        testTurn += 1
    print("___________")
    print(testTurn)
    print(g.checkPlayer())
    print('----------(Fix Char Name Func)---------')
    childs = fixCharName('ChIlDs')
    print(childs)
    fuches = fixCharName("fuches")
    print(fuches)
    vanwall = fixCharName("VanWall")
    print(vanwall)
