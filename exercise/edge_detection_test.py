import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2

#imgplot = plt.imshow(img)
#plt.colorbar()
#plt.show()

#nparray = np.asarray(array_2d)

#cap = cv2.VideoCapture(0)

img = mpimg.imread('images/01.jpg')

while(1):
  frame = img
  gray_vid = cv2.cvtColor(frame, cv2.IMREAD_GRAYSCALE)
  cv2.imshow('Original',frame)
  edged_frame = cv2.Canny(frame,100,200)
  cv2.imshow('Edges',edged_frame)
#cap.release()
cv2.destroyAllWindows()
