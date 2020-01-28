from time import sleep
import math
import sys
from ubidots import ApiClient

api = ApiClient(token='BBFF-seb79vW5XCFUmhatBKB6gmSPxoaANE')
my_variable = api.get_variable('5d0dd2c21d8472636d8f4e75')

a = 10
new_value = my_variable.save_value({"value":a,"context":{"lat":51.5,"lng":-0.11}})
print(a)

