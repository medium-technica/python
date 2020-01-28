import cv2
import numpy as np
from matplotlib import pyplot as plt

img1 = cv2.imread('../images/messi.jpg',0)
img2 = img1[1:100,1:100];
cv2.imshow('Test',img2)
cv2.waitKey(0)
cv2.destroyAllWindows()

#plt.subplot(121),plt.imshow(img1,cmap = 'gray')
#plt.title('Original Image'), plt.xticks([]), plt.yticks([])
#plt.subplot(122),plt.imshow(img2,cmap = 'gray')
#plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

#plt.show()
