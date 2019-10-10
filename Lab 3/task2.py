"""
Замай Антон 4.8

Лабораторная работа №3. Растровые алгоритмы
Работа в командах.

    Задание 2. Выделение границы связной области.

    На вход подается изображение. Граница связной области задается одним цветом. Имея начальную точку границы
    организовать ее обход, занося точки в список в порядке обхода.
    Начальную точку границы можно получать любым способом.
    Для контроля полученную границу прорисовать поверх исходного изображения.
"""

import sys
import cv2
import numpy as np
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton
from PyQt5.QtGui import QPixmap, QPainter, QPen, QImage


def eq(pix1, pix2):
    return pix1[0] == pix2[0] and pix1[1] == pix2[1] and pix1[2] == pix2[2]


def findfirstx(img, xx, yy, bnd_clr):
    if len(img) == 0 and len(img[0]) == 0:
        print('Wrong image size')
        return -1

    for j in range(xx, len(img[0])):
        if eq(img[yy][j], bnd_clr):
            return j


def nextclw(curp, backp):
    dif = (backp[0] - curp[0], backp[1] - curp[1])
    clw = [(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)]
    offset = clw[(clw.index(dif) + 1) % len(clw)]
    newp = (curp[0] + offset[0], curp[1] + offset[1])
    return newp


def findbound(img, xx, yy, bnd_clr):
    y = yy
    x = findfirstx(img, xx, yy, bnd_clr)
    startp = (x, y)
    bnd = []
    backp = (x - 1, y)
    bndp = (x, y)
    curp = nextclw(bndp, backp)
    while curp != startp:
        if eq(img[curp[1]][curp[0]], bnd_clr):
            bnd.append(curp)
            backp = bndp
            bndp = curp
            curp = nextclw(bndp, backp)
        else:
            backp = curp
            curp = nextclw(bndp, backp)
    print(bnd)
    for el in bnd:
        (x, y) = el
        img[y][x] = [0, 0, 255]

    return img


size = 500
    
# start pixel

# img
gbr = []


class Menu(QMainWindow):
    xx = -1
    yy = -1

    def __init__(self):
        super().__init__()
        self.drawing = False
        self.lastPoint = QPoint()
        self.image = QPixmap("white.png")
        blank_image2 = 255 * np.ones(shape=[size, size, 3], dtype=np.uint8)
        self.image = QPixmap.fromImage(QImage(blank_image2, blank_image2.shape[1], blank_image2.shape[0],
                                              blank_image2.strides[0], QImage.Format_RGB888))
        self.title = 'Find bounds algo'
        self.setGeometry(100, 100, size, size)
        self.resize(self.image.width(), self.image.height())
        self.initUI()
        self.show()
            
    def initUI(self):
        self.setWindowTitle(self.title)
        button = QPushButton('Clear', self)
        button.clicked.connect(self.on_click1)
        button1 = QPushButton('Go', self)
        button1.move(0,30)
        button1.clicked.connect(self.on_click2)

    def on_click1(self):
        # self.image = QPixmap("white.png")
        blank_image2 = 255 * np.ones(shape=[size, size, 3], dtype=np.uint8)
        self.image = QPixmap.fromImage(QImage(blank_image2, blank_image2.shape[1], blank_image2.shape[0],
                                              blank_image2.strides[0], QImage.Format_RGB888))
        self.repaint()
        self.show()
        
    def on_click2(self):
        self.image.save("toalgo.png") 
        gbr = cv2.imread("toalgo.png")
        img = findbound(gbr, self.xx, self.yy, [255, 0, 0])
        # cv2.imshow('Result', gbr)
        cv2.imwrite('task2.png', img)
        self.image = QPixmap("task2.png")
        self.repaint()
        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.image)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos()
        if event.button() == Qt.RightButton:
            self.yy = event.pos().y()
            self.xx = event.pos().x()

    def mouseMoveEvent(self, event):
        if event.buttons() and Qt.LeftButton and self.drawing:
            painter = QPainter(self.image)
            painter.setPen(QPen(Qt.blue, 4, Qt.SolidLine))
            painter.drawLine(self.lastPoint, event.pos())
            self.lastPoint = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button == Qt.LeftButton:
            self.drawing = False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainMenu = Menu()
    sys.exit(app.exec_())
