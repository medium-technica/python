import os
import time
import sys
import paho.mqtt.client as mqtt
import json
import random

client = mqtt.Client()

HOST = 'test.mosquitto.org'
ACCESS_TOKEN = 'cuaA4VeO1QSkJ878J4if'

INTERVAL = 0.5

sensor_data = {'value': 0.0}

next_reading = time.time() 

def on_connect(client, userdata, flags, rc):
	global next_reading
	if rc==0:
		print("connected OK Returned code=",rc)
		#client.subscribe("value")
		client.subscribe('hello/world')
	else:
		print("Bad connection Returned code=",rc)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
	global next_reading
	print("received: " + msg.topic+" "+str(msg.payload))
	value = random.randrange(55)
	print(u"Sent: {:g}".format(value))
	sensor_data['value'] = value
	# Sending humidity and temperature data to ThingsBoard
	#client.publish('hello/world', json.dumps(sensor_data), 1)
	client.publish('hello/world', value)
	next_reading += INTERVAL
	sleep_time = next_reading-time.time()
	if sleep_time > 0:
		time.sleep(sleep_time)
    
# Register connect callback
client.on_connect = on_connect
# Registed publish message callback
client.on_message = on_message
# Set access token
#client.username_pw_set(ACCESS_TOKEN)
# Connect to ThingsBoard using default MQTT port and 60 seconds keepalive interval
client.connect(HOST, 1883)
client.publish('hello/world', random.randrange(55))
try:
	client.loop_forever()
except KeyboardInterrupt:
   pass



