import serial, time, sys
import tkinter as tk

class TangoBot:

    #initializes robot
    def __init__(self):
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

        #movement
        target = 4500
        #least significant bit
        lsb = target &0x7F
        #most significant bit
        msb = (target >> 7) &0x7F

        cmd = chr(0xaa) + chr(0xC) + chr(0x04) + chr(0x02) + chr(lsb) + chr(msb)
        print('reading')
        self.usb.write(cmd.encode())
        print('writing')
        #touch screen
        #motors
        #servos

        #Ports: 0-1 motor controls, 2 waist, 3-4 head, arms after that

    def moveForward(self, key):
        print("moving forward")
        self.makeCommand(4200, 0x01)

    def moveReverse(self, key):
        print("moving reverse")

    def turnRight(self, key):
        print('turning right')

    def turnLeft(self, key):
        print('turning left')

    def stop(self, key):
        print("stopping")

    def moveWaist(self, key):
        print("swiveling")

    def moveHead(self, key):
        print("move head")

    def makeCommand(self, target, port):
        lsb = target &0x7F
        msb = (target >> 7) &0x7F
        cmd = chr(0xaa) + chr(0xC) + chr(0x04) + chr(port) + chr(lsb) + chr(msb)
        print(cmd)
        self.execute(cmd)

    def execute(self, cmd):
        print('Writing')
        self.usb.write(cmd.encode('utf-8'))
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
            self.robot.moveWaist(key)
        elif(key.keycode == 54):
            self.robot.moveWaist(key)
            

    def head(self, key):
        if(key.keycode == 25):
            self.robot.moveHead(key)
        elif(key.keycode == 38):
            self.robot.moveHead(key)
        elif(key.keycode == 39):
            self.robot.moveHead(key)
        elif(key.keycode == 40):
            self.robot.moveHead(key)
    

def main():
    robot = TangoBot()
    kc = KeyController(robot)

main()


