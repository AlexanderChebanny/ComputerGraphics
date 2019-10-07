import sys
import cv2
import numpy as np
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton
from PyQt5.QtGui import QPixmap, QPainter, QPen, QImage

def white(pxl):
    return pxl[0] == 255 and pxl[1] == 255 and pxl[2] == 255

def findfirstx(img, xx, yy):
    if len(img) == 0 and len(img[0]) == 0:
        print('Wrong image size')
        return -1
        
    for j in range(xx, len(img[0])):
        if not white(img[yy][j]):
            return j
            

def nearpix(direc, x, y):
    if direc == 0:
        return x + 1, y
    elif direc == 1:
        return x + 1, y - 1
    elif direc == 2:
        return x, y - 1
    elif direc == 3:
        return x - 1, y - 1
    elif direc == 4:
        return x - 1, y
    elif direc == 5:
        return x - 1, y + 1
    elif direc == 6:
        return x, y + 1
    elif direc == 7:
        return x + 1, y + 1

def bp1(img, x, y):
    return white(img[y - 1][x]) or white(img[y + 1][x]) or white(img[y][x - 1]) or white(img[y][x + 1])

def bp2(img, x, y):
    return bp1(img, x, y) or white(img[y - 1][x - 1]) or white(img[y - 1][x + 1]) or white(img[y + 1][x - 1]) or white(img[y + 1][x + 1])

def findbound(img, xx, yy):
    '''
    ————>x
    |
    |
    v
    y
    '''
    '''
    3 2 1
    4 X 0
    5 6 7
    '''
    y = yy
    x = findfirstx(img, xx, yy)
    direc = 6
    bnd = set()
    while not ((x, y) in bnd):
        bnd.add((x, y))
        for i in range(8):
            d = (direc - i + 8) % 8
            xn, yn = nearpix(d, x, y)
            if not white(img[yn][xn]) and not ((xn, yn) in bnd) and bp1(img, xn, yn):
                x = xn
                y = yn
                direc = d
                break
              
    for el in bnd:
        (x, y) = el
        img[y][x] = [0, 0, 255]

    return img

size = 1000
    
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
        img = findbound(gbr, self.xx, self.yy)
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