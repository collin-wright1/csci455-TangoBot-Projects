#from Project_2_Robot_Movement_Code import TangoBot
import sys

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

"""
Class for storing movements and options on the timeline.
Type dictates which group of functionality is targeted
Config is a dictionary of variables or commands, dependent on the function.
"""
class Component:
    config = ""
    type = ""
    index = None

    # don't know if index or type is really necessary here but I'm scared to touch them

    # decides which component to create
    def create(text):
        if text == "Motor":
            return MotorComponent("")
        elif text == "Head":
            return HeadComponent("")
        elif text == "Waist":
            return WaistComponent("")
        elif text == "SpeechIn":
            return speechInput("")
        elif text == "SpeechOut":
            return speechOutput("")

    def getConfig(self):
        return self.config

    def getIndex(self):
        return self.index
    
    def setIndex(self, index):
        self.index = index

    def editConfig(self, newConfig):
        #print("in Component")
        #print(newConfig)
        self.config = newConfig

    def execute():
        pass


class MotorComponent(Component):

    # need speed and time, direction stored in speed

    def __init__(self, config):
        self.type = "Motor"
        self.config = config

    # TODO: Implement motor execute
    def execute(self):
        robot = TangoBot()
        print(self.type)
        print(self.config)

class HeadComponent(Component):

    def __init__(self, config):
        self.type = "Head"
        self.config = config

    # TODO: Implement Head Execute
    def execute(self):
        print(self.type)
        print(self.config)

class WaistComponent(Component):

    def __init__(self, config):
        self.type = "Waist"
        self.config = config

    # TODO: Implement waist execute
    def execute(self):
        print(self.type)
        print(self.config)

class speechInput(Component):

    def __init__(self, config):
        self.type = "speechInput"
        self.config = config

    # TODO: Implement speech in execute
    def execute(self):
        print(self.type)
        print(self.config)

class speechOutput(Component):

    def __init__(self, config):
        self.type = "speechOutput"
        self.config = config

    # TODO: Implement speech out execute
    def execute(self):
        print(self.type)
        print(self.config)
