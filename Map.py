"""
Final Project Class. Imports the Node class
This class contains the map which the robot will navigate.
"""
from Node import EmptyNode, Node

class Map:

    # TODO: Map coordinates are kinda messed up, I think x and y needs to be reversed.
    def __init__(self):
        self.navMap = [[ Node() for x in range(0,5)] for y in range(0,5)]
        self.navMap[2][0] = EmptyNode() # Adding nodes. Specify the coordinate and then create a node in that position on the navmap.
        self.navMap[2][1] = EmptyNode()
        self.navMap[2][2] = EmptyNode()
        self.navMap[2][3] = EmptyNode()
        self.navMap[2][4] = EmptyNode()
        self.navMap[0][2] = EmptyNode()
        self.navMap[1][2] = EmptyNode()
        self.navMap[3][2] = EmptyNode()
        self.navMap[4][2] = EmptyNode()
        self.robotX = 2
        self.robotY = 0
        # TODO: Randomly set start and end node on accessible node.

    # Tostring for the map printout
    def __str__(self):
        total = ""
        for x in range(0, 5):
            row = "[ "
            for y in range (0, 5):
                row += str(self.navMap[x][y])
            row += " ]\n"   
            total += row
        return total

    def moveRight(self):
        self.robotX += 1

    def moveLeft(self):
        self.robotX -= 1

    def moveUp(self):
        self.robotY += 1
    
    def moveDown(self):
        self.robotY -= 1

    def getRobotPosition(self):
        return self.robotX, self.robotY

    # calls the action of the current robot the robot is in.
    def induceAction(self):
        x = self.robotX
        y = self.robotY
        # TODO: check the type of node and pass in the robot if necessary (when it's a heal, an item, or a fight).
        self.navMap[x][y].performAction()

    # evaluates where the robot can move to.
    def getPossibleMoves(self):
        possMoves = []
        x = self.robotX
        y = self.robotY
        if y + 1 < len(self.navMap):
            if self.navMap[x][y+1].getType() != "wall":
                possMoves.append("up")
        if y - 1 >= 0:
            if self.navMap[x][y-1].getType() != "wall":
                possMoves.append("down")
        if x + 1 < len(self.navMap[x]):
            if self.navMap[x+1][y].getType() != "wall":
                possMoves.append("right")
        if x - 1 >= 0:
            if self.navMap[x-1][y].getType() != "wall":
                possMoves.append("left")
        return possMoves
    
