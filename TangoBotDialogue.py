#TangoBots Dialogue Project

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

#main function
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
