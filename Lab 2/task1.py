"""
1) Преобразовать изображение из RGB в оттенки серого. Реализовать два варианта формулы с учетом разных вкладов R, G и B
в интенсивность (см презентацию). Затем найти разность полученных полутоновых изображений. Построить гистограммы
интенсивности после одного и второго преобразования.
"""

import cv2
import numpy as np
from matplotlib import pyplot as plt


def to_NTSC(image_old):
    """
    NTSC яркость
    """
    image = image_old.copy()
    a = [0] * 256
    for i in range(len(image)):
        for j in range(len(image[0])):
            b = image[i, j,0] * 0.114
            g = image[i, j,1] * 0.587
            r = image[i, j,2] * 0.299
            image[i, j] = [(b + g + r)/3]
            a[image[i, j]] += 1
    return image, a


def to_sRGB(image_old):
    """
    HDTV модель, sRGB яркость
    """
    image = image_old.copy()
    a = [0] * 256
    for i in range(len(image)):
        for j in range(len(image[0])):
            b = image[i, j,0] * 0.0722
            g = image[i, j,1] * 0.7152
            r = image[i, j,2] * 0.2126
            image[i, j] = [(b + g + r) / 3]
            a[image[i, j, 0]] += 1
    return image, a


def images_difference(image1, image2):
    if image1.shape != image2.shape:
        print('Different images size!')
        return
    image = image1.copy()
    for i in range(len(image)):
        for j in range(len(image[0])):
            # image[i, j] = max(0, image1[i, j] - image2[i, j])
            image[i, j, 0] = abs(image1[i, j] - image2[i, j])
    return image


image = cv2.imread('test.jpg')

windowName_1 = 'To grayscale NTSC'
#cv2.namedWindow(windowName_1)
image_1, array_1 = to_NTSC(image)
print(image_1)
#cv2.imshow(windowName_1, image_1)
'''
windowName_2 = 'To grayscale sRGB'
cv2.namedWindow(windowName_2)
image_2, array_2 = to_sRGB(image)
cv2.imshow(windowName_2, image_2)

windowName_3 = 'Difference'
cv2.namedWindow(windowName_3)
image_3 = images_difference(image_1, image_2)
cv2.imshow(windowName_3, image_3)
'''
# for plotting
xs = range(256)
#plt.subplot(2, 1, 1)
plt.plot(xs, array_1[0], color='b', fillstyle='bottom')
plt.fill_between(xs, array_1, color='b')
#
# plt.subplot(2, 1, 2)
# plt.plot(xs, array_2[0], color='b', fillstyle='bottom')
# plt.fill_between(xs, array_2, color='b')

plt.show()

cv2.waitKey(0)
cv2.destroyAllWindows()
