from PIL import Image
import numpy as np
import random


w, h = 512, 512
data = np.zeros((h, w, 3), dtype=np.uint8)
for x in range(w):
	for y in range(h):
		data[x,y] = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]

img = Image.fromarray(data, 'RGB')
img.save('my.png')
img.show()
