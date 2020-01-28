# Import library and create instance of REST client.
from Adafruit_IO import Client
aio = Client('3554a940f9c64bf7bcd292326a3e0f47')
data = aio.receive('waterflow')
print('Received value: {0}'.format(data.value))
