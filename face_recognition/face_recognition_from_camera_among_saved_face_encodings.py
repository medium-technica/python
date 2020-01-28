import face_recognition
import cv2
import paho.mqtt.client as mqtt
import pickle
import glob
import time as t

image = face_recognition.load_image_file("images/test/Aaron_Eckhart_0001.jpg")

file_path = "images/test/"
save_file_name = "face_encodings_data.pkl"
file_name_encodings = file_path+save_file_name

outfile = open(file_name_encodings, 'rb')
pickle_string = pickle.load(outfile)
outfile.close

saved_face_data = pickle.loads(pickle_string)
[saved_face_encodings, saved_face_names] = saved_face_data

camera_face_locations = []
camera_face_encodings = []
camera_face_names = []
process_this_frame = True

while True:
	frame = image
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
	camera_face_locations = face_recognition.face_locations(small_frame)
	
	if len(camera_face_locations):
		camera_face_encodings = face_recognition.face_encodings(small_frame, camera_face_locations)
		camera_face_names = []
		face_count = 0
		for camera_face_encoding in camera_face_encodings:
			match = face_recognition.compare_faces(saved_face_encodings, camera_face_encoding)
			for i in match:
				face_count+=1
				if (i):
					print (face_count, "Found Match!!!, Face ID:", saved_face_names[i])
		exit()
		'''
		for (top, right, bottom, left), name in zip(camera_face_locations, camera_face_names):
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
			break
		'''
# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
