import rotaryio
import board
import keypad

encoder = rotaryio.IncrementalEncoder(board.GP10, board.GP11)
lastPosition = None

menu = {"channels":[]}
types = [{"title":"Sine", "value":"sine"},
         {"title":"Square", "value":"square"},
         {"title":"Triangle", "value":"triangle"},]

menuIdx = list(menu.keys())[0]
for i in range(8): 
    channel = {}
    channel["selections"] = [{"title": "Type", "name":"type", "values":types, "value":types[0]},
                             {"title": "Transpose", "name":"transpose", "values":range(-12,12,1), "value":0}]
    channel["title"] = "Channel " + str(i+1)
    channel["code"] = "channel"+str(i+1)     
                          
    menu["channels"].append(channel)

submenuIdx = 0
selectionIdx = 0
valueIdx = 0

# skip level 0 for now
menuDepth = 1


KEY_PINS = (
    board.GP28,
)

keys = keypad.Keys(KEY_PINS, value_when_pressed=False, pull=True)


#1 Channel, Other settings (sampling rate)
# 2 Channel 1
#  3 Type
#   4 Sine
#   4 Saw
#   4 ..
#  3 Transpose
#   4 -12
#   4 .. 
#   4 12
# 2 Other setting 
#  3 Rate 
#   4 32000
#   4 44000

while True:
    event = keys.events.get()
    position = encoder.position
    
    if event:
        if event.pressed:
            menuDepth = menuDepth +1
            if menuDepth > 3:
                channel = menu[menuIdx][submenuIdx]
                print(channel)
                menuDepth = 1
    if lastPosition is None or position != lastPosition:
        if menuDepth == 1:
            submenuIdx = position%len(menu[menuIdx])
            channel = menu[menuIdx][submenuIdx]
            print(channel["title"])
        if menuDepth == 2:
            selectionIdx = position%len(menu[menuIdx][submenuIdx]["selections"])
            selection = menu[menuIdx][submenuIdx]["selections"][selectionIdx]
            print(channel["title"] +"> "+selection["title"])
        if menuDepth == 3:
            valueIdx = position%len(menu[menuIdx][submenuIdx]["selections"][selectionIdx]["values"])
            value = menu[menuIdx][submenuIdx]["selections"][selectionIdx]["values"][valueIdx]
            if (isinstance(value,int)):
                selection["value"] = value      
                print(channel["title"] + "> " + selection["title"] +"> " +str(value))              
            else:
                selection["value"] = value["value"]
                print(channel["title"] + "> " + selection["title"] +"> " +value["title"])

    lastPosition = position