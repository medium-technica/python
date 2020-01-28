import cv2
import numpy as np
import math
import scipy.misc

#img = cv2.imread('test.jpg')
file_name_image = 'test.jpg'


size = [4,4]
scale = [size[0]*100, size[1]*100];
size_of_room_grid = size[:]
size_of_square_probability_matrix = [size_of_room_grid[0] * 3, size_of_room_grid[1] * 3]

probability_matrix = [[10] * size_of_square_probability_matrix[0] for i in range(size_of_square_probability_matrix[1])]

nparray = np.asarray(probability_matrix)
ndarray = scipy.misc.imresize(nparray, scale, interp='nearest', mode=None)

while True:
	overlay = ndarray.copy()
	alpha = 0.5
	for r in [0, 100, 200, 300]:
		for c in [0, 100, 200, 300]:
			#cv2.rectangle(overlay, (0, 0), (100, 100),(255, 255, 255), 2)
			cv2.rectangle(overlay, (c, r), (c+100, r+100),(255, 255, 255), 2)
			if ((int((r/100)*4+(c/100))) > 9):
				c_1 = c+38
				r_1 = r+55
			else:
				c_1 = c+45
				r_1 = r+55
			cv2.putText(overlay, str(int((r/100)*4+(c/100))).format(alpha),(c_1, r_1), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

	# Display the resulting image
	cv2.imshow('Video', overlay)
	# Hit 'q' on the keyboard to quit!
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()
