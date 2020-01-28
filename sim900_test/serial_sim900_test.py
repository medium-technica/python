import time
import serial
import sys
import msvcrt as m

def wait():
    m.getch()

def send_to_serial(data):
	ser.write(data+'\r')
	print "Data Sent: "+data
	time.sleep(0.2)

def read_serial_data():
	out = ''
	while ser.inWaiting():
		out += ser.read(1)
	return out

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(port='COM6',baudrate=9600,timeout=None)

ser.isOpen()


# Open a file
i=0

'''
data_lines_array = [line.rstrip('\n') for line in open('gprs_initialization_commands.txt')]

for data in data_lines_array:
	send_to_serial(data)
	print read_serial_data()
'''
data_lines_array = [line.rstrip('\n') for line in open('gprs_http_commands.txt')]
for data in data_lines_array:
	send_to_serial(data)
	time.sleep(1)
	print "Received Data: "+read_serial_data()
	wait()
	
