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
                self.usb = serial.Serial('/dev/ttyACM0')
                print(self.usb.name)
                print(self.usb.baudrate)
            except:
                print("No servo serial ports found")
                sys.exit(0)

        #movement
        target = 5896
        #least significant bit
        lsb = target &0x7F
        #most significant bit
        msb = (target >> 7) &0x7F

        
        cmd = chr(0xaa) + chr(0xC) + chr(0x04) + chr(0x05) + chr(lsb) + chr(msb)

        #touch screen
        #motors
        #servos

        #Ports: 0-1 motor controls, 2 waist, 3-4 head, arms after that

    def move(self, key):
        print(key.keycode)

    def turn(self, key):
        print(key.keycode)

    def stop(self, key):
        print(key.keycode)

    def moveWaist(self, key):
        print(key.keycode)
    

#Keyboard input
win = tk.Tk()
keys = keyControl(win)

win.bind('<Up>', keys.move)
win.bind('<Left>', keys.turn)
win.bind('<Down>', keys.move)
win.bind('<Right>', keys.turn)
win.bind('<Space>', keys.stop)
win.bind('<z>', keys.moveWaist)
win.bind('<c>', keys.moveWaist)
win.bind('<w>', keys.moveHead)
win.bind('<a>', keys.moveHead)
win.bind('<s>', keys.moveHead)
win.bind('<d>', keys.moveHead)
win.mainloop()
keys = KeyControl(win)


