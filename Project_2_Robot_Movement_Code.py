import serial, time, sys
import tkinter as tk
import time
import _thread, threading
import speech_recognition as sr
import random


#class to store gloabl variables
class VariableStore:
    
    #initializes by setting empty dictionary
    def __init__(self):
        self.varStore = {}

    #accesses store to return variable value
    def getVar(self, varName):
        return self.varStore[varName]

    #sets a given variable with a given value to dict
    def setVar(self, varName, varValue):
        self.varStore[varName] = varValue

    #prints out all variable-value pairs stored
    def printVars(self):
        for i in self.varStore:
            print(i, self.varStore[i])

#Class to store a dialogue input/output rule
class Rule:

    #initializes rule by settting input/output values, takes a single line as input for parsing
    def __init__(self, inout):
        inout = inout.strip(" ")
        #splits line by close paren
        strList = inout.split(")")
        #rids of open paren on lhs
        self.input = strList[0].strip("(")
        #isolates the output (rhs) and removes excess spaces
        out = strList[1].strip(": ")
        #handles if output is a list of random choices
        if(out[0] == "["): #puts choice list into proper format
            out = out.strip("[")
            out = out.strip("]")
            outList = out.split()
            out = makeOptionList(outList)
            self.output = out
        elif(out[0] == "~"): #if output contains any stored topic variables, then sets accordingly
            self.output = variableStore.getVar(out)
        else: #otherwise, single outputs are stored
            outList = []
            outList.append(out)
            self.output = outList
        #handles inputs (lhs)
        inputList = strList[0].split(" ")
        #sets up comparison list (list of true/false used to compare inputs with blanks)
        #any wordspace containing a blank is stored as false, which will be ignored in euqlity comparison
        eqList = []
        for i in range(len(inputList)):
            if(inputList[i] == "_"):
                eqList.append(False)
            else:
                eqList.append(True)
        self.compareList = eqList

    #checks equality of a given input, to the input of this rule
    def isEqual(self, stmt):
        stmtList = stmt.split(" ")
        inputList = self.input.split(" ")
        for i in range(len(self.compareList)):
            #ignores any false slots in the comparison list
            if(self.compareList[i]):
                if(stmtList[i] != inputList[i]):
                    #returns false if significant input words are missed
                    return False
        #calls logVar to store the fill-in-the-blank variable words
        self.logVar(stmt)
        return True

    #checks for fill-in-the-blank variables and logs them into global variableStore
    def logVar(self, input):
        stmtList = input.split(" ")
        for i in range(len(self.compareList)):
            #false flag in the compare list indicates that that wordspace contains variable values to store
            if(not self.compareList[i]):
                name = ""
                for j in self.output:
                    outList = j.split(" ")
                    for k in outList:
                        if(k[0] == "$"):
                            name = k
                if(name != ""):
                    variableStore.setVar(name, stmtList[i])

    #returns the correct output according to random choices and stored variables
    def getOutput(self):
        #randomly chooses an output option
        out = self.output[random.randint(0, (len(self.output) - 1))]
        tempList = out.split(" ")
        outList = []
        #if option contains any variables, replaces the output word with the proper stored value
        for i in tempList:
            if(i[0] == "$"):
                if(i in variableStore.varStore):
                    outList.append(variableStore.varStore[i])
                #catches for variables that have not been set
                else:
                    return "UNKNOWN"
            else:
                outList.append(i)
        total = ""
        for i in outList:
            total += i
            total += " "
        total.strip(" ")
        return total

    #allows for printing rules
    def __str__(self):
        return f"Rule inp: {self.input}  out: {self.output}"

#node class to store rules as nested nodes
class Node:
    
    #initialize with given rule, sets an empty list of children (to be filled with any children nodes to create a tree)
    def __init__(self, rul):
        self.rule = rul
        self.children = []

    #allows for printing nodes (includes rule and list of children nodes)
    def __str__(self):
        stringyChildren = [str(item) for item in self.children]
        return f"{str(self.rule)} Children: {str(stringyChildren)}"

    #adds a given node as a child to this node
    def addChild(self, child):
        self.children.append(child)
    
class TangoBot:

    #initializes robot
    def __init__(self):

        self.waist = 6000
        self.headHorz  = 6000
        self.headVert = 6000
        self.motors = 6000
        self.turn = 6000

        self.message = "-1"

        try:
            self.usb = serial.Serial('/dev/ttyACM0')
            print(self.usb.name)
            print(self.usb.baudrate)
        except:
            try:
                self.usb = serial.Serial('/dev/ttyACM1')
                print(self.usb.name)
                print(self.usb.baudrate)
            except:
                print("No servo serial ports found")
                sys.exit(0)

        self.reset()

        #Ports: 0-1 motor controls, 2 waist, 3-4 head, arms after that

    def reset(self):
        self.waist = 6000
        self.headHorz  = 6000
        self.headVert = 6000
        self.motors = 6000
        self.turn = 6000
        self.makeCommand(self.headHorz, 0x03)
        self.makeCommand(self.headVert, 0x04)
        self.makeCommand(self.waist, 0x02)
        self.makeCommand(self.motors, 0x00)
        self.makeCommand(self.turn, 0x01)

    def moveReverse(self):
        if(self.motors < 7500):
            self.motors += 500
            self.makeCommand(self.motors, 0x00)
            print("moving reverse")
        else:
            print("max speed")

    def moveForward(self):
        if(self.motors > 4500):
            self.motors -= 500
            self.makeCommand(self.motors, 0x00)
            print("moving forward")
        else:
            print("max speed")

    def turnLeft(self):
        print('turning left')
#        self.motors = 6000
#        self.makeCommand(self.motors, 0x00)
        self.turn += 1300
        self.makeCommand(self.turn, 0x01)
        self.turn = 6000
#        time.sleep(1)
#        for i in range(3):
#            self.moveReverse(key)
#        for i in range(3):
#            self.moveForward(key)

    def turnRight(self):
        print('turning right')
#        self.motors = 6000
#        self.makeCommand(self.motors, 0x00)
        self.turn -= 1300
        self.makeCommand(self.turn, 0x01)
        self.turn = 6000
#        for i in range(3):
#            self.moveReverse(key)
#        for i in range(3):
#            self.moveForward(key)

    def stop(self):
        print("stopping")
        if(self.motors > 6000):
            while(self.motors > 6000):
                self.motors -= 250
                self.makeCommand(self.motors, 0x00)
        elif(self.motors < 6000):
            while(self.motors < 6000):
                self.motors += 250
                self.makeCommand(self.motors, 0x00)

    def moveWaistLeft(self):
        if(self.waist < 9000):
            self.waist += 500
            self.makeCommand(self.waist, 0x02)
            print("swiveling left")
        else:
            print("max swivel")

    def moveWaistRight(self):
        if(self.waist > 3000):
            self.waist -= 500
            self.makeCommand(self.waist, 0x02)
            print("swiveling right")
        else:
            print("max swivel")

    def moveHeadRight(self):
        if(self.headHorz > 5000):
            print("move head right")
            self.headHorz -= 500
            self.makeCommand(self.headHorz, 0x03)
        else:
            print("head too far right")

    def moveHeadLeft(self):
        if(self.headHorz < 7000):
            print("move head left")
            self.headHorz += 500
            self.makeCommand(self.headHorz, 0x03)
        else:
            print("head too far left")

    def moveHeadUp(self):
        if(self.headVert < 7000):
            print("move head up")
            self.headVert += 500
            self.makeCommand(self.headVert, 0x04)
        else:
            print("head too high")

    def moveHeadDown(self):
        if(self.headVert > 5000):
            print("move head down")
            self.headVert -= 500
            self.makeCommand(self.headVert, 0x04)
        else:
            print("head too low")

    def makeCommand(self, target, port):
        lsb = target &0x7F
        msb = (target >> 7) &0x7F
        cmd = chr(0xaa) + chr(0xC) + chr(0x04) + chr(port) + chr(lsb) + chr(msb)
        self.execute(cmd)

    def execute(self, cmd):
        print('Writing')
        self.usb.write(cmd.encode())
        print('Reading')

    def voiceController(self):
        #read in dialogue file
        tree = readDialogueFile('/home/pi/csci455-TangoBot-Projects/demo.txt')
        #set variables as default
        inp = ""
        scope = []
        while "exit" not in self.message:
            if "stop" in self.message:
                self.stop()
                self.message = "-1"
            elif "forward" in self.message:
                self.moveForward()
                self.message = "-1"
            elif "reverse" in self.message:
                self.moveReverse()
                self.message = "1"
            elif "turn left" in self.message:
                self.turnLeft()
                self.message = "-1"
            elif "turn right" in self.message:
                self.turnRight()
                self.message = "-1"
            elif "look up" in self.message:
                self.moveHeadUp()
                self.message = "-1"
            elif "look down" in self.message:
                self.moveHeadDown()
                self.message = "-1"
            elif "look left" in self.message:
                self.moveHeadLeft()
                self.message = "-1"
            elif "look right" in self.message:
                self.moveHeadRight()
                self.message = "-1"
            elif "rotate left" in self.message:
                self.moveWaistLeft()
                self.message = "-1"
            elif "rotate right" in self.message:
                self.moveWaistRight()
                self.message = "-1"
            else:
                flag = True
                #take in user input as lowercase string
                inp = self.message
                #debugging feature prints all variables in store
                if(inp == 'print variables'):
                    variableStore.printVars()
                #checks if input belongs to a stored topic variable list, if so convert input to generalized topic name
                for i in variableStore.varStore:
                    if(inp in variableStore.varStore[i]):
                        inp = i
                #checks current node scope for matching inputs of rules
                for i in scope:
                    rul = i.rule
                    #if there's a match, print the appropriate output
                    if(rul.isEqual(inp)):
                        print(rul.getOutput())
                        if(i.children != []):
                            scope = i.children
                        flag = False
                #otherwise, checks the outermost level ('u' rules) for matching input
                if(flag):
                    for node in tree:
                        rul = node.rule
                        #if there's a match, print the appropriate output
                        if(rul.isEqual(inp)):
                            print(node.rule.getOutput())
                            scope = node.children
                self.message = "-1

    def voiceInput(self):
        listening = True
        while listening:
            with sr.Microphone() as source:
                r = sr.Recognizer()
                r.adjust_for_ambient_noise(source)
                r.dynamic_energythreshhold = 3000

                try:
                    print("Listening")
                    audio = r.listen(source)
                    print("Got Audio")
                    self.message = r.recognize_google(audio)
                    print(self.message)
                except sr.UnknownValueError:
                    print("Unknown Word")

    def mainThread(self):
        i = 0
        while i != -1:
            if i % 10 == 0:
                print(str(i))
            i += 1

#implements keyboard input
class KeyController:

    def __init__(self, robo):

        self.robot = robo

        win = tk.Tk()

        win.bind('<Up>', self.arrows)
        win.bind('<Left>', self.arrows)
        win.bind('<Down>', self.arrows)
        win.bind('<Right>', self.arrows)
        win.bind('<space>', self.arrows)
        win.bind('<z>', self.waist)
        win.bind('<c>', self.waist)
        win.bind('<w>', self.head)
        win.bind('<a>', self.head)
        win.bind('<s>', self.head)
        win.bind('<d>', self.head)
        win.mainloop()

    def arrows(self, key):
        print(key.keycode)
        if(key.keycode == 111):
            self.robot.moveForward(key)
        elif(key.keycode == 116):
            self.robot.moveReverse(key)
        elif(key.keycode == 113):
            self.robot.turnLeft(key)
        elif(key.keycode == 114):
            self.robot.turnRight(key)
        elif(key.keycode == 65):
            self.robot.stop(key)

    def waist(self, key):
        print(key.keycode)
        if(key.keycode == 52):
            self.robot.moveWaistLeft(key)
        elif(key.keycode == 54):
            self.robot.moveWaistRight(key)

    def head(self, key):
        print(key.keycode)
        if(key.keycode == 25):
            self.robot.moveHeadUp(key)
        elif(key.keycode == 38):
            self.robot.moveHeadLeft(key)
        elif(key.keycode == 39):
            self.robot.moveHeadDown(key)
        elif(key.keycode == 40):
            self.robot.moveHeadRight(key)

#reads a given dialogue file and converts into a tree of nodes contianing nested rules
def readDialogueFile(filename):
    #reads file
    file = open(filename, 'r')
    tree = []
    nodeStack = []
    counter = 0
    uN = "u" + str(counter)
    for line in file:
        #Gets rid of white space and new lines
        line = line.replace("\t", "")
        line = line.replace("\n", "")
        line = line.strip(" ")
        #stores topic variable lists in global variable store
        if(line[0] == "~"):
            topic = line.split(':')
            if(topic[1][1] == '['):
                topicList = parseList(topic[1])
                variableStore.setVar(topic[0], topicList)
            else:
                variableStore.setVar(topic[0], topic[1])
        #ignores comments
        elif(line[0] != '#'):
            #catches errors in file formatting
            if(line.count(":") == 2 and '(' in line and ')' in line):
                line = line.split(":", 1)
                #makes a tree of indefinite size
                if(line[0] == "u"):
                    rul = Rule(line[1].lower())
                    topNode = Node(rul)
                    tree.append(topNode)
                    nodeStack = []
                    nodeStack.append(topNode)
                    counter = 1
                    uN = "u" + str(counter)
                else:
                    while(uN != "u0"):
                        if(line[0] == uN):
                            rul = Rule(line[1].lower())
                            node = Node(rul)
                            nodeStack[-1].addChild(node)
                            nodeStack.append(node)
                            counter += 1
                            uN = "u" + str(counter)
                            break
                        else:
                            nodeStack.pop(-1)
                            counter -= 1
                            uN = "u" + str(counter)
            else:
                print("Error in Dialogue rules... Ignored")
    file.close()
    return tree

#function to make a given line into a list of random options
#solely used for formating
def makeOptionList(line):
    rlist = []
    quote = []
    for word in line:
        if(quote == []):
            if(word[0] == "\""):
                noQuoteWord = word.strip("\"")
                quote.append(noQuoteWord)
            else:
                rlist.append(word)
        else:
            if(word[-1] == "\""):
                noQuoteWord = word.strip("\"")
                quote.append(noQuoteWord)
                total = ""
                for i in quote:
                    total += i
                    total += " "
                total = total.strip(" ")
                rlist.append(total)
                quote = []
            else:
                quote.append(word)
    return rlist

#parses a given list from document
def parseList(line):
    # getting rid of opening and closing brace
    line = line.strip(" ")
    line = line.strip("[")
    line = line.strip("]")
    line = line.split(" ")
    rlist = makeOptionList(line)
    return rlist



#global variable store
variableStore = VariableStore()
            
def main():
    robot = TangoBot()
    try:
        print("Starting Thread")
        _thread.start_new_thread(robot.voiceInput,())
    except:
        print("Error: unable to start thread")
    robot.voiceController()
    #kc = KeyController(robot)

main()


"""
def main():
    #read in dialogue file
    tree = readDialogueFile('/home/pi/csci455-TangoBot-Projects/demo.txt')
    #set variables as default
    inp = ""
    scope = []
    #loop through user inputs until input is "exit"
    while(inp != 'exit'):
        flag = True
        #take in user input as lowercase string
        inp = input().lower()
        #debugging feature prints all variables in store
        if(inp == 'print variables'):
            variableStore.printVars()
        #checks if input belongs to a stored topic variable list, if so convert input to generalized topic name
        for i in variableStore.varStore:
            if(inp in variableStore.varStore[i]):
                inp = i
        #checks current node scope for matching inputs of rules
        for i in scope:
            rul = i.rule
            #if there's a match, print the appropriate output
            if(rul.isEqual(inp)):
                print(rul.getOutput())
                if(i.children != []):
                    scope = i.children
                flag = False
        #otherwise, checks the outermost level ('u' rules) for matching input
        if(flag):
            for node in tree:
                rul = node.rule
                #if there's a match, print the appropriate output
                if(rul.isEqual(inp)):
                    print(node.rule.getOutput())
                    scope = node.children
    print("Goodbye")

#calls main
main()
"""
