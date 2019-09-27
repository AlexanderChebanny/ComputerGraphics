"""
Лысенко Н. С.

Лабораторная работа №3. Растровые алгоритмы
Работа в командах.

Задание 1. Рекурсивный алгоритм заливки на основе серий пикселов (линий).

1а) Заливка заданным цветом.
"""

import sys
import cv2
import numpy as np
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton
from PyQt5.QtGui import QPixmap, QPainter, QPen, QImage
import queue


# find left border for current x and y
def left_border(img, x, y):
    left = 1
    x_left = x
    while 1 < x_left:
        x_left -= 1
        # print('x = {}, y = {}, {}'.format(x_left, y, img[y, x_left]))
        if int(img[y, x_left, 0]) == 0:
            left = x_left
            break
    return left


# find right border for current x and y
def right_border(img, x, y):
    right = 299
    x_right = x
    while x_right < 299:
        x_right += 1
        # print('x = {}, y = {}, {}'.format(x_right, y, img[y, x_right]))
        if int(img[y, x_right, 0]) == 0:
            right = x_right
            break
    return right


# draw lines with queue
def draw_line_q(img, q):
    while not q.empty():
        cur = q.get()
        x = cur[0]
        y = cur[1]
        if img[y, x, 0] == 255 and img[y, x, 1] == 255 and img[y, x, 2] == 255:
            left = left_border(img, x, y)
            right = right_border(img, x, y)
            cv2.line(img, (left + 1, y), (right - 1, y), (255, 0, 0), 1)
            cv2.imwrite('lol.png', img)
            for i in range(left, right + 1):
                q.put((i, y - 1))
                q.put((i, y + 1))


# main function for filling
def fill_lines(img, x, y):
    q = queue.Queue()
    q.put((x, y))
    draw_line_q(img, q)
    cv2.rectangle(img, (x, y), (x + 1, y + 1), (0, 0, 255), 2)
    cv2.imwrite('lol.png', img)


# img
gbr = []

class Menu(QMainWindow):
    xx = -1
    yy = -1

    def __init__(self):
        super().__init__()
        self.drawing = False
        self.lastPoint = QPoint()
        # self.image = QPixmap("white.png")
        self.title = 'Filling'
        self.setGeometry(100, 100, 300, 100)

        blank_image2 = 255 * np.ones(shape=[300, 300, 3], dtype=np.uint8)
        self.image = QPixmap.fromImage(
            QImage(blank_image2, blank_image2.shape[1], blank_image2.shape[0], blank_image2.strides[0],
                   QImage.Format_RGB888))
        self.resize(self.image.width(), self.image.height())
        self.initUI()
        self.show()

    def initUI(self):
        self.setWindowTitle(self.title)
        button = QPushButton('Clear', self)
        button.clicked.connect(self.on_click1) #on_click1)
        button1 = QPushButton('Fill', self)
        button1.move(0, 30)
        button1.clicked.connect(self.on_click2)

    def on_click1(self):
        self.image = QPixmap("white.png")
        self.show()

    def on_click2(self):
        self.image.save("new.png")
        gbr = cv2.imread("new.png")
        print(gbr.shape)
        fill_lines(gbr, self.xx, self.yy)
        cv2.imshow('Result', gbr)

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
            painter.setPen(QPen(Qt.black, 5, Qt.SolidLine))
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
