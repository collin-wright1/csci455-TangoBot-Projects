from Robot import Robot
from Map import Map

if __name__ == "__main__":
    nmap = Map()
    print(nmap)
    choice = ""
    robot = Robot()
    while choice != "exit":
        nmap.induceAction()
        choice = robot.menu()
        if choice == "scout":
            move = robot.scout(nmap)
            robot.move(move, nmap)
        elif choice == "rest":
            robot.rest()
        elif choice == "report":
            robot.report(nmap)
        elif choice == "sharpen":
            robot.sharpen()
        else:
            print("I don't understand.")
