from time import sleep
import math
import sys
from ubidots import ApiClient

api = ApiClient(token='BBFF-CTRSpeSd93nRjEFCKZHRVbrMoVLfiB')
my_variable = api.get_variable('5c7f8b561d84724cf347b04d')

for n in range(100):
	a = 50 + 50*math.sin(2 * 3.14 * 100 * (n * 0.001))
	new_value = my_variable.save_value({'value': a})
	print(a)
	sleep(2)
print ("Program has ended")

	
'''
# Then you can read this value and do something:

if last_value[0]['value']:
    print "Switch is ON"
else:
    print "Switch is OFF"
'''
