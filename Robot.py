"""
Final Project Class. Implements robot actions
This class implements the robot and its possible actions, as well as managing user input
"""
import random

class Robot:

    # TODO: The print statments need to be changed to be output by the speaker and the input needs to be text to speech.
    # TODO: need to add a condition to check if total moves are greater than some amount, if so the game is lost.

    def __init__(self):
        self.health = 200
        self.weapon = "basic sword"
        self.key = False
        self.damage = 10
        self.turns = 0

    # prints the selection menu
    def menu(self):
        print("I can scout, rest, sharpen my weapon, or report")
        return input("What should I do? \n")

    
    # This method examines surrounding squares in the map and tells the user which ways are possible
    def scout(self, map):
        return self.getMovementChoice(map.getPossibleMoves())

    # This method rests in the current node and heals a random chunk of hp
    def rest(self):
        heal = random.randrange(3, 20, 3)
        self.health += heal
        self.turns += 1
        print(f"I healed for {heal} hp, bringing my total to {self.health}.\n")
    
    # This method works like rest but improves the current weapon
    def sharpen(self):
        sharp = random.randrange(3, 20, 3)
        self.damage += sharp
        self.turns += 1
        print(f"I sharpened my weapon for {sharp} damage, bringing my total to {self.damage} damage.\n")

    # not implemented yet, might not be necessary
    def fightChoice(self, type):
        if type == "fight":
            return self.ask(["fight", "retreat"])

    def getMovementChoice(self, possMovesArray):
        for i in possMovesArray:
            print("I can move {}".format(i))
        choice = input("Where should I go?\n")
        if choice not in possMovesArray and not "exit":
            choice = input("I can't do move there. Try a different movement.\n ")
        return choice

    def takeDamage(self, damage):
        self.health -= damage
    
    def getHealth(self):
        return self.health
    
    def getWeapon(self):
        return self.weapon
    
    def getKey(self):
        return self.key

    def getDamage(self):
        return self.damage

    def getTurns(self):
        return self.turns


    # executes the actual move on the map
    def move(self, choice, robomap):
        # update robot position on map
        if choice == "right":
            robomap.moveRight()
        elif choice == "left":
            robomap.moveLeft()
        elif choice == "up":
            robomap.moveUp()
        elif choice == "down":
            robomap.moveDown()
        self.turns += 1
        

    # return info on current weapon, health, and whatever else we want to add.
    def report(self, nmap):
        print(f"I am in square {nmap.robotX}, {nmap.robotY}\n")
        print(f"I have {self.health} health\n")
        print(f"I have a {self.weapon} which does {self.damage} damage\n")
        if self.key:
            print(f"I have found the exit key\n")
        else:
            print(f"I have not found the exit key\n")
        print(f"I have used {self.turns} turns\n")
        print()
        print(nmap)


