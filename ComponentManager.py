"""
Used for managing and updating the components on the timeline 
"""
from Components import Component
import sys, serial, time

#TangoBot Class from other projects
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


class ComponentManager:

    totalComponents = 0

    def __init__(self):
        self.timeline = []

    def createComponent(self, text):
        comp = Component.create(text)
        self.addToTimeline(comp)
        self.totalComponents += 1
        if not self.timeline:
            comp.setIndex(0)
        else:
            comp.setIndex(len(self.timeline) - 1)

    def getTotalComponents(self):
        return self.totalComponents


    def addToTimeline(self, component):
        self.timeline.append(component)

    def removeFromTimeline(self, component):
        self.timeline.remove(component)
    
    def clearTimeline(self):
        self.timeline = []
        self.totalComponents = 0
    
    def editConfig(self, index, config):
        #print("In Component Manager")
        #print(config)
        #print(self.timeline[index].getConfig())
        self.timeline[index].editConfig(config)
        
    def getTimeline(self):
        return self.timeline

    def runTimeline(self):
        robot = TangoBot()
        robot.stop()
        for component in self.timeline:
            component.execute()
            robot.moveHeadRight()
            if(component.type == "Head"):
                if(component.config == "updateleft"):
                    robot.moveHeadLeft()
                if(component.config == "updateRight"):
                    robot.moveHeadRight()
                if(component.config == "updateUp"):
                    robot.moveHeadUp()
                if(component.config == "updateDown"):
                    robot.moveHeadDown()
            if(component.type == "Waist"):
                if(component.config == "updateleft"):
                    robot.moveWaistRight()
                if(component.config == "updateRight"):
                    robot.moveWaistLeft()
            time.sleep(1)
