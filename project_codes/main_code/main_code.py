import paho.mqtt.client as mqtt
import time as t
import os.path
import os
import numpy as np
import math
import methods_module as mm

broker_address = "localhost"
client = mqtt.Client("client_python_subcribe")
mm.user_id = "unknown"
mm.size_of_room_grid = [1,1]
mm.pixels_per_cell_grid = 64
mm.current_node_id = "0,0"
mm.previous_node_id = "0,0"
mm.entry_node_id = "0,0"
mm.last_node_id = "0,0"
mm.next_node_id = "0,0"
mm.dest_node_id = "0,0"
mm.broker_address = broker_address
mm.iteration_count = 0
mm.node_data_count = 0
mm.reset_flag = False
mm.initialize_variables()
mm.initialize_file_names()
mm.show_graph()

def fn_on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("outTopic")
    #mm.test_run()

def fn_on_message(client, userdata, msg):
	if(msg.topic == "outTopic"):
		msg.payload = msg.payload.decode("utf-8")
		mm.process_message(msg)


client.on_connect = fn_on_connect
client.on_message = fn_on_message

client.connect(broker_address, 1883, 60)
client.loop_forever()





