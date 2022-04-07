#TangoBots Dialogue Project
class VariableStore:
    
    def __init__(self):
        self.varStore = {}

    def getVar(self, varName):
        return self.varStore[varName]

    def setVar(self, varName, varValue):
        self.varStore[varName] = varValue

    def clear(self):
        self.varStore = {}

"""
(~greetings) [hi hello "what up" sup]    
(you) good
(and) [one two]
(you) Should not be here
(test) two
(third) ~greetings
(my name is _) hello $name
(I am _ years old) You are $age years old
(do you remember my name) Yes
(what is it) $name
(you are very smart) I know
(what is my name) your name is $name     
(how old am I) you are $age
"""

class Rule:

    def __init__(self, inout):
        print(inout)
        strList = inout.split(")")
        self.input = strList[0].strip("(")
        self.output = strList[1]
        inputList = strList[0].split(" ")
        eqList = []
        for i in range(len(inputList)):
            if(inputList[i] == "_"):
                eqList.append(False)
            else:
                eqList.append(True)
        self.compareList = eqList

    def isEqual(self, stmt):
        stmtList = stmt.split(" ")
        inputList = self.input.split(" ")
        for i in range(len(self.compareList)):
            if(self.compareList[i]):
                if(stmtList[i] != inputList[i]):
                    return False
        return True

    def getInput():
        #checks for tilda or $ and replace accordingly
        #return self.input with proper replaced value
        pass 

    def getOutput():
        #checks for tilda or $ and replace accordingly
        #return self.output with proper replaced value
        pass

    def parseList(self):
        pass

    def parsePhrase(self):
        pass 

    def __str__(self):
        return f"Rule inp: {self.input}  out: {self.output}"
    

class Node:
    
    def __init__(self, rul):
        self.rule = rul
        self.children = []

    def __str__(self):
        stringyChildren = [str(item) for item in self.children]
        return f"{str(self.rule)} Children: {str(stringyChildren)}"

    def addChild(self, child):
        self.children.append(child)

def readDialogueFile(filename):
    #reads file
    file = open(filename, 'r')
    tree = []
    variablestore = VariableStore()
    for line in file:
        #Gets rid of tabbed white space and new lines
        line = line.replace("\t", "")
        line = line.replace("\n", "")
        #ignores comments
        if(line[0] == "~"):
            topic = line.split(':')
            topicList = parseList(topic[1])
            variablestore.setVar(topic[0])   
        if(line[0] != '#'):
            line = line.split(":")
            if(line[0] == "u"):
                rul = Rule(line[1])
                topNode = Node(rul)
                tree.append(topNode)
            if(line[0] == "u1"):
                rul = Rule(line[1])
                u1Node = Node(rul)
                topNode.addChild(u1Node)
            if(line[0] == "u2"):
                rul = Rule(line[1])
                u2Node = Node(rul)
                u1Node.addChild(u2Node)
            if(line[0] == "u3"):
                rul = Rule(line[1])
                u3Node = Node(rul)
                u2Node.addChild(u3Node)
    file.close()
    return tree

def parseList(line):
    
    pass

def main():
    tree = readDialogueFile('D:\colli\Downloads\Dialogue.txt')
    inp = ""
    scope = []
    while(inp != 'exit'):
        inp = input().lower()
        for i in scope:
            if(i.rule.isEqual(inp)):
                print(i.rule.output)
        for node in tree:
            if(node.rule.isEqual(inp)):
                print(node.rule.output)
                scope = node.children
    print("Goodbye")
    

main()


"""
#comments are ignored
~greetings: [hello howdy "hi there"]
u:(~greetings) [hi hello "what up" sup]
	u1:(you) good
	u1:(and) [one two]
u:(you) Should not be here
u:(test) two
	u1:(third) ~greetings
u:(my name is _) hello $name
	u1:(i am _ years old) You are $age years old
	u1:(do you remember my name) Yes
	#comments are ignored
		u2:(what is it) $name
			u3:(you are very smart) I know
u:(what is my name) your name is $name
u:(how old am I) you are $age
#u:(this is an error) error here
"""
