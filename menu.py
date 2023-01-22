import rotaryio
import board
import keypad
import busio
import time
import adafruit_character_lcd.character_lcd_i2c as character_lcd

i2c = busio.I2C(board.GP1, board.GP0)

cols = 16
rows = 2
lcd = character_lcd.Character_LCD_I2C(i2c, cols, rows)
lcd.message = "Hello\nCircuitPython"
time.sleep(2)

encoder = rotaryio.IncrementalEncoder(board.GP10, board.GP11)

lastPosition = None

class Options:
    def __init__(self, options: list):
        self.options = []
        for option in options:
            if(isinstance(option,tuple)):
                self.options.append({"title":option[0], "value":option[1]})
            elif(isinstance(option,str)):
                self.options.append({"title":option, "value":option.lower().replace(" ", "_")})              

class Selection:
    def __init__(self, title:str, options, name:str=None,value=None):
        self.optionIdx = 0
        self.title = title
        if name:
            self.name = name
        else:
            self.name = self.title.lower().replace(" ", "_")
        
        if(isinstance(options,Options)):
            self.options = options.options
            if value is not None:
                self.value = value
            else:
                self.value = self.options[0]["value"]
        elif(isinstance(options,range)):
            self.options = list(options)
            if value is not None:
                self.value = value
                self.optionIdx = self.options.index(value)
            else:
                self.value = self.options[0]
    
    def getValue(self):
        return self.value

    def setValue(self,value):
        self.value = value
    
    def setCurrentOption(self):
        if(isinstance(self.options[0],int)):      
            self.value = self.options[self.optionIdx]
        else:
            self.value = self.options[self.optionIdx]["value"]

    def nextOption(self):
        self.optionIdx = self.optionIdx +1
        if(self.optionIdx >= len(self.options)):
            self.optionIdx = 0 
        self.setCurrentOption()

    def prevOption(self):
        self.optionIdx = self.optionIdx -1                
        if(self.optionIdx < 0):
            self.optionIdx = len(self.options) -1
        self.setCurrentOption()
    
    def getCurrentOption(self):
        return self.options[self.optionIdx]
    
    def getCurrentValueTitle(self):
        if(isinstance(self.options[0],int)):    
            return self.value
        else:
            filteredList = list(filter(lambda val: val["value"]==self.value,self.options))
            return filteredList[0]["title"]


  
class SubMenu:
    def __init__(self,title:str,name:str=None):
        self.title = title
        self.selections = {}
        self.selectionIdx = 0

        if name:
            self.name = name
        else:
            self.name =self.title.lower().replace(" ","_")
    
    def addSelection(self,selection:Selection):
        if selection.name in self.selections:
            raise Exception("Name must be unique.")
        self.selections[selection.name] = selection

    def getCurrentSelection(self):
        return self.selections[list(self.selections.keys())[self.selectionIdx]]

    def nextSelection(self):
        self.selectionIdx = self.selectionIdx +1
        if(self.selectionIdx >= len(self.selections)):
            self.selectionIdx = 0 

    def prevSelection(self):
        self.selectionIdx = self.selectionIdx -1                
        if(self.selectionIdx < 0):
            self.selectionIdx = len(self.selections) -1



class Menu:
    def __init__(self):
        self.submenus = {}
        self.submenuIdx = 0
        self.menuDepth = 0

    def addSubMenu(self, submenu:SubMenu):
        if submenu.name in self.submenus:
            raise Exception("Name must be unique.")
        self.submenus[submenu.name] = submenu

    def getCurrentSubMenu(self):
        return self.submenus[list(self.submenus.keys())[self.submenuIdx]]

    def nextSubMenu(self):
        self.submenuIdx = self.submenuIdx +1
        if(self.submenuIdx >= len(self.submenus)):
            self.submenuIdx = 0 
        self.getCurrentSubMenu().selectionIdx = 0

    def prevSubMenu(self):
        self.submenuIdx = self.submenuIdx -1                
        if(self.submenuIdx < 0):
            self.submenuIdx = len(self.submenus) -1
        self.getCurrentSubMenu().selectionIdx = 0

    def nextSelection(self):
        self.getCurrentSubMenu().nextSelection()

    def prevSelection(self):
        self.getCurrentSubMenu().prevSelection()


    def nextOption(self):
        self.getCurrentSubMenu().getCurrentSelection().nextOption()

    def prevOption(self):
        self.getCurrentSubMenu().getCurrentSelection().prevOption()

    def addSelectionToCurrent(self,selection:Selection):
        self.getCurrentSubMenu().addSelection(selection)

    def getCurrentSubmenuTitle(self):
        return self.getCurrentSubMenu().title

    def getCurrentSelectionTitle(self):
        return self.getCurrentSubMenu().getCurrentSelection().title

    def getCurrentOptionTitle(self):
        return self.getCurrentSubMenu().getCurrentSelection().getCurrentValueTitle()

    def getSubmenuSelectionValue(self, submenuName, selectionName):
        return self.submenus[submenuName].selections[selectionName].getCurrentValueTitle()
    
    def increaseDepth(self):
        self.menuDepth = self.menuDepth +1
        if self.menuDepth > 2:
            self.menuDepth = 0


   
menu = Menu()
# Init submenus

menu.addSubMenu(SubMenu("Channel 1",name='channel_1'))
menu.addSubMenu(SubMenu("Channel 2",name='channel_2'))
menu.addSubMenu(SubMenu("Channel 3",name='channel_3'))

# Add options
for i in range(3):
    menu.nextSubMenu()
    menu.addSelectionToCurrent(Selection("Type",Options(["Sine","Square","Triangle"]),'type'))
    menu.addSelectionToCurrent(Selection("Transpose",range(-12,12,1),value=0,name="trans"))


KEY_PINS = (
    board.GP28,
)

keys = keypad.Keys(KEY_PINS, value_when_pressed=False, pull=True)
printValue = True

while True:
    keyEvent = keys.events.get()
    position = encoder.position

    if keyEvent:
        if keyEvent.pressed:
            menu.increaseDepth()
            printValue = True

    if lastPosition is not None and position != lastPosition:        
        printValue = True
        if menu.menuDepth == 0:
            if position > lastPosition:
                menu.nextSubMenu()
            else:
                menu.prevSubMenu()
        elif menu.menuDepth == 1:
            if position > lastPosition:
                menu.nextSelection()
            else:
                menu.prevSelection()  
        elif menu.menuDepth == 2:
            if position > lastPosition:
                menu.nextOption()
            else:
                menu.prevOption() 
    if printValue:
        lcd.clear()
        printValue = False
        if menu.menuDepth == 0:
            lcd.message = '{subMenu}'.format(subMenu = menu.getCurrentSubmenuTitle())
        else:
            lcd.message ='{subMenu} > {selection}\n{option}'.format(subMenu = menu.getCurrentSubmenuTitle(), selection = menu.getCurrentSelectionTitle(),option= menu.getCurrentOptionTitle())
            
    lastPosition = position


"""
channel = SubMenu("Channel 1")
channel.addSelection(Selection("Type",Options(["Sine","Square","Triangle"])))
channel.addSelection(Selection("Transpose",range(-12,12,1),value=0))

channel.nextSelection()
channel.nextSelection()
channel.nextSelection()
channel.nextSelection()

print(channel.title)
print(channel.getCurrentSelection().title)
print(channel.getCurrentSelection().getCurrentValueTitle())

channel.getCurrentSelection().nextOption()
channel.getCurrentSelection().setCurrentOption()
print(channel.getCurrentSelection().getCurrentValueTitle())

channel.getCurrentSelection().nextOption()
channel.getCurrentSelection().setCurrentOption()

print(channel.getCurrentSelection().getCurrentValueTitle())

channel.getCurrentSelection().nextOption()
channel.getCurrentSelection().setCurrentOption()
print(channel.getCurrentSelection().getCurrentValueTitle())



channel.getCurrentSelection().prevOption()
channel.getCurrentSelection().setCurrentOption()
print(channel.getCurrentSelection().getCurrentValueTitle())

channel.getCurrentSelection().prevOption()
channel.getCurrentSelection().setCurrentOption()

print(channel.getCurrentSelection().getCurrentValueTitle())

channel.getCurrentSelection().prevOption()
channel.getCurrentSelection().setCurrentOption()
print(channel.getCurrentSelection().getCurrentValueTitle())

channel.getCurrentSelection().prevOption()
channel.getCurrentSelection().setCurrentOption()
print(channel.getCurrentSelection().getCurrentValueTitle())







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
"""