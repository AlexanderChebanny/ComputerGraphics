"""
Лысенко Н.С. 4.8

Лабораторная работа №2. Цветовые пространства. Преобразование цветовых пространств.

2) Выделить из полноцветного изображения один из каналов R, G, B  и вывести результат. Построить гистограмму по цветам.
"""

import numpy as np
from PIL import Image
from matplotlib import pyplot as plt


def out_one_of_rgb_channels(image_name, r_or_g_or_b):
    img = Image.open(image_name)
    arr = np.asarray(img, dtype='uint8')
    arr2 = arr.copy()

    if r_or_g_or_b == 'r':
        out = (1, 2)
    elif r_or_g_or_b == 'g':
        out = (0, 2)
    elif r_or_g_or_b == 'b':
        out = (0, 1)
    else:
        print('Wrong data!')
        return

    for i in range(len(arr)):
        for j in range(len(arr[i])):
            arr2[i][j][out[0]] = 0
            arr2[i][j][out[1]] = 0

    img = Image.fromarray(arr2)
    img.save('{}_{}.jpg'.format(image_name[0 : image_name.index('.')], r_or_g_or_b))
    return


def plot_hist_of_rgb(image_name):
    img = Image.open(image_name)
    arr = np.asarray(img, dtype='uint8')

    red, green, blue = 0, 0, 0

    for i in range(len(arr)):
        for j in range(len(arr[i])):
            red += arr[i][j][0]
            green += arr[i][j][1]
            blue += arr[i][j][2]

    print('red \t: {}'.format(red))
    print('green \t: {}'.format(green))
    print('blue \t: {}'.format(blue))

    fig, ax = plt.subplots()
    ax.bar(1, red, color='red')
    ax.bar(2, green, color='green')
    ax.bar(3, blue, color='blue')

    fig.set_figwidth(12)  # ширина Figure
    fig.set_figheight(6)  # высота Figure
    plt.show()


name = 'aaa.jpg'
# out_one_of_rgb_channels(name, 'b')
plot_hist_of_rgb(name)
