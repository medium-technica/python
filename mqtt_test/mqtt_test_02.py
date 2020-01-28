#import msvcrt as m
import sys
import paho.mqtt.client as mqtt #import the client1
#broker_address="192.168.1.184" 
#broker_address="iot.eclipse.org" #use external broker
broker_address="test.mosquitto.org"
client = mqtt.Client("client_id_01") #create new instance

#def wait_for_any_key():
#    m.getch()

for x in range(0, 3):
	client.connect(broker_address) #connect to broker
	client.publish("abraham_123984714","Hai This is Abraham")#publish
	print "Published!!!"
	#wait_for_any_key();
