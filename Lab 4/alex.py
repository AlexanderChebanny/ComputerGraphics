from lab4 import *
from tkinter import *
import numpy as np
from PIL import Image, ImageTk, ImageDraw


'''
АФИННЫЕ ПРЕОБРАЗОВАНИЯ К ПОЛИГОНАМ
'''


# поворот для набора точек
def rotate_basic(points, angle):
    rot = np.array([[cos(angle), sin(angle), 0], [-sin(angle), cos(angle), 0], [0, 0, 1]])
    for i in range(len(points)):
        x = points[i]
        x.append(1)
        prod = np.matmul(x, rot)
        points[i] = list(prod[:2])
    return points


# перемещение для набора точек
def offset(points, dx, dy):
    off = np.array([[1, 0, 0], [0, 1, 0], [dx, dy, 1]])
    for i in range(len(points)):
        x = points[i]
        x.append(1)
        prod = np.matmul(x, off)
        points[i] = list(prod[:2])
    return points


# поиск барицентра n-угольника
def barycenter(points):
    xb = 0
    yb = 0
    c = 0
    for el in points:
        c += 1
        xb += el[0]
        yb += el[1]
    xb /= c
    yb /= c
    return [xb, yb, 1]


# поворот для набора точек относительно заданной точки
def rotatep(points, angle, x, y):
    return offset(rotate_basic(offset(points, -x, -y), angle), x, y)


# поворот для набора точек относительно центра n-угольника
def rotatec(points, angle):
    center = barycenter(points)
    return rotatep(points, angle, center[0], center[1])


# масштабирование для набора точек относительно заданной точки
def scalep(points, scale, x, y):
    sc = offset(points, -x, -y)
    sc = np.multiply(sc, scale)
    sc = [list(x) for x in sc]
    sc = offset(sc, x, y)
    return sc


# масштабирование для набора точек относительно центра
def scalec(points, scale):
    center = barycenter(points)
    return scalep(points, scale, center[0], center[1])


'''
РАБОТА С РЕБРАМИ
'''


# поворот ребра на 90 градусов
def rotate_edge(x1, y1, x2, y2):
    return rotatec([[x1, y1, 1],[x2, y2, 1]], np.pi/2)


# пересечение отрезков
def line(p1, p2):
    A = (p1[1] - p2[1])
    B = (p2[0] - p1[0])
    C = (p1[0]*p2[1] - p2[0]*p1[1])
    return A, B, -C


def intersection(p1, p2, p3, p4):
    l1 = line(p1, p2)
    l2 = line(p3, p4)
    D  = l1[0] * l2[1] - l1[1] * l2[0]
    Dx = l1[2] * l2[1] - l1[1] * l2[2]
    Dy = l1[0] * l2[2] - l1[2] * l2[0]
    mx1 = max(p1[0], p2[0])
    nx1 = min(p1[0], p2[0])
    my1 = max(p1[1], p2[1])
    ny1 = min(p1[1], p2[1])
    mx2 = max(p3[0], p4[0])
    nx2 = min(p3[0], p4[0])
    my2 = max(p3[1], p4[1])
    ny2 = min(p3[1], p4[1])
    f1 = max(nx1, nx2)
    f2 = min(mx1, mx2)
    f3 = max(ny1, ny2)
    f4 = min(my1, my2)
    if D != 0:
        x = Dx / D
        y = Dy / D
        if x >= f1 and x <= f2 and y >= f3 and y <= f4:
            return [x, y]
    return []


'''
ПРОВЕРКИ
'''


# определение положения точки относительно ребра
def findside(p1, p2, x, y):

    xa = p2[0] - p1[0]
    ya = p2[1] - p1[1]
    x -= p1[0]
    y -= p1[1]
    if y*xa - x*ya > 0:
        return True
    else:
        return False


# принадлежит ли точка выпуклому многоугольнику

def belongs(points, x, y):
    for i in range(len(points) - 1):
        if not findside(points[i], points[i+1], x, y):
            return False
    return True


# принадлежит ли точка невыпуклому многоугольнику
def belongsnon(points, x, y):
    c = 0
    c1 = 0
    for i in range(len(points) - 1):
        if intersection(points[i], points[i+1], [x, y], [x + 100000, y]) != []:
            c += 1
            if points[i][0] == x:
                c1 += 1

    res = c - c1
    if res % 2 == 0:
        return False
    else:
        return True


class Gui:
    CANVAS_WIDTH = 1000
    CANVAS_HEIGHT = 1000

    def __init__(self):
        self.window = Tk()
        self.full_figure = False
        # point
        self.point = False
        self.point_x = 0
        self.point_y = 0
        self.window.title("MECHMAT SILA")
        self.window.resizable(False, False)
        # current figure
        self.points = []
        # canvas
        self.canvas = Canvas(self.window, width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT-200, background='white')
        self.canvas.grid(row=0, column=0)
        # mouse clicks
        self.canvas.bind("<ButtonRelease-1>", self.left_button_release)
        self.canvas.bind("<ButtonRelease-2>", self.middle_button_release)
        self.canvas.bind("<ButtonRelease-3>", self.right_button_release)

        # clear button
        self.clear_button = Button(self.window, text='Clear', command=self.clear_window)
        self.clear_button.grid(row=2, column=1)

        Label(self.window, text="x: ").grid(row=2, column=2)
        Label(self.window, text="y: ").grid(row=3, column=2)
        Label(self.window, text="angle: ").grid(row=2, column=4)
        Label(self.window, text="scale: ").grid(row=3, column=4)
        self.x_input_box = Entry(self.window)
        self.y_input_box = Entry(self.window)
        self.x_input_box.insert(0, "100")
        self.y_input_box.insert(0, "100")
        self.x_input_box.grid(row=2, column=3)
        self.y_input_box.grid(row=3, column=3)

        self.angle_input_box = Entry(self.window)
        self.angle_input_box.insert(0, "180")
        self.angle_input_box.grid(row=2, column=5)

        self.scale_input_box = Entry(self.window)
        self.scale_input_box.insert(0, "2")
        self.scale_input_box.grid(row=3, column=5)

        self.shift_button = Button(self.window, text='Shift', command=self.shift)
        self.shift_button.grid(row=3, column=1)

        self.shift_button = Button(self.window, text='Point Rotate', command=self.point_rotate)
        self.shift_button.grid(row=4, column=1)

        self.shift_button = Button(self.window, text='Rotate', command=self.rotate)
        self.shift_button.grid(row=5, column=1)

        self.shift_button = Button(self.window, text='Point Scale', command=self.point_scale)
        self.shift_button.grid(row=4, column=2)

        self.shift_button = Button(self.window, text='Scale', command=self.scale)
        self.shift_button.grid(row=5, column=2)

        self.shift_button = Button(self.window, text='Segment Rotate 90', command=self.segment_rotate_90)
        self.shift_button.grid(row=1, column=3)

        self.shift_button = Button(self.window, text='Segments Intersection', command=self.segments_intersection)
        self.shift_button.grid(row=1, column=4)


        self.shift_button = Button(self.window, text='In Convex Polygon', command=self.in_convex_polygon)
        self.shift_button.grid(row=0, column=1)

        self.shift_button = Button(self.window, text='In Concave Polygon', command=self.in_concave_polygon)
        self.shift_button.grid(row=0, column=3)

        self.shift_button = Button(self.window, text='Point Position', command=self.point_position)
        self.shift_button.grid(row=4, column=3)


        self.window.mainloop()

    def clear_window(self):
        self.canvas.delete("all")
        self.full_figure = False
        self.points = []
        #self.image = Image.new('RGB', (self.DEFAULT_WIDTH, self.DEFAULT_WIDTH), 'white')
        #self.draw = ImageDraw.Draw(self.image)

    def left_button_release(self, event):
        x, y = event.x, event.y
        if self.points == []:
            self.points.append([x, y])
            self.canvas.create_oval(x,y,x-1,y-1)
        else:
            x0, y0 = self.points[-1]
            self.canvas.create_line(x0,y0,x,y)
            self.points.append([x, y])

    def middle_button_release(self, event):
        if self.point:
            self.point = False
            self.polygon()
        self.point = True
        x, y = event.x, event.y
        self.point_x = x
        self.point_y = y
        self.canvas.create_oval(x+1,y+1,x-1,y-1, fill="green")

    def right_button_release(self, event):
        if self.full_figure:
            1
        else:
            if len(self.points) > 2:
                x0, y0 = self.points[-1]
                x, y = self.points[0]
                self.canvas.create_line(x0,y0,x,y)
                self.full_figure = True

    def polygon(self):
        self.canvas.delete("all")
        if self.point:
            x, y = self.point_x, self.point_y
            self.canvas.create_oval(x+1,y+1,x-1,y-1, fill="green")
        if len(self.points) == 1:
            x, y = self.points[0]
            self.canvas.create_oval(x,y,x-1,y-1)
        else:
            l = len(self.points)
            for i in range(0, len(self.points)):
                x, y = self.points[i]
                x0, y0 = self.points[(i - 1) % l]
                self.canvas.create_line(x0,y0,x,y)

    def shift(self):
        if self.points != []:
            self.points = offset(self.points, int(self.x_input_box.get()), int(self.y_input_box.get()))
            self.polygon()

    def point_rotate(self):
        if self.point and self.points != []:
            self.points = rotatep(self.points, np.pi / 180 * int(self.angle_input_box.get()), self.point_x, self.point_y)
            self.polygon()

    def rotate(self):
        if self.points != []:
            self.points = rotatec(self.points, np.pi / 180 * int(self.angle_input_box.get()))
            self.polygon()

    def point_scale(self):
        if self.point and self.points != []:
            self.points = scalep(self.points, float(self.scale_input_box.get()), self.point_x, self.point_y)
            self.polygon()

    def scale(self):
        if self.points != []:
            self.points = scalec(self.points, float(self.scale_input_box.get()))
            self.polygon()

    def segment_rotate_90(self):
        if len(self.points) == 2:
            self.points = rotatec(self.points, np.pi / 2)
            self.polygon()

    def segments_intersection(self):
        if len(self.points) == 4:
            p1, p2, p3, p4 = self.points
            #print(p1, p2, p3, p4)
            res = intersection( p1, p2, p3, p4)
            if res != []:
                x, y = res
                Label(self.window, text="x: " + str(round(x,2)) + "; y: "+ str(round(y,2))).grid(row=1, column=5)
            else:
                Label(self.window, text="No intersection").grid(row=1, column=5)
        else:
            Label(self.window, text="Draw Valid Two Segments").grid(row=1, column=5)

    def in_convex_polygon(self):
        print(belongs(self.points, self.point_x, self.point_y))
        if self.full_figure:
            if belongs(self.points, self.point_x, self.point_y):
                Label(self.window, text="True").grid(row=0, column=2)
            else:
                Label(self.window, text="False").grid(row=0, column=2)
        else:
            Label(self.window, text="Draw A Valid Convex Polygon").grid(row=0, column=2)

    def in_concave_polygon(self):
        if self.full_figure:
            if belongsnon(self.points, self.point_x, self.point_y):
                Label(self.window, text="True").grid(row=0, column=4)
            else:
                Label(self.window, text="False").grid(row=0, column=4)
        else:
            Label(self.window, text="Draw A Valid Concave Polygon").grid(row=0, column=4)

    def point_position(self):
        if len(self.points) == 2:
            print(self.points)
            print(self.point_x, self.point_y)
            if findside(self.points[0], self.points[1], self.point_x, self.point_y):
                Label(self.window, text="Right").grid(row=4, column=4)
            else:
                Label(self.window, text="Left").grid(row=4, column=4)
        else:
            Label(self.window, text="Draw A Valid Segment").grid(row=4, column=4)


if __name__ == '__main__':
    Gui()
