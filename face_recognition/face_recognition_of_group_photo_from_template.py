import face_recognition
import numpy as np
import cv2
from matplotlib import pyplot as plt

print("Loading face image(s)")
template_image = face_recognition.load_image_file("images/abraham_01.jpg")
template_image_face_encoding = face_recognition.face_encodings(template_image)[0]
test_image = face_recognition.load_image_file("images/abraham_05.jpg")
output = test_image.copy()

# Initialize some variables
face_locations = []
face_encodings = []

face_locations = face_recognition.face_locations(test_image)
face_encodings = face_recognition.face_encodings(test_image, face_locations)
face_names = []
for face_encoding in face_encodings:
	match = face_recognition.compare_faces([template_image_face_encoding], face_encoding)
	name = "Unknown"
	if (match[0]):
		name = "Abraham"
	face_names.append(name)
	for (top, right, bottom, left), name in zip(face_locations, face_names):
		# Draw a box around the face
		cv2.rectangle(output, (left, top), (right, bottom), (0, 0, 255), 2)
		# Draw a label with a name below the face
		cv2.rectangle(output, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
		font = cv2.FONT_HERSHEY_DUPLEX
		cv2.putText(output, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
plt.imshow(output)
plt.show()

