"""
Final Project Class. Implements the nodes and their affects on the robot.
This class creates the different node types that are stored within the map and defines their interactions with the robot
"""
import random

class Node:

    def __init__(self):
        self.type = "wall"
        self.start = False
        self.end = False
        self.encountered = False

    # TODO: Need to implement a general method to check if the node is the end and if the robot has the key. If so, the game is over.

    def performAction(self, robot):
        pass

    def getType(self):
        return self.type

    def __str__(self):
        return f"[N: {self.type} v: {self.encountered}]"

class EmptyNode(Node):

    def __init__(self):
        self.type = "empty"
        self.encountered = False
        

    def performAction(self, robot):
        if self.encountered == False:
            self.encountered = True
            print("There's nothing here")
        else:
            print("You've already been here")

# TODO: I have not added a fight node to the map so this has not been tested.
class FightNode(Node):
 
    # Name : [Health, Damage]
    enemies = {"goblin" : [15, 5], "orc" : [30, 3], "giant spider" : [10, 2], "dragon" : [40, 10], "elf" : [2, 0]}

    def __init__(self):
        self.type = "fight"
        self.encountered = False
        self.enemy, stats = random.choice(list(self.enemies.items()))
        self.enemyHealth = stats[0]
        self.enemyAttack = stats[1]

    def performAction(self, robot):
        self.encountered = True
        while self.enemyAlive: # If enemy alive
            if robot.getHealth() >= 0: # if robot alive
                choice = robot.fightChoice(self.type)
                if choice == "attack":
                    self.enemyHealth -= robot.getDamage()
                    if self.enemyHealth <= 0:
                        self.enemyKilled()
                    else:
                        self.enemyTurn(robot)
                # TODO: add retreat condition, should have 75% chance of succeeding
            # TODO: add condition where robot is dead (what should we do when the robot is out of health, game over?)
        print(f"The scars of battle remain here, but the {self.enemy} has been long vanquished")
        

    # subtract enemy attack from robot health
    def enemyTurn(self, robot):
        robot.takeDamage(self.enemyAttack)

    # changes node type to empty once enemy is killed
    def enemyKilled(self):
        self.enemyAlive = False
        print("enemy killed")

# TODO: needs to be implemented. Should replace the robots equiped weapon with something better. Select randomly from a list like the enemy node.
# One of these should also have a key. Or we could make it drop from a monster?
class ItemNode(Node):
    pass

# TODO: needs to be implemented. Heals the robot to 200 hp. 
class HealthNode(Node):
    pass
