import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread("../images/rgb_colors.jpg", cv2.CV_LOAD_IMAGE_COLOR)
img = cv2.resize(img,None,fx=1, fy=1, interpolation = cv2.INTER_CUBIC)
r,g,b = cv2.split(img)
cv2.imshow('Window Title',b)
cv2.waitKey(0)
cv2.destroyAllWindows()
