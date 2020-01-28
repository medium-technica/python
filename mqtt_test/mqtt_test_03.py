import math
import random
import sys
import time

from Adafruit_IO import MQTTClient

ADAFRUIT_IO_KEY      = '938f74dec434480b8cd1138c9a49ba8b'
ADAFRUIT_IO_USERNAME = 'abeyalexander'

client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

client.connect()

last = 0
x = 0
print('Publishing a new message every 1 seconds (press Ctrl-C to quit)...')
while True:
	client.loop()
	if (time.time() - last) >= 1.0:
		value = 100 + 50*math.sin(x)
		x+=0.1
		print('Publishing {0} to DemoFeed.'.format(value))
		client.publish('demofeed', value)
		last = time.time()
