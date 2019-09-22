"""
1) Преобразовать изображение из RGB в оттенки серого. Реализовать два варианта формулы с учетом разных вкладов R, G и B
в интенсивность (см презентацию). Затем найти разность полученных полутоновых изображений. Построить гистограммы
интенсивности после одного и второго преобразования.


image[i, j, k] = image1[i, j, k] - image2[i, j, k]

image before  image1[i,j]   image2[i,j]     image after
-1.0	    [160 160 160]   [160 160 160]	0.0
-1.0	    [158 158 158]   [159 159 159]	255.0


# image[i, j, k] = int(image1[i, j, k]) - int(image2[i, j, k])

image before  image1[i,j]   image2[i,j]     image after
-1.0	    [160 160 160]   [160 160 160]	0.0
-1.0	    [158 158 158]   [159 159 159]	-1.0
"""

import cv2
import numpy as np
from matplotlib import pyplot as plt
from timeit import default_timer as timer


def to_grayscale(image_old, method):
    image = image_old.copy()
    a = np.zeros(256)
    if method == 'NTSC':
        coefs = [0.114, 0.587, 0.299]
    elif method == 'sRGB':
        coefs = [0.0722, 0.7152, 0.2126]
    else:
        print('Wrong method!')
        return

    for i in range(len(image)):
        for j in range(len(image[0])):
            b = image[i, j, 0] * coefs[0]
            g = image[i, j, 1] * coefs[1]
            r = image[i, j, 2] * coefs[2]
            x = int(b + g + r)
            image[i, j] = x
            a[x] += 1
    return image, a


def images_difference(image1, image2):
    if image1.shape != image2.shape:
        print('Different sizes of images!')
        return

    image = np.ones(shape=image1.shape, dtype=int)
    for i in range(len(image)):
        for j in range(len(image[0])):
            for k in range(3):
                    image[i, j, k] = int(image2[i, j, k]) - int(image1[i, j, k])
    print(image)
    # find min and add it to each values
    min_value = image.min()
    print(min_value)
    if min_value < 0:
        for i in range(len(image)):
            for j in range(len(image[0])):
                for k in range(3):
                    x = image[i, j, k] - int(min_value)
                    if x > 255:
                        x = 255
                    image[i, j, k] = x
    min_value_after = image.min()
    print(min_value_after)
    print(image)
    
    return  np.uint8(image)


def main():
    image_name = 'ФРУКТЫ.jpg' #'test.jpg'
    image = cv2.imread(image_name)

    method = 'NTSC'
    windowName = 'To grayscale ' + method
    cv2.namedWindow(windowName)
    image_1, array_1 = to_grayscale(image, method)
    cv2.imshow(windowName, image_1)
    cv2.imwrite(image_name[0 : image_name.index('.')] + '_' + method + image_name[image_name.index('.'):], image_1)

    method = 'sRGB'
    windowName = 'To grayscale ' + method
    cv2.namedWindow(windowName)
    image_2, array_2 = to_grayscale(image, method)
    cv2.imshow(windowName, image_2)
    cv2.imwrite(image_name[0: image_name.index('.')] + '_' + method + image_name[image_name.index('.'):], image_2)

    method = 'difference'
    windowName = 'Difference'
    cv2.namedWindow(windowName)
    image_3 = images_difference(image_1, image_2)
    cv2.imshow(windowName, image_3)
    cv2.imwrite(image_name[0: image_name.index('.')] + '_' + method + image_name[image_name.index('.'):], image_3)

    # for plotting
    xs = range(256)
    plt.subplot(2, 1, 1)
    plt.plot(xs, array_1, color='black', fillstyle='bottom')
    plt.fill_between(xs, array_1, color='black')

    plt.subplot(2, 1, 2)
    plt.plot(xs, array_2, color='black', fillstyle='bottom')
    plt.fill_between(xs, array_2, color='black')
    plt.show()

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    start_time = timer()
    main()
    print("Total elapsed: {:g} secs".format(timer() - start_time))
