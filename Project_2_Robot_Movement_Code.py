import serial, time, sys
import tkinter as tk
import time
import _thread, threading
import speech_recognition as sr

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

    def voiceController(self):
        while "exit" not in self.message:
            if "stop" in self.message:
                self.stop()
                self.message = "-1"
            elif "forward" in self.message:
                self.moveForward()
                self.message = "-1"
            elif "reverse" in self.message:
                self.moveReverse()
                self.message = "1"
            elif "turn left" in self.message:
                self.turnLeft()
                self.message = "-1"
            elif "turn right" in self.message:
                self.turnRight()
                self.message = "-1"
            elif "look up" in self.message:
                self.moveHeadUp()
                self.message = "-1"
            elif "look down" in self.message:
                self.moveHeadDown()
                self.message = "-1"
            elif "look left" in self.message:
                self.moveHeadLeft()
                self.message = "-1"
            elif "look right" in self.message:
                self.moveHeadRight()
                self.message = "-1"
            elif "rotate left" in self.message:
                self.moveWaistLeft()
                self.message = "-1"
            elif "rotate right" in self.message:
                self.moveWaistRight()
                self.message = "-1"

    def voiceInput(self):
        listening = True
        while listening:
            with sr.Microphone() as source:
                r = sr.Recognizer()
                r.adjust_for_ambient_noise(source)
                r.dynamic_energythreshhold = 3000

                try:
                    print("Listening")
                    audio = r.listen(source)
                    print("Got Audio")
                    self.message = r.recognize_google(audio)
                    print(self.message)
                except sr.UnknownValueError:
                    print("Unknown Word")

    def mainThread(self):
        i = 0
        while i != -1:
            if i % 10 == 0:
                print(str(i))
            i += 1

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
        print(key.keycode)
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
        print(key.keycode)
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
    try:
        print("Starting Thread")
        _thread.start_new_thread(robot.voiceInput,())
    except:
        print("Error: unable to start thread")
    robot.voiceController()
    #kc = KeyController(robot)

main()


