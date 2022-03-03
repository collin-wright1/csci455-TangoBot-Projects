import serial, time, sys
import tkinter as tk

class TangoBot:

    #initializes robot
    def __init__(self):

        self.waist = 6000
        self.headHorz  = 6000
        self.headVert = 6000
        self.motors = 6000

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

        self.makeCommand(self.headHorz, 0x03)
        self.makeCommand(self.headVert, 0x04)
        self.makeCommand(self.waist, 0x02)
        self.makeCommand(self.motors, 0x01)

        #movement
        #target = 6000
        #least significant bit
        #lsb = target &0x7F
        #most significant bit
        #msb = (target >> 7) &0x7F

        #cmd = chr(0xaa) + chr(0xC) + chr(0x04) + chr(0x03) + chr(lsb) + chr(msb)
        #print('reading')
        #print(cmd.encode())
        #self.usb.write(cmd.encode())
        #print('writing')
        #touch screen
        #motors
        #servos

        #Ports: 0-1 motor controls, 2 waist, 3-4 head, arms after that

    def moveForward(self, key):
        print("moving forward")
        self.motors += 200
        self.makeCommand(self.motors, 0x01)

    def moveReverse(self, key):
        self.motors -= 200
        print("moving reverse")
        self.makeCommand(self.motors, 0x01)

    def turnRight(self, key):
        print('turning right')

    def turnLeft(self, key):
        print('turning left')

    def stop(self, key):
        print("stopping")

    def moveWaistLeft(self, key):
        self.waist += 200
        print("swiveling left")
        self.makeCommand(self.waist, 0x02)

    def moveWaistRight(self, key):
        self.waist -= 200
        print("swiveling right")
        self.makeCommand(self.waist, 0x02)

    def moveHeadRight(self, key):
        print("move head right")
        self.headHorz -= 200
        self.makeCommand(self.headHorz, 0x03)

    def moveHeadLeft(self, key):
        print("move head left")
        self.headHorz += 200
        self.makeCommand(self.headHorz, 0x03)

    def moveHeadUp(self, key):
        print("move head up")
        self.headVert += 200
        self.makeCommand(self.headVert, 0x04)

    def moveHeadDown(self, key):
        print("move head down")
        self.headVert -= 200
        self.makeCommand(self.headVert, 0x04)

    def makeCommand(self, target, port):
        lsb = target &0x7F
        msb = (target >> 7) &0x7F
        cmd = chr(0xaa) + chr(0xC) + chr(0x04) + chr(port) + chr(lsb) + chr(msb)
        print("Commanding", cmd)
        self.execute(cmd)

    def execute(self, cmd):
        print('Writing')
        self.usb.write(cmd.encode())
        print('Reading')


#implements keyboard input
class KeyController:

    def __init__(self, robo):

        self.robot = robo

        win = tk.Tk()

        win.bind('<Up>', self.arrows)
        win.bind('<Left>', self.arrows)
        win.bind('<Down>', self.arrows)
        win.bind('<Right>', self.arrows)
        win.bind('<space>', self.arrows)
        win.bind('<z>', self.waist)
        win.bind('<c>', self.waist)
        win.bind('<w>', self.head)
        win.bind('<a>', self.head)
        win.bind('<s>', self.head)
        win.bind('<d>', self.head)
        win.mainloop()

    def arrows(self, key):
        if(key.keycode == 111):
            self.robot.moveForward(key)
        elif(key.keycode == 116):
            self.robot.moveReverse(key)
        elif(key.keycode == 113):
            self.robot.turnLeft(key)
        elif(key.keycode == 114):
            self.robot.turnRight(key)
        elif(key.keycode == 65):
            self.robot.stop(key)

    def waist(self, key):
        print(key.keycode)
        if(key.keycode == 52):
            self.robot.moveWaistLeft(key)
        elif(key.keycode == 54):
            self.robot.moveWaistRight(key)

    def head(self, key):
        if(key.keycode == 25):
            self.robot.moveHeadUp(key)
        elif(key.keycode == 38):
            self.robot.moveHeadLeft(key)
        elif(key.keycode == 39):
            self.robot.moveHeadDown(key)
        elif(key.keycode == 40):
            self.robot.moveHeadRight(key)
    

def main():
    robot = TangoBot()
    kc = KeyController(robot)

main()


