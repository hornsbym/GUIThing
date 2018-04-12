"""
Written by Mitchell Hornsby
descriptions.py
This file holds all dialogue and descriptions for the game The Thing by Mitchell Hornsby.
"""
openingMessage = """\
The Thing\n\
A Text-Based Adventure by Mitchell Hornsby\n\
\n\
You play as MacReady, an antarctic researcher locked underground with the rest of his team. Some of them have been infected by an alien parasite known as "The Thing", which looks and acts exactly like its host. Armed only with a flamethrower, your \
goal is to identify and kill every infected researcher, then escape. Or, simply kill everyone else in the base without losing your own life.The camp's chief scientist, Blair, has locked himself away from the others and will help you identify infected \
crew members.\n\
\n\
The outside world will not believe the events that transpire within the base. Even if you manage to escape with your life, you and Blair will need at least one other witness to avoid a life in prison. However, if the Thing manages to escape \
the base, its shape-shifting abilities and hunger for flesh will certainly drive the rest of the world to extinction. \n\
\n\
What will you do? Escape with your life, or save the world? The fate of humanity will be decided by your actions here."""

creditMessage = """\
Credits:\n\
\n\
Writing, programming and game design by Mitchell Hornsby\n\
\n\
Game based on the short story "Who Goes There?" by John Campbell and the 1983 movie "The Thing" by John Carpenter.\n\
\n\
Special thanks my willing guinea pigs, Mandie Wahlers and Carter Huffman.\n\
"""
 

roomDict = {"Blair's Room":"You are in a narrow room dug out of the ice. It is dimly lit; one lamp sits in the center of the room, casting a weak blue light over everything. There is a door, chained shut, along the far wall. Approaching the door, \
you see there is a small opening to look through. Inside, you find a short, pudgy man huddled in front of a computer screen. Blair. From here, you can reach the experiment room and dining room.","Dining Room":"You find yourself in a large, warm room. \
A small generator hums in the corner; beside it sits an electric heater. A long table sits in the center of the room. Its chairs are turned the wrong way and lined up in rows. Clearly, there has been an important meeting here recently. From here, you \
can get to the kitchen, hangar, experiment room, thawing room, and Blair's room","Kitchen":"The make-shift space barely qualifies as a kitchen. It is dark, cold and dirty. Dirty plates are scattered piled on one of the wooden counters, and the remains \
of last night's meal lay decaying on the carving table. The smell is almost too much to bear. From here, you can go to the dining room or the thawing room.",'Experiment Room':"The experiment is the brightest room on base. There is a long metal table \
in the center of the room, flanked on either side by loud, buzzing machinery. In the corner of the room sits a blood-stained wooden stool. There are claw marks intermittenly dispersed along the icy walls... Someone fought for their life here. From \
here, you can get to Blair's room and the dining room.",'Hangar':"It is the largest room on the base, and only half buried in the ice. One side of the hangar connects to the base, the other leads outside through large bay doors. The bay doors won't be \
able to open until next spring. Two planes, a helicopter, and six snow mobiles are stored here. From here, you can reach the dog room or the dining room.","Foyer":"The foyer is the only room that leads outside during the winter. It is a small room \
with a heavy metal door and a coat rack. A little light streams in through a window in the door. There's a soft whistle as wind batters the drafty door. From here, you can get to the thawing room.","Dog Room":"More of a corridor than a room, the dog \
room is flanked by kennels on each side. At one point, there had been about twelve dogs to pull the sleds. Now, there's just spatterings of blood on the walls and a broken chain-link fences. From here, you can reach the security room or the hangar.\
","Thawing Room":"The thawing room resembles a meat locker more than it does a room. Entire sides of cattle are suspended from the ceiling, thawing so they can be cooked. Before, you knew you were just standing in cow's blood. Now, you're not so sure. \
From here, you can head to the dining room, kitchen, foyer or hangar.","Security Room":"The security room housed all the weapons on base, along with the computer and radio equipment. However, the weapons have all disappeared and the equipment has been smashed. \
From here, you can get to the dog room."}

quitMessages = ["MacReady has had enough. In a fit of exasperation, he turns the flamethrower on himself...", "MacReady heard the shuffle of feet behind him. He quickly turns around, but slips on the icy floor, hitting his head. Before he blacks out, \
he witnesses a large, dark shadow loom over him...","MacReady suddenly feels very sick. He doubles over in pain, struggling to breathe. He collapses as a long, fleshy tendril bursts from his back..."]

deathMessages = ["The Thing attacks when MacReady's back is turned! MacReady hears a loud shriek, and whirls around, already blasting his flamethrower. But he's too late, as he's tackeled to the ground. The Thing pins him down and devours him.","MacRe\
ady hears a loud bang and turns to the left. A barrel had fallen over for no obvious reason. Suspecting what was truly going on, MacReady fires up his flamethrower whips around to the other in the room. He's too late.","MacReady hears a low growl from \
around the corner. One of the sled dogs slinks around the corner, his head low and tail straight, growling. MacReady ignites his flamethrower, but he feels a sharp pain in his lower legs. He finds that the other sled dogs somehow snuck behind him, \
immobilizing him. He sinks to one knee, screaming as the Thing sets upon him."]

dialogue = ['''"What's up, Mac?"''', '''"Hey, Mac."''', '''"What's up, MacReady?"''', '''"What's the weather looking like, Mac?"''','''"Any leads, MacReady?"''','''"Any leads, Mac?"''','''"Hey, MacReady."''','''"What's the weather looking like, \
MacReady?"''', '''"How you holdin' up, Mac?"''','''"How you holdin' up, MacReady?"''']

baseMap = "\
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n\
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n\
XXXXXXXXXXXXXXXXXXXXXX           XXXXXXXXX           XXXXXXXXXXX           XXX\n\
XXXXXXXXXXXXXXXXXXXXXX           XXXXXXXXX           XXXXXXXXXXX           XXX\n\
XXXXXXXXXXXXXXXXXXXXXX  Hangar               Dog                 Security  XXX\n\
XXXXXXXXXXXXXXXXXXXXXX           XXXXXXXXX   Room    XXXXXXXXXXX   Room    XXX\n\
XXXXXXXXXXXXXXXXXXXXXX              XXXXXX           XXXXXXXXXXX           XXX\n\
XXX          XXXXXXXXX           XX  XXXXX           XXXXXXXXXXX           XXX\n\
XXX          XXXXXXXXXXXXX  XXXXXXXX  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n\
XXX  Blair's XXXXXXXXXXXXX  XXXXXXXXX  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n\
XXX   Room       XXXXXXXXX  XXXXXXXXXX      XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n\
XXX          XXX  XXXXXXXX  XXXXXXXXXXXXXX   XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n\
XXX          XXXX  XXXXXXX  XXXXXXXXXXXXXXX  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n\
XXXXXXX  XXXXXXXXX              XXXXXXXXXX           XXXXXXXXXXXXXXXXXXXXXXXXX\n\
XXXXXXX  XXXXXXXXXXXXX          XXXXXXXXXX           XXXXXXXXXXXXXXXXXXXXXXXXX\n\
XXXXXXX  XXXXXXXXXXXXX  Dining              Thawing              XXXXXXXXXXXXX\n\
XXXXXXX  XXXXXXXXXXXXX   Room   XXXXXXXXXX    Room   XXXXXXXXXX    XXXXXXXXXXX\n\
XXXXXXX  XXXXXXXXXX             XXXXXXXXXX           XXXXXXXXXXXX   XXXXXXXXXX\n\
XXX          XXXXX  XX          XXXXXXXXXX           XXXXXXXXXXXXX  XXXXXXXXXX\n\
XXX          XXXX  XXXXXXX  XXXXXXXXXXXXXXXX  XXXXXXXXXXXXXXXXXXX          XXX\n\
XXX Experim. XXX  XXXXXXXX  XXXXXXXXXXXXXXX  XXXXXXXXXXXXXXXXXXXX          XXX\n\
XXX   Room       XXXXXXXXX  XXXXXXXXXXXXXX  XXXXXXXXXXXXXXXXXXXXX  Foyer   XXX\n\
XXX          XXXXXXXXXXXXX  XXXXXXXX       XXXXXXXXXXXXXXXXXXXXXX          XXX\n\
XXX          XXXXXXXXXXXXX  XXXXXXX  XXXXXXXXXXXXXXXXXXXXXXXXXXXX          XXX\n\
XXXXXXXXXXXXXXXXXXXXXX          XX  XXXXXXXXXXXXXXXXXXXXXXXXXXXXX [LOCKED] XXX\n\
XXXXXXXXXXXXXXXXXXXXXX             XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  XXXXXXX\n\
XXXXXXXXXXXXXXXXXXXXXX Kitchen  XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  XXXXXXX\n\
XXXXXXXXXXXXXXXXXXXXXX          XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  XXXXXXX\n\
XXXXXXXXXXXXXXXXXXXXXX          XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  XXXXXXX\n\
XXXXXXXXXXXXXXXXXXXXXX          XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  XXXXXXX\n\
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  XXXXXXX\n\
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  XXXXXXX\n"


