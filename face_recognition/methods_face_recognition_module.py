import face_recognition
#import cv2
#import numpy as np
import pickle
import glob
import time as t

def encode_jpg_images_and_save_face_encodings_to_file(file_path, save_file_name):
	image_path_string = file_path

	file_list = glob.glob(image_path_string+"*.jpg")
	f_name_jpg = []
	for f_name in file_list:
		f_name_jpg.append(f_name[len(image_path_string):])
		
	face_encodings_to_save = []
	face_names_to_save = []
	count = 0
	for fname in f_name_jpg:
		image = face_recognition.load_image_file(image_path_string+fname)
		image_face_encodings = face_recognition.face_encodings(image)
		print(len(image_face_encodings))
		face_count = 1
		for face_encoding in image_face_encodings:
			face_encodings_to_save.append(face_encoding)
			face_name_string = fname[:-4]+"_"+str(face_count)
			face_names_to_save.append(face_name_string)
			print (face_name_string)
			count+=1
			face_count+=1
			
	face_data_to_save = [face_encodings_to_save, face_names_to_save]
	outfile = open(file_path+save_file_name, 'wb')
	pickle_string = pickle.dumps(face_data_to_save)
	pickle.dump(pickle_string, outfile)
	outfile.close
	
	outfile = open(file_path+save_file_name, 'rb')
	pickle_string = pickle.load(outfile)
	outfile.close
	face_data = pickle.loads(pickle_string)
	[face_encodings, face_names] = face_data
	print ("No. of Face Encodings saved :",len(face_names))

def match_face_encodings_with_image(file_name_encodings, image_file):
	#print (t.time())
	outfile = open(file_name_encodings, 'rb')
	pickle_string = pickle.load(outfile)
	outfile.close

	face_data = pickle.loads(pickle_string)
	[face_encodings, face_names] = face_data

	reference_face_image = face_recognition.load_image_file(image_file)
	reference_face_encoding = face_recognition.face_encodings(reference_face_image)
	#reference_face_encoding = face_encodings[8][0][:]
	#print(t.time())
	face_count = 0
	for face_encoding, face_name in zip(face_encodings, face_names):
		match = face_recognition.compare_faces(reference_face_encoding, face_encoding)
		for i in match:
			face_count+=1
			if (i):
				print (face_count, "Found Match!!!, Face ID:", face_name)

def compare_two_images(file_name_1, file_name_2):
	
	picture_of_me = face_recognition.load_image_file(file_name_1)
	my_face_encoding = face_recognition.face_encodings(picture_of_me)[0]

	# my_face_encoding now contains a universal 'encoding' of my facial features that can be compared to any other picture of a face!

	unknown_picture = face_recognition.load_image_file(file_name_2)
	unknown_face_encoding = face_recognition.face_encodings(unknown_picture)[0]

	# Now we can see the two face encodings are of the same person with `compare_faces`!

	results = face_recognition.compare_faces([my_face_encoding, unknown_face_encoding], unknown_face_encoding)
	return results

		
file_path = "images/"
save_file_name = "face_encodings_data.pkl"
#encode_jpg_images_and_save_face_encodings_to_file(file_path, save_file_name)
match_face_encodings_with_image(file_path+save_file_name, "images/abraham_06.jpg")
'''
file_name_1 = "images/abraham_01.jpg"
file_name_2 = "images/unknown_03.jpg"

result = compare_two_images(file_name_1, file_name_2)

print (result)
'''



