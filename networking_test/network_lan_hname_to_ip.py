#!/usr/bin/python           # This is client.py file

import socket               # Import socket module
#import msvcrt as m
import time
import sys


#def wait_for_any_key():
#    m.getch()

hname_array = [
"abraham-virtualbox", 
"abraham-pc", 
"android-724e08f31f257098", 
"ESP_1C2ED8", 
"raspberrypi", 
"Abraham-PC", 
"abraham-virtual",
"jiofi.local.html",
"www.google.com",
"raspberrypi"
]
for hname in hname_array:
	try:
		print ("IP of '"+hname+"' is :"+socket.gethostbyname(hname))
	except:
		print ("Error: ", sys.exc_info()[0])


