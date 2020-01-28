import math
import sys

from time import sleep
import urllib.request

a = 0
baseURL = 'http://api.thingspeak.com/update?api_key=E9SM1GGQLQ2XNILK&field1='
for n in range(100):
	response = urllib.request.urlopen(baseURL + str(a))
	html = response.read()
	print(str(html) + ", " + str(a))
	sleep(15)
	a = 50 + 50*math.sin(2 * 3.14 * 100 * (n * 0.001))
print ("Program has ended")
