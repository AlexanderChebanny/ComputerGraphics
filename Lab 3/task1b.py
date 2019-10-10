"""
Чебанный Александр 4.8

Лабораторная работа №3. Растровые алгоритмы
Работа в командах.

    Задание 1. Рекурсивный алгоритм заливки на основе серий пикселов (линий).

    1б) Заливка рисунком из графического файла. Файл можно загрузить встроенными средствами и затем считывать
    точки изображения для использования в заливке.
    Область рисуется мышкой. Область произвольной формы. Внутри могут быть отверстия. Точка, с которой начинается
    заливка, задается щелчком мыши.
"""


import sys
import cv2
import queue
from collections import deque
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton
from PyQt5.QtGui import QPixmap, QPainter, QPen


def compare_color(cl, b, g, r):
    return cl[0] == b and cl[1] == g and cl[2] == r


def drawarea(img, bck, x, y):
    yb, xb, _ = bck.shape
    yb1, xb1, _ = img.shape
    print(yb1, xb1)
    xc = xb // 2
    yc = yb // 2
    ycc = y
    q = queue.Queue()
    b, g, r = img[y][x]
    q.put((x, y, xc, yc))
    while not q.empty():
        x1, y1, xc, yc = q.get()
        if not (y1 >= 0 and y1 < yb1 and x1 >= 0 and x1 < xb1) or not compare_color(img[y1][x1], b, g, r):
            continue
        x2 = x1
        xc1 = xc
        top = deque()
        bot = deque()
        while y1 >= 0 and y1 < yb1 and x1 >= 0 and x1 < xb1 and compare_color(img[y1][x1], b, g, r):
            #print(type(img[y1][x1]))
            #print(bck[yc % yb][xc % xb])
            img[y1][x1] = bck[yc % yb][xc % xb]
            if y1 < yb1 - 1 and compare_color(img[y1 + 1][x1], b, g, r):
                top.appendleft((x1, y1 + 1, xc, yc + 1))
            if y1 >= 1 and compare_color(img[y1 - 1][x1], b, g, r):
                bot.appendleft((x1, y1 - 1, xc, yc - 1))
            x1 -= 1
            xc -= 1
        x1 = x2 + 1
        xc = xc1 + 1
        count = 0
        while y1 >= 0 and y1 < yb1 and x1 >= 0 and x1 < xb1 and compare_color(img[y1][x1], b, g, r):
            img[y1][x1] = bck[yc % yb][xc % xb]
            if y1 >= 1 and compare_color(img[y1 - 1][x1], b, g, r):
                bot.append((x1, y1 - 1, xc, yc - 1))
            if y1 < yb1 - 1 and compare_color(img[y1 + 1][x1], b, g, r):
                top.append((x1, y1 + 1, xc, yc + 1))
            x1 += 1
            xc += 1
        for x in top:
            q.put(x)
        for x in bot:
            q.put(x)
    return img


class Menu(QMainWindow):
    xc, yc = -1, -1
    xx, yy = -1, -1

    def __init__(self):
        super().__init__()
        self.drawing = False
        self.lastPoint = QPoint()
        self.image = QPixmap(500, 500)  # ("white.png")
        self.title = 'Fill'
        self.setGeometry(0, 0, 500, 500)
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
        self.image = QPixmap(500, 500)
        self.repaint()
        self.show()
        
    def on_click2(self):
        self.image.save("toalgo.png") 
        gbr = cv2.imread("toalgo.png")
        bground = cv2.imread("back.jpeg")

        img = drawarea(gbr, bground, self.xx, self.yy)

        cv2.imwrite('tyan.png', img)
        self.image = QPixmap("tyan.png")
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
            painter.setPen(QPen(Qt.white, 3, Qt.SolidLine))
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
