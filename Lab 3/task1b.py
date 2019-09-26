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
    xc = xb // 2
    yc = yb // 2
    ycc = y
    q = queue.Queue()
    b, g, r = img[y][x]
    q.put((x, y, xc, yc))
    while not q.empty():
        x1, y1, xc, yc = q.get()
        if not compare_color(img[y1][x1], b, g, r):
            continue
        x2 = x1
        xc1 = xc
        top = deque()
        bot = deque()
        while compare_color(img[y1][x1], b, g, r):
            #print(type(img[y1][x1]))
            print(bck[yc % yb][xc % xb])
            img[y1][x1] = bck[yc % yb][xc % xb]
            if compare_color(img[y1 + 1][x1], b, g, r):
                top.appendleft((x1, y1 + 1, xc, yc + 1))
            if compare_color(img[y1 - 1][x1], b, g, r):
                bot.appendleft((x1, y1 - 1, xc, yc - 1))
            x1 -= 1
            xc -= 1
        x1 = x2 + 1
        xc = xc1 + 1
        count = 0
        while compare_color(img[y1][x1], b, g, r):
            img[y1][x1] = bck[yc % yb][xc % xb]
            if compare_color(img[y1 - 1][x1], b, g, r):
                bot.append((x1, y1 - 1, xc, yc - 1))
            if compare_color(img[y1 + 1][x1], b, g, r):
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
        self.image = QPixmap(1100, 1000)#("white.png")
        self.title = 'Fill'
        self.setGeometry(0, 0, 1200, 1200)
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
        self.image = QPixmap(1000, 1000)
        self.show()
        
    def on_click2(self):
        self.image.save("toalgo.png") 
        gbr = cv2.imread("toalgo.png")
        bground = cv2.imread("back.jpeg")
        drawarea(gbr, bground, self.xx, self.yy)
        cv2.imshow('[eq', gbr)
        
        
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
