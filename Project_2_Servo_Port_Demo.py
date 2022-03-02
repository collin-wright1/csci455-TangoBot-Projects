import serial, time, sys

try:
    usb = serial.Serial('<USB LOCATION>')
    print(usb.name)
    print(usb.baudrate)

except:
    try:
        usb = serial.Serial('<OTHER USB LOCATION>')
        print(usb.name)
        print(usb.baudrate)
    except:
        print("No servo serial ports found.")
        sys.exit(0)

target = 6700

#least significant bit
lsb = target &0x7F
#most significant bit
msb = (target >> 7) &0x7F

                                        #Port number
cmd = chr(0xaa) + chr(0xC) + chr(0x04) + chr(0x03) + chr(lsb) + chr(msb)

print('Writing')
usb.write(usb.encode('utf-8'))
print('Reading')
