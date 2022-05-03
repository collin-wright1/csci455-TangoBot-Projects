"""
Final Project Class. Implements robot actions
This class implements the robot and its possible actions, as well as managing user input
"""
import random

class Robot:

    # TODO: The print statments need to be changed to be output by the speaker and the input needs to be text to speech.
    # TODO: need to add a condition to check if total moves are greater than some amount, if so the game is lost.

    def __init__(self):
        self.health = 80
        self.weapon = "basic sword"
        self.key = False
        self.damage = 5
        self.turns = 0
        self.allowedTurns = 15

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
    def fightChoice(self, enemy, enemyHealth):
        print(f"I am fighting a {enemy}. It has {enemyHealth} health and I have {self.health} health.")
        choice = input("I can attack or retreat\n")
        while choice != "attack" and choice != "retreat":
            choice = input("I can attack or retreat\n")
        return choice

    def retreat(self, map):
        print("inside retreat")
        possMoves = map.getPossibleMoves()
        print(possMoves)
        choice = possMoves[random.randint(0, len(possMoves)-1)]
        print(choice)
        self.move(choice, map)


    def getMovementChoice(self, possMovesArray):
        for i in possMovesArray:
            print("I can move {}".format(i))
        choice = input("Where should I go?\n")
        while choice not in possMovesArray:
            choice = input("I can't move there. Try a different movement.\n") # TODO: might not be working correctly
        return choice

    def takeDamage(self, damage):
        self.health -= damage
    
    def getHealth(self):
        return self.health
    
    def setHealth(self, inhealth):
        self.health = inhealth
    
    def getWeapon(self):
        return self.weapon
    
    def getKey(self):
        return self.key

    def setKey(self, bool):
        self.key = bool

    def getDamage(self):
        return self.damage

    def getTurns(self):
        return self.turns

    def evalTurns(self):
        if self.turns == self.allowedTurns:
            print("You took too long and died of starvation.")
            exit()



    # executes the actual move on the map
    def move(self, choice, robomap):
        # update robot position on map
        if choice == "right":
            print("Moving Right")
            robomap.moveRight()
        elif choice == "left":
            print("Moving Left")
            robomap.moveLeft()
        elif choice == "up":
            print("Moving up")
            robomap.moveUp()
        elif choice == "down":
            print("Moving Down")
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


