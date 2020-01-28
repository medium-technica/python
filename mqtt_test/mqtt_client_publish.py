#import msvcrt as m
import sys
import random as rand
import time as t
import paho.mqtt.client as mqtt #import the client1
#broker_address="192.168.1.184" 
#broker_address="iot.eclipse.org" #use external broker
broker_address="localhost"
client = mqtt.Client("client_id_01") #create new instance

#def wait_for_any_key():
#    m.getch()

count = 0;

for x in range(16):
	client.connect(broker_address) #connect to broker
	#msg_string = count%16
	msg_string = int(round(15*rand.random()))
	client.publish("outTopic",msg_string)#publish
	print ("Published!!!", msg_string)
	count+=1
	#t.sleep(1)
