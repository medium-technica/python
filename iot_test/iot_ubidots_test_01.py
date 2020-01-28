import time
from ubidots import ApiClient

api = ApiClient(token='BBFF-cUZQOc2P5OQPZ56jLX5t6NpY5n4n5Q')
my_variable = api.get_variable('5c6a82a61d847233a6c20d00')
#new_value = my_variable.save_value({'value': 10})


# Getting all the values from the server. WARNING: If your variable has millions of datapoints, then this will take forever or break your code!
all_values = my_variable.get_values()

# If you want just the last 10 values you can use:
some_values = my_variable.get_values(10)
for i in range(10):
	last_value = my_variable.get_values(1)
	print (last_value[0]['value'])
	time.sleep(1);
	
'''
# Then you can read this value and do something:

if last_value[0]['value']:
    print "Switch is ON"
else:
    print "Switch is OFF"
'''
