import time
import serial
import sys

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    port='COM6',
    baudrate=9600,
    timeout=None
)

ser.isOpen()
print 'Enter your commands below.\r\nInsert "exit" to leave the application.'

input=1
while 1 :
    # get keyboard input
    input = raw_input(">> ")
  
    if input == 'exit':
        ser.close()
        exit()
    else:
        ser.write(input)
        ser.write('\r')
        out = ''
        time.sleep(0.2)
        while ser.inWaiting():
			out += ser.read(1)
	if out != '':
		print out
