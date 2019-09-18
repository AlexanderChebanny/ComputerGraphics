import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('test.jpg')

x, y, z = img.shape

print(x, y, z)

a = np.zeros(shape=(3,256))
xs = range(256)

for i in range(x):
    for j in range(y):
        for k in range(3):
            a[k][img[i, j, k]] += 1

names = {0:'Blue', 1:'Green', 2:'Red'} 
short_names = {0:'b', 1:'g', 2:'r'}
for i in range(3):
    plt.subplot(3, 1, i + 1)
    plt.plot(xs, a[i], color=short_names[i], fillstyle='bottom')
    plt.fill_between(xs, a[i], color=short_names[i])
    #plt.title(names[i])

plt.show()

img[:,:,:2] = 0
cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
