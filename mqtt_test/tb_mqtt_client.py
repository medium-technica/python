# https://github.com/thingsboard/thingsboard-python-client-sdk

from tb_device_mqtt import TBDeviceMqttClient, TBPublishInfo
import time
import random
import math

# THINGSBOARD_HOST = 'demo.thingsboard.io'
# ACCESS_TOKEN = 'cuaA4VeO1QSkJ878J4if'
THINGSBOARD_HOST = 'kabaniconnectdemo.ddns.net'
ACCESS_TOKEN = 'U4hXB5JT4gCszEp'

client = TBDeviceMqttClient(THINGSBOARD_HOST, ACCESS_TOKEN)

INTERVAL = 0.5
tick = time.time()
success = True
f1 = 0.01
nT = 0

# Connect to ThingsBoard
client.connect()
if client.is_connected:
	print("connected OK")
	while success:
		f2 = random.randrange(500)/1000
		i = 1
		while i <= 20:
			if time.time() - tick > INTERVAL :
				value = 50 + 35*math.sin(2 * math.pi * f1 * nT + (2/8*math.pi*random.random())) + 10*math.sin(2 * math.pi * f2 * nT) + random.randrange(5)
				telemetry = {
					"ts": int(round(time.time() * 1000)),
					"values": {
						"e6420": value
					}
				}
				named_tuple = time.localtime() # get struct_time
				time_string = time.strftime("%Y/%m/%d, %H:%M:%S -", named_tuple)
				print(f2,"Hz,", i, ":", time_string, telemetry['values']['e6420'])
				i+=1	
				# Sending telemetry and checking the delivery status (QoS = 1 by default)
				result = client.send_telemetry(telemetry)
				# get is a blocking call that awaits delivery status  
				success = result.get() == TBPublishInfo.TB_ERR_SUCCESS	
				tick = time.time()
				nT += INTERVAL / 10	
	print ("Sending Unsuccesful, diconnecting")
	# Disconnect from ThingsBoard
	client.disconnect()
