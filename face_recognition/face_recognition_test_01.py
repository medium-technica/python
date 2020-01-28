import face_recognition

# Load the jpg files into numpy arrays
image_1 = face_recognition.load_image_file('images/01.jpg')
image_2 = face_recognition.load_image_file('images/06.jpg')
image_unknown = face_recognition.load_image_file('images/03.jpg')

# Get the face encodings for each face in each image file
# Since there could be more than one face in each image, it returns a list of encodings.
# But since I know each image only has one face, I only care about the first encoding in each image, so I grab index 0.
image_1_face_encoding = face_recognition.face_encodings(image_1)[0]
image_2_face_encoding = face_recognition.face_encodings(image_2)[0]
unknown_face_encoding = face_recognition.face_encodings(image_unknown)[0]

known_faces = [
    image_1_face_encoding,
    image_2_face_encoding
]

# results is an array of True/False telling if the unknown face matched anyone in the known_faces array
results = face_recognition.compare_faces(known_faces, unknown_face_encoding)

print("Is the unknown face a picture of Image_1? {}".format(results[0]))
print("Is the unknown face a picture of Image_2? {}".format(results[1]))
print("Is the unknown face a new person that we've never seen before? {}".format(not True in results))
