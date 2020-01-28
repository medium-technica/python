import numpy as np
from sklearn.decomposition import PCA
from scipy import misc
import matplotlib.pyplot as plt

face = misc.imread('../images/abraham_03.jpg', flatten=True)
h, w = face.shape 
X = misc.imresize(face, [50,50], 'cubic')
pca = PCA()
pca.fit(X)
eigenface = pca.components_
print(eigenface)
#plt.imshow(eigenface, cmap=plt.cm.gray)
#plt.show()
