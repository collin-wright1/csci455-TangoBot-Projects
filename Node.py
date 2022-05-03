"""
Final Project Class. Implements the nodes and their affects on the robot.
This class creates the different node types that are stored within the map and defines their interactions with the robot
"""
import random
import time

class Node:
    start = False
    end = False

    def __init__(self):
        self.type = "wall"
        self.encountered = False

    # TODO: Need to implement a general method to check if the node is the end and if the robot has the key. If so, the game is over.

    def performAction(self, map, robot):
        pass

    def getType(self):
        return self.type

    def __str__(self):
        return f"[N: {self.type} v: {self.encountered}]"

    def getEnd(self):
        return self.end

    def setEnd(self, bool):
        self.end = bool

    def setStart(self, bool):
        self.start = bool

    def getStart(self):
        return self.start

    def checkEnd(self, robot):
        if self.end and robot.getKey():
            print("You won!")
            exit()
        elif self.end:
            print("This is the exit, but I don't have a key")

class EmptyNode(Node):

    def __init__(self):
        self.type = "empty"
        self.encountered = False
        

    def performAction(self, map, robot):
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
        self.enemyAlive = True

    def performAction(self, map, robot):
        self.encountered = True
        if self.enemyAlive:
            while self.enemyAlive: # If enemy alive
                if robot.getHealth() > 0: # if robot alive
                    choice = robot.fightChoice(self.enemy, self.enemyHealth)
                    if choice == "attack":
                        print("ATTACK!!!!")
                        robot.bot.moveArmUp()
                        time.sleep(1)
                        robot.bot.pinch()
                        time.sleep(1)
                        robot.bot.moveArmDown()
                        self.enemyHealth -= robot.getDamage()
                        if self.enemyHealth <= 0:
                            self.enemyKilled()
                        else:
                            self.enemyTurn(robot)
                    elif choice == "retreat": # TODO: Add retreat condition
                        print("Attempting retreat\n")
                        if random.random() <= 0.75:
                            print("Retreat Successful")
                            robot.retreat(map)
                            break
                        else:
                            print("Could not escape")
                            self.enemyTurn(robot)
                else:
                    print("You have been killed")
                    print("Game Over")
                    robot.bot.moveHeadDown()
                    time.sleep(1)
                    robot.bot.moveHeadDown()
                    time.sleep(1)
                    robot.bot.moveHeadDown()
                    time.sleep(1)
                    robot.bot.moveHeadDown()
                    time.sleep(1)
                    robot.bot.moveHeadDown()
                    exit()
        else:
            print(f"The scars of battle remain here, but the {self.enemy} has been long vanquished")
        

    # subtract enemy attack from robot health
    def enemyTurn(self, robot):
        robot.takeDamage(self.enemyAttack)
        robot.bot.moveWaistLeft()
        print("OUCH! Damage Taken")
        time.sleep(1)
        robot.bot.moveWaistRight()

    # changes node type to empty once enemy is killed
    def enemyKilled(self):
        self.enemyAlive = False
        print("enemy killed")

# TODO: needs to be implemented. Should replace the robots equiped weapon with something better. Select randomly from a list like the enemy node.
# One of these should also have a key. Or we could make it drop from a monster?
class ItemNode(Node):

    def __init__(self):
        self.type = "item"
        self.encountered = False
        

    def performAction(self, map, robot):
        if self.encountered == False:
            self.encountered = True
            print("I found a key!")
            robot.setKey(True)
        else:
            print("You've already been here")

# Heals robot to full health one time. 
class HealthNode(Node):
    
    def __init__(self):
        self.type = "health"
        self.encountered = False
        

    def performAction(self, map, robot):
        if self.encountered == False:
            self.encountered = True
            if robot.getHealth() < 80:
                print("Found a health node. Health restored to 80")
                robot.setHealth(80)
        else:
            print("You've already been here")
