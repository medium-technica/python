import face_recognition
import numpy as np

# Load a sample picture and learn how to recognize it.
print("Loading known face image(s)")
image_01 = face_recognition.load_image_file("images/08.jpg")
image_01_face_encoding = face_recognition.face_encodings(image_01)[0]

# Initialize some variables
face_locations = []
face_encodings = []

# Find all the faces and face encodings in the current frame of video
output = face_recognition.load_image_file("images/09.jpg")
face_locations = face_recognition.face_locations(output)
print("Found {} faces in image.".format(len(face_locations)))
face_encodings = face_recognition.face_encodings(output, face_locations)

# Loop over each face found in the frame to see if it's someone we know.
for face_encoding in face_encodings:
	# See if the face is a match for the known face(s)
	match = face_recognition.compare_faces([image_01_face_encoding], face_encoding)
	name = "<Unknown Person>"

	if match[0]:
		name = "Abraham"

	print("I see someone named {}!".format(name))
