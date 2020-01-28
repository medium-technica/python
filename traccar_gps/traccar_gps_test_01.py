#!/usr/bin/python

import sys
import math
import urllib
import httplib
import time
import random

id = '416035'
server = 'demo5.traccar.org:5055'
period = 1
step = 0.001
speed1 = 40
lat1 = 10.7671786
lon1 = 76.2727124
speed_delta = 0

points = []

def send(conn, lat, lon, speed):
    params = (('id', id), ('timestamp', int(time.time())), ('lat', lat), ('lon', lon), ('speed', speed))
    print urllib.urlencode(params)
    conn.request('POST', '?' + urllib.urlencode(params))
    conn.getresponse().read()


index = 0
delta = 0.0000100;


conn = httplib.HTTPConnection(server)

while True:
	lat1 += delta
	lon1 += delta
	speed1 += speed_delta
	send(conn, lat1, lon1, speed1)
	time.sleep(period)
	speed_delta += 0.1
index += 1
