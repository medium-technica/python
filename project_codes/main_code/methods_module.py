import paho.mqtt.client as mqtt
import time as t
import os.path
import os
import numpy as np
import math
import random as rand
import scipy.misc
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2
import face_recognition
import threading

global broker_address, user_id
user_id = "unknown"
def on_connect(client, userdata, flags, rc):
	#print("Connected with result code "+str(rc))
	global connect_flag
	connect_flag = True
	
def mqtt_client_publish(topic, message):
	global client, broker_address
	global connect_flag
	client.on_connect = on_connect
	client.connect(broker_address, 1883, 60)
	client.loop_start()
	
	while(connect_flag==False):
		#print("Waiting for connect ack from broker...")
		pass
	
	client.publish(topic,message)
	print ("Published!!!" + str(topic) + "/" + str(message))
	client.loop_stop()
	client.disconnect();

class msg():
	payload = 0
	topic = ""

def datetimestamp():
	now = t.time()
	localtime = t.localtime(now)
	milliseconds = '%03d' % int((now - int(now)) * 1000)
	return t.strftime('%Y%m%d%H%M%S', localtime) + milliseconds

def time_string():
	now = t.time()
	localtime = t.localtime(now)
	milliseconds = '%03d' % int((now - int(now)) * 1000)
	return t.strftime('%H:%M:%S', localtime) + "."+milliseconds

def get_face_info_from_webcam():
	global face_id
	face_id = "unknown"
	# Get a reference to webcam #0 (the default one)
	# video_capture = cv2.VideoCapture(0)
	ipwebcam_url = "http://192.168.1.4:8080/video"	#video_capture = cv2.VideoCapture("/home/abraham/Videos/V_20180104_095243.mp4")
	video_capture = cv2.VideoCapture(ipwebcam_url)

	# Load a second sample picture and learn how to recognize it.
	akash_image = face_recognition.load_image_file("../../images/abraham_02.jpg")
	akash_face_encoding = face_recognition.face_encodings(akash_image)[0]

	# Load a second sample picture and learn how to recognize it.
	hareesh_image = face_recognition.load_image_file("../../images/abraham_01.jpg")
	hareesh_face_encoding = face_recognition.face_encodings(hareesh_image)[0]

	# Load a second sample picture and learn how to recognize it.
	rahul_image = face_recognition.load_image_file("../../images/abraham_03.jpg")
	rahul_face_encoding = face_recognition.face_encodings(rahul_image)[0]

	# Create arrays of known face encodings and their names
	known_face_encodings = [
		akash_face_encoding,
		hareesh_face_encoding,
		rahul_face_encoding    
	]
	known_face_names = [
		"akash",
		"hareesh",
		"rahul"
	]

	# Initialize some variables
	face_locations = []
	face_encodings = []
	face_names = []
	process_this_frame = True

	while True:
		# Grab a single frame of video
		ret, frame = video_capture.read()
		frame = cv2.resize(frame, (0, 0), fx=0.75, fy=0.75)

		# Resize frame of video to 1/4 size for faster face recognition processing
		small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

		# Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
		rgb_small_frame = small_frame[:, :, ::-1]

		# Only process every other frame of video to save time
		if process_this_frame:
			# Find all the faces and face encodings in the current frame of video
			face_locations = face_recognition.face_locations(rgb_small_frame)
			face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

			face_names = []
			for face_encoding in face_encodings:
				# See if the face is a match for the known face(s)
				matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
				name = "unknown"

				# If a match was found in known_face_encodings, just use the first one.
				if True in matches:
					first_match_index = matches.index(True)
					name = known_face_names[first_match_index]
					face_id = name

				face_names.append(name)

		process_this_frame = not process_this_frame


		# Display the results
		for (top, right, bottom, left), name in zip(face_locations, face_names):
			# Scale back up face locations since the frame we detected in was scaled to 1/4 size
			top *= 4
			right *= 4
			bottom *= 4
			left *= 4

			# Draw a box around the face
			cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

			# Draw a label with a name below the face
			cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
			font = cv2.FONT_HERSHEY_DUPLEX
			cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

		# Display the resulting image
		cv2.imshow('Video', frame)

		# Hit 'q' on the keyboard to quit!
		if cv2.waitKey(1) & 0xFF == ord('q'):
			cv2.destroyWindow('Video')
			break

	# Release handle to the webcam
	video_capture.release()
	return face_id

def initialize_variables():
	print ("Initializing variables...")
	global size_of_room_grid, size_of_square_probability_matrix
	global pixels_per_cell_grid, next_node_id, dest_node_id
	global probability_matrix, current_probability_matrix
	global current_node_position, previous_node_position, next_node_position, dest_node_position, current_node_id, previous_node_id, entry_node_id
	global reset_flag, node_data_count
	
	size_of_square_probability_matrix = [size_of_room_grid[0] * 3, size_of_room_grid[1] * 3]
	
	probability_matrix = [[0] * size_of_square_probability_matrix[1] for i in range(size_of_square_probability_matrix[0])]
	current_probability_matrix = [[0] * size_of_square_probability_matrix[1] for i in range(size_of_square_probability_matrix[0])]
	
	current_node_position = convert_node_id_string_to_position_coordinates(current_node_id)
	next_node_position = convert_node_id_string_to_position_coordinates(next_node_id)
	dest_node_position = convert_node_id_string_to_position_coordinates(dest_node_id)
	previous_node_position = convert_node_id_string_to_position_coordinates(previous_node_id)
	
	reset_flag = False
	node_data_count = 0
	
def initialize_file_names():
	global file_name_node_data, file_name_probability_matrix, user_id
	print ("Initializing variables...")
	file_name_node_data = user_id+"_"+"node_data_file.txt"
	file_name_probability_matrix = user_id+"_"+"probability_matrix_file_test.txt"
	if (os.path.isfile(file_name_probability_matrix)):
		load_probability_matrix_from_file(file_name_probability_matrix)

def node_id_value_to_prob_matrix_index(node_id_value):
	return 3*(node_id_value) + 1

def update_probability_matrix_from_new_node_data(node_id):
	print("Updating p.matrix from new node data...")
	node_position_coordinates = convert_node_id_string_to_position_coordinates(node_id)
	probability_matrix_coordinates = convert_node_grid_coordinate_to_probability_matrix_coordinate(node_position_coordinates)
	probability_matrix[probability_matrix_coordinates[0]][probability_matrix_coordinates[1]] += 1
	current_probability_matrix[probability_matrix_coordinates[0]][probability_matrix_coordinates[1]] += 1
	save_probability_matrices_to_file()

def process_file_and_update_probability(file_name_node_data):
	file = open(file_name_node_data, "r") 
	for line_string in file: 
		temp_array = line_string.split(",")
		if (len(temp_array) >= 2):
			node_id_array.append(int(temp_array[1].strip())) 
		else:
			print ("File "+file_name_node_data+" format incorrect!!!")
	file.close()

	for node_id in node_id_array:
		update_probability_matrix_from_new_node_data(node_id)
		
def print_matrix_2d(matrix):
	for i in matrix:
		for j in i:
			print(j, end=' ')
		print ()

def highlight_grid_cell(base_image, cell_position, highlight_area, pixels_per_cell_grid):
	pixel_positon = [int((cell_position[0]*pixels_per_cell_grid)), int((cell_position[1]*pixels_per_cell_grid))]
	cv2.circle(base_image,(pixel_positon[1]+int(pixels_per_cell_grid/2), pixel_positon[0]+int(pixels_per_cell_grid/2)), highlight_area, (255,255,255), -1)
	return base_image
	
def generate_grid_image(array_2d, pixels_per_cell_grid):
	nparray = np.array(array_2d)
	h_p_matrix = nparray.shape[0]
	w_p_matrix = nparray.shape[1]
	h_room_grid = h_p_matrix//3
	w_room_grid = w_p_matrix//3
	scale = [h_room_grid*pixels_per_cell_grid, w_room_grid*pixels_per_cell_grid];
	ndarray = np.ndarray(shape=(3,h_p_matrix,w_p_matrix))
	ndarray[0] = nparray
	ndarray[1] = nparray
	ndarray[2] = nparray
	imarray = np.resize(ndarray, scale)
	grid_pixel_rows = [i*pixels_per_cell_grid for i in range(h_p_matrix)]
	grid_pixel_columns = [i*pixels_per_cell_grid for i in range(w_p_matrix)]
	overlay = imarray.copy()
	
	overlay = highlight_grid_cell(overlay, current_node_position, pixels_per_cell_grid//2, pixels_per_cell_grid)
	overlay = highlight_grid_cell(overlay, next_node_position, pixels_per_cell_grid//3, pixels_per_cell_grid)
	overlay = highlight_grid_cell(overlay, dest_node_position, pixels_per_cell_grid//4, pixels_per_cell_grid)
	
	alpha = .8
	letter_size = 0.6
	for c in grid_pixel_rows:
		for r in grid_pixel_columns:
			cv2.rectangle(overlay, (c, r), (r+pixels_per_cell_grid, c+pixels_per_cell_grid),(128, 128, 128), 2)
			cv2.putText(overlay, str(c//pixels_per_cell_grid - 1)+","+str(r//pixels_per_cell_grid),(r+(int(pixels_per_cell_grid/2)-15), c-(int(pixels_per_cell_grid/2))+7), cv2.FONT_HERSHEY_SIMPLEX, letter_size, (255, 255, 0), 2)
	return overlay

def show_2darray_as_image(window_title, array_2d, pixels_per_cell_grid):
	quantized_array = quantize_array_values(array_2d)
	image_array = generate_grid_image(quantized_array, pixels_per_cell_grid)
	cv2.imshow(window_title, image_array)
	# Hit 'q' on the keyboard to quit!
	if cv2.waitKey(1) & 0xFF == ord('q'):
		exit()

def quantize_array_values(x):
	max_value = find_max_array_2d(x)
	mid_value = int(max_value / 2)
	min_value = int(max_value /3)
	r=0
	c=0
	for column in x:
		c=0
		for element in column:
			if (element > mid_value):
				x[r][c] = 3
			elif (element > min_value):
				x[r][c] = 2
			elif (element > 0):
				x[r][c] = 1
			c+=1
		r+=1
		
	return x

def find_max_array_2d(array_2d):
	max_value = 0
	for i in array_2d:
		if(max_value < max(i)):
			max_value = max(i)
	return max_value

def load_probability_matrix_from_file(file_name):
	global probability_matrix, current_probability_matrix, size_of_room_grid
	print ("Loading Probability matrix from last saved file...")
	t_probability_matrix = []
	file = open(file_name, "r")
	i=0
	for line_string in file:
		j=0
		temp_array = (line_string.strip()).split()
		t_probability_matrix.append([])
		for element in temp_array:
			t_probability_matrix[i].append(int(element.strip()))
			j+=1
		i+=1
	file.close()
	probability_matrix = merge_array_contents(t_probability_matrix, probability_matrix)
	rows_p_m = len(probability_matrix[:])
	cols_p_m = len(probability_matrix[0][:])
	t_current_probability_matrix = [[0] * cols_p_m for i in range(rows_p_m)]
	current_probability_matrix = merge_array_contents(current_probability_matrix, t_current_probability_matrix)
	size_of_room_grid = [rows_p_m//3, cols_p_m//3]
	save_probability_matrices_to_file()

def merge_array_contents(array_one, array_two):
	print("Merging array contents...")
	dim_array_one = [len(array_one[0][:]), len(array_one[:])]
	dim_array_two = [len(array_two[0][:]), len(array_two[:])] 
	dim_array_larger = [max(dim_array_one[1], dim_array_two[1]), max(dim_array_one[0], dim_array_two[0])]
	array_larger = [[0] * dim_array_larger[1] for i in range(dim_array_larger[0])]
	dim_array_smaller = [min(dim_array_one[1], dim_array_two[1]), min(dim_array_one[0], dim_array_two[0])]
	
	for i in range(dim_array_one[1]):
		for j in range(dim_array_one[0]):
				array_larger[i][j] = array_larger[i][j] + array_one[i][j]
	
	for i in range(dim_array_two[1]):
		for j in range(dim_array_two[0]):
			array_larger[i][j] = array_larger[i][j] + array_two[i][j]
	return(array_larger)

def save_probability_matrix_to_file(file_name):
	file = open(file_name,"w")
	write_string = ""
	for column in probability_matrix:
		for element in column:
			write_string += str(element) + " "
		write_string += "\n"
	file.write(write_string) 
	file.close()

def append_real_time_node_data_to_file(node_id):
	write_string = datetimestamp()+","+str(node_id)+"\n"
	now = t.time()
	localtime = t.localtime(now)
	file_name_string_node_data = t.strftime('%Y%m%d', localtime)+"_"+file_name_node_data
	file = open(file_name_string_node_data,"a+") 
	file.write(write_string)
	file.close()

def convert_node_id_string_to_position_coordinates(node_id_string):
	node_coordinates_string = node_id_string.split(",")
	node_coordinates = [int(node_coordinates_string[0]), int(node_coordinates_string[1])]
	return node_coordinates

def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = math.degrees(np.arctan2(y, x))
    return([rho, phi])

def calculate_displacement_vector(previous_position, current_position):
	displacement_gradient = [0]*len(current_position[:])
	for i in range(len(displacement_gradient)):
		displacement_gradient[i] = previous_position[i] - current_position[i]
	[rho, phi] = cart2pol(displacement_gradient[0], displacement_gradient[1])
	
	return ([rho,phi])

def approximate_angle_resolution_to_45_degrees(angle):
	approximated_angle = str(round(angle / 45) * 45)
	return approximated_angle


def convert_angle_to_direction_coordinate(angle):
	angle = str(angle)
	switch = {
	'0': [-1,0],
	'45': [-1,-1],
	'90': [0,-1],
	'135': [1,-1],
	'180': [1,0],
	'-45': [-1,1],
	'-90':[0,1],
	'-135':[1,1],
	'-180':[1,0]
	}	
	return switch[angle]
	
def convert_node_grid_coordinate_to_probability_matrix_coordinate(node_position_coordinates):
	row_coordinate = node_id_value_to_prob_matrix_index(node_position_coordinates[0])
	column_coordinate = node_id_value_to_prob_matrix_index(node_position_coordinates[1])
	return [row_coordinate, column_coordinate]

def calculate_and_insert_probability_data_into_probability_matrix(previous_position, angle_of_current_node_id):
	approximated_angle = approximate_angle_resolution_to_45_degrees(angle_of_current_node_id)
	direction_coordinate = convert_angle_to_direction_coordinate(approximated_angle)
	previous_position_probability_matrix = convert_node_grid_coordinate_to_probability_matrix_coordinate(previous_position)
	probability_update_position = np.add(previous_position_probability_matrix, direction_coordinate)
	probability_matrix[probability_update_position[0]][probability_update_position[1]] += 1
	current_probability_matrix[probability_update_position[0]][probability_update_position[1]] += 1

def resize_size_of_room_grid(current_node_position):
	global size_of_room_grid, current_node_id, next_node_id, dest_node_id, last_node_id, previous_node_id
	global probability_matrix, current_probability_matrix
	print("Resizing room grid size...")
	size_of_room_grid = [max(size_of_room_grid[0], current_node_position[0]+1), max(size_of_room_grid[1], current_node_position[1]+1)]
	print("New room grid size: "+str(size_of_room_grid))
	rows_p_m = size_of_room_grid[0]*3
	cols_p_m = size_of_room_grid[1]*3
	t_probability_matrix = [[0] * cols_p_m for i in range(rows_p_m)]
	probability_matrix = merge_array_contents(probability_matrix, t_probability_matrix)
	t_current_probability_matrix = t_probability_matrix[:]
	current_probability_matrix = merge_array_contents(current_probability_matrix, t_current_probability_matrix)
	save_probability_matrices_to_file()
	
def check_if_node_position_is_outside_room_grid(node_position):
	print("Checking if Node ID is outside boundary...")
	print("Node Position: "+str(node_position)+", Room grid size: "+str(size_of_room_grid))
	if (node_position[0] >= size_of_room_grid[0] or node_position[1] >= size_of_room_grid[1]):
		return True
	else:
		return False  

def process_message(msg):
	global node_data_count, previous_node_position, next_node_position, dest_node_position, current_node_position, current_node_id, previous_node_id, corner_node_position, last_node_id
	global angle_of_current_node_id, reset_flag, user_id, current_probability_matrix, next_node_id, dest_node_id
	approximated_angle = 0
	os.system('clear')
	current_node_id = msg.payload
	current_node_position = convert_node_id_string_to_position_coordinates(current_node_id)
	print("Node ID: "+str(current_node_position)+" received @: "+time_string())
	while (user_id == "unknown"):
		begin_entry()
	print("User ID = "+user_id)

	if(check_if_node_position_is_outside_room_grid(current_node_position)):
		print("Node ID is Outside the boundary")
		resize_size_of_room_grid(current_node_position)

	reset_flag = ((current_node_id == entry_node_id) & (previous_node_id != entry_node_id))

	if(reset_flag!=True):
		append_real_time_node_data_to_file(current_node_id)
		update_probability_matrix_from_new_node_data(current_node_id)
		if (node_data_count > 0):
			position_vector_polar_coordinate = calculate_displacement_vector(previous_node_position, current_node_position)
			angle_of_current_node_id = position_vector_polar_coordinate[1]
			distance_from_previous_position = position_vector_polar_coordinate[0]
			if (distance_from_previous_position>0):
				approximated_angle = approximate_angle_resolution_to_45_degrees(angle_of_current_node_id)
				calculate_and_insert_probability_data_into_probability_matrix(previous_node_position, angle_of_current_node_id)
		#print_matrix_2d(probability_matrix)
		if (last_node_id != current_node_id):
			[next_node_id, probability_value] = find_most_probable_next_node_avoiding_previous_node(current_node_id, previous_node_id)
			[max_stayed_node_id, largest_stay_count] = find_max_stayed_node_in_the_forward_path(current_node_id, previous_node_id, next_node_id, 0)
			dest_node_id = max_stayed_node_id
			#print ("Pr.Node:", previous_node_id, "C.Node:", current_node_id, ", N.P.Node:", next_node_id, ", P.D.Node:",max_stayed_node_id)		
			print (previous_node_id, "->", current_node_id, "->", "["+next_node_id+"]","->","["+max_stayed_node_id+"]")
			mqtt_client_publish("current", str(current_node_id))
			mqtt_client_publish("next", str(next_node_id))
			mqtt_client_publish("dest", str(dest_node_id))
			previous_node_id = current_node_id
			previous_node_position = current_node_position[:]
		else:
			next_node_id = dest_node_id = current_node_id
			print ("User staying in Node ["+current_node_id+"]")
			mqtt_client_publish("current", str(current_node_id))
			mqtt_client_publish("next", str(next_node_id))
			mqtt_client_publish("dest", str(dest_node_id))
			
		last_node_id = current_node_id
		node_data_count += 1
		reset_flag = False
	else:
		print ("Current User Reached Path Exit!!!", "Current Node: ["+current_node_id+"], Previous Node: ["+previous_node_id+"]")
		system_reset()
	
	next_node_position = convert_node_id_string_to_position_coordinates(next_node_id)
	dest_node_position = convert_node_id_string_to_position_coordinates(dest_node_id)

def save_probability_matrices_to_file():
	save_probability_matrix_to_file(file_name_probability_matrix)
	file_name_backup_probability_matrix = t.strftime("%Y%m%d")+"_"+file_name_probability_matrix
	save_probability_matrix_to_file(file_name_backup_probability_matrix)

def show_graph():
	global probability_matrix, current_probability_matrix, pixels_per_cell_grid, reset_flag
	if(reset_flag!=True):
		threading.Timer(0.3, show_graph).start()
		window_title = "Probability Matrix"
		show_2darray_as_image(window_title, probability_matrix, pixels_per_cell_grid)
		window_title = "Current Path Status"
		show_2darray_as_image(window_title, current_probability_matrix, pixels_per_cell_grid)

def system_reset():
	global user_id, next_node_id, dest_node_id, current_node_id, previous_node_id
	print("Resetting system!!!")
	user_id = "unknown"
	rows_p_m = size_of_room_grid[0]*3
	cols_p_m = size_of_room_grid[1]*3
	current_probability_matrix = [[0] * cols_p_m for i in range(rows_p_m)]
	previous_node_id = next_node_id = dest_node_id = current_node_id
	mqtt_client_publish("current", str(current_node_id))
	mqtt_client_publish("next", str(next_node_id))
	mqtt_client_publish("dest", str(dest_node_id))
	
def begin_entry():
	status_face_id = "n"
	while(status_face_id!="y"):
		print ("Waiting for new User information from Webcam face recognition...")
		face_id = get_face_info_from_webcam()
		status_face_id = input("Are you "+face_id+"? (y/n)")
	print("Got Face ID: "+face_id)
	initialize_variables()
	set_user_id(face_id)
	initialize_file_names()

def scan_probability_matrix_and_get_next_nodes_around_node_id_with_probability_values(node_id):
	node_coordinates = convert_node_id_string_to_position_coordinates(node_id)
	probability_matrix_coordinate = convert_node_grid_coordinate_to_probability_matrix_coordinate(node_coordinates)
	next_nodes_probability_values_array = []
	next_nodes_array = []
	for i in [-1,0,1]:
		for j in [-1,0,1]:
			if (not((i==0)&(j==0))):
				probability_value = probability_matrix[probability_matrix_coordinate[0]+i][probability_matrix_coordinate[1]+j]
				next_nodes_probability_values_array.append(probability_value)
				next_node_id = convert_node_coordinate_to_node_id_string(np.add(node_coordinates,[i,j]))
				next_nodes_array.append(next_node_id)
	return_array = [next_nodes_array, next_nodes_probability_values_array]
	#print (node_id, return_array)
	return return_array 
	
	
def find_most_probable_next_node_avoiding_previous_node(current_node_id, previous_node_id):
	[next_nodes_array, next_nodes_probability_values_array] = scan_probability_matrix_and_get_next_nodes_around_node_id_with_probability_values(current_node_id)
	largest_probability_value = 0
	next_node_id = current_node_id
	for [probability_value, node_id] in zip(next_nodes_probability_values_array, next_nodes_array):
		if (node_id!=previous_node_id):
			if (probability_value > largest_probability_value):
				largest_probability_value = probability_value
				next_node_id = node_id
	#print("N. Node:",next_node_id, "L. P. Value:", largest_probability_value)
	return [next_node_id, largest_probability_value]

def find_max_stayed_node_in_the_forward_path(current_node_id, previous_node_id, max_stayed_node_id, largest_stay_count):
	global iteration_count
	iteration_count+=1
	[next_node_id, probability_value] = find_most_probable_next_node_avoiding_previous_node(current_node_id, previous_node_id)
	max_stayed_node_id = next_node_id
	if ((current_node_id!=next_node_id)&(iteration_count<(size_of_room_grid[0]*size_of_room_grid[1]))):
		current_node_coordinates = convert_node_id_string_to_position_coordinates(current_node_id)
		probability_matrix_coordinates = convert_node_grid_coordinate_to_probability_matrix_coordinate(current_node_coordinates)
		stay_count = probability_matrix[probability_matrix_coordinates[0]][probability_matrix_coordinates[1]]
		if(stay_count > largest_stay_count):
			largest_stay_count = stay_count
			max_stayed_node_id = current_node_id
		[max_stayed_node_id, largest_stay_count] = find_max_stayed_node_in_the_forward_path(next_node_id, current_node_id, max_stayed_node_id, largest_stay_count)
	iteration_count = 0
	#print("P. Node: ",previous_node_id, "C. Node:", current_node_id, "N. Node:", next_node_id, "Max. Stayed Node:", max_stayed_node_id, "Stay Count:", largest_stay_count)
	return [max_stayed_node_id, largest_stay_count]

def convert_node_coordinate_to_node_id_string(node_coordinates):
	node_id = str(node_coordinates[0])+","+str(node_coordinates[1])
	return node_id 

def set_user_id(username):
	global user_id
	user_id = username
	print("Setting User ID...")
	
def test_run():
	global node_data_count, previous_node_position, next_node_id, size_of_room_grid
	size_of_room_grid = 4
	test_node_id_sequence = {
	'0': ["0,0", "0,1","0,2","1,3","1,3","0,2", "0,2", "0,2", "0,2", "0,2", "0,2", "0,2", "0,1", "0,1", "0,1", "0,1", "0,0"],
	'1': ["0,0", "1,1", "1,2","2,2","2,3","2,3","2,2", "1,2", "1,2", "1,1", "1,1", "1,1", "1,1", "0,0"],
	'2': ["0,0", "1,0", "2,0","3,1","3,2","3,3","3,3","3,3","3,3", "3,3", "3,3", "3,3", "3,2","3,1", "2,0", "2,0", "2,0", "1,0", "0,0"],
	
	}
	'''
	test_node_id_sequence = {
	'0': ["0,0", "0,1","0,2","1,3","1,3","0,2","0,1","0,0"]
	}
	'''
	for j in range(3):
		sequence = test_node_id_sequence[str(int(round(2*rand.random())))]
		for i in sequence:
			msg.payload = i
			process_message(msg)
			t.sleep(1)
			#input()
	#input()

	while(True):
		msg.payload = input("Enter node id Eg: "+str(next_node_id)+" :")
		node_id_string = msg.payload.split(",")
		if((type(int(node_id_string[0])) is int) & (type(int(node_id_string[1])) is int)):
			process_message(msg)
		else:
			print("Invalid numerical value (data type) entered!!!, Try again.")

def test_run_01():
	rows = 1
	columns = 10
	array_one = [[0,1,0,0,0],[0,1,2,0,0],[0,3,4,0,0],[0,0,0,4,6]]
	array_two = [[1] * columns for i in range(rows)]
	print_matrix_2d(array_one)
	print("")
	print_matrix_2d(array_two)
	print("")
	m_array = merge_array_contents(array_one, array_two)
	print_matrix_2d(m_array)
	#print(find_max_array_2d(m_array))
	
	
#test_run()



