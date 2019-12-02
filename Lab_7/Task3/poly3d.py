import math as m
import numpy as np

#   Константы
EPS = 0.000001


# Класс точка
class P(object):

    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, p):
        if type(p) == int:
            return P(self.x + p, self.y + p, self.z + p)
        elif type(p) == P:
            return P(self.x + p.x, self.y + p.y, self.z + p.z)

    def __sub__(self, p):
        return P(self.x - p.x, self.y - p.y, self.z - p.z)

    def __mul__(self, p):
        return P(self.x * p.x, self.y * p.y, self.z * p.z)

    def __floordiv__(self, p):
        try:
            return P(self.x // p.x, self.y // p.y, self.z // p.z)
        except:
            return "Dividing by zero"

    def __eq__(self, p):
        return (self.x - p.x) < EPS and (self.y - p.y) < EPS and (self.z - p.z) < EPS

    def __ne__(self, p):
        return not self == p

    def __str__(self):
        return "(%s, %s, %s)" % (self.x, self.y, self.z)

    def __repr__(self):
        return "(%s, %s, %s)" % (self.x, self.y, self.z)


# Класс линия
class L(object):

    def __init__(self, p1=P(), p2=P()):
        self.x1 = p1.x
        self.y1 = p1.y
        self.z1 = p1.z
        self.x2 = p2.x
        self.y2 = p2.y
        self.z2 = p2.z


# Класс многоугольник
class N_edge(object):

    # Конструктор
    def __init__(self, points=[], edges=[], worldcoor=False):

        # Множество точек многогранника
        self._points = points
        # Множество ребер многогранника
        self._edges = edges
        # Находится ли центр в точке (0, 0, 0). Влияет на то, нужны ли сдвиги пространства
        # в центр многогранника в некоторых время преобразований
        self._worldcoor = worldcoor
        if self._points != []:
            self.center()

    # Возвращает тип координат
    def typecoor(self):
        return self._worldcoor

    # Чтение из файла
    '''
    Формат файла имеет вид:

    x y z типа float - координаты точек
    ...
    i j  типа int - ребра, т.е. пары индексов вершин (индексы счита ются по мере считывания файла от 0)
    ...
    True/False - находится ли центр в (0, 0, 0) (False - находится)
    '''

    def fileread(self, filename):
        self._points = []
        self._edges = []
        f = open(filename, 'r')
        for line in f:
            pline = line.split(' ')
            if len(pline) == 3:
                self._points.append(P(float(pline[0]), float(pline[1]), float(pline[2])))
            if len(pline) == 2:
                self._edges.append([int(pline[0]), int(pline[1])])
            if len(pline) == 1:
                self._worldcoor = bool(pline[0])
        f.close()
        if self._points != []:
            self.center()
        return self

    # Сохранение в файл
    def filesave(self, filename):
        f = open(filename, 'w')
        for p in self._points:
            f.write(str(p.x) + ' ' + str(p.y) + ' ' + str(p.z))
        for e in self._edges:
            f.write(str(e[0]) + ' ' + str(e[1]))
        f.write(str(False))
        f.close()
        return self

    # Считает центр и возвращает его
    def center(self):
        x = y = z = 0
        for p in self._points:
            x += p.x
            y += p.y
            z += p.z
        self._center = P(x / len(self._points), y / len(self._points), z / len(self._points))
        return self._center

    # Переносит центр
    def setcenter(self, x=0, y=0, z=0):
        x -= self._center.x
        y -= self._center.y
        z -= self._center.z
        addp = P(x, y, z)
        newpoints = []
        for p in self._points:
            newpoints.append(p + addp)
        self._points = newpoints
        self.center()
        if P(x, y, z) != P():
            self._worldcoor = True
        return self

    # Устанавливает центр в точке (0, 0, 0)
    def returnCtoZ(self):
        x = self._center.x
        y = self._center.y
        z = self._center.z
        newpoints = []
        addp = P(x, y, z)
        for p in self._points:
            newpoints.append(p - addp)
        self._points = newpoints
        self.center()
        self._worldcoor = False

    # Проецирование фигуры тремя способами
    # tp = 0 (ортографическое), 1 (изометрическое), 2 (перспективное)
    # key = 0 (на yz), 1 (на xz), 2 (на xy) ДЛЯ ОРТОГРАФИЧЕСКИХ
    def projection(self, tp=0, key=0):

        orth = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]

        iso = [[m.sqrt(0.5), 0, -m.sqrt(0.5), 0],
               [1 / m.sqrt(6), 2 / m.sqrt(6), 1 / m.sqrt(6), 0],
               [1 / m.sqrt(3), -1 / m.sqrt(3), 1 / m.sqrt(3), 0],
               [0, 0, 0, 1]]

        per = [[m.sqrt(0.5), 0, -m.sqrt(0.5), 0],
               [1 / m.sqrt(6), 2 / m.sqrt(6), 1 / m.sqrt(6), 0],
               [1 / m.sqrt(3), -1 / m.sqrt(3), 1 / m.sqrt(3), 0],
               [0, 0, 0, 1]]

        if key == 0:
            orth[0][0] = 0
        elif key == 1:
            orth[1][1] = 0
        elif key == 2:
            orth[2][2] = 0

        x = self._center.x
        y = self._center.y
        z = self._center.z
        flag = self._worldcoor

        if (flag):
            self.returnCtoZ()

        newpoints = []

        mulmatr = []
        if tp == 0:
            mulmatr = orth
        elif tp == 1:
            mulmatr = iso
        elif tp == 2:
            mulmatr = per

        for p in self._points:
            newp = np.matmul([p.x, p.y, p.z, 1], mulmatr)
            newpoints.append(P(newp[0], newp[1], newp[2]) + P(x, y, z))

        if (flag):
            self.setcenter(x, y, z)

        return newpoints, self._edges

    # Поворот относительно выбранной оси координат (проходящей через центр)
    # key = 0 (относительно Х), 1 (относительно Y), 2 (относительно Z)
    def rotation(self, angle, key=0):
        r = m.radians(angle)
        rotX = [[1, 0, 0, 0], [0, m.cos(r), -m.sin(r), 0], [0, m.sin(r), m.cos(r), 0], [0, 0, 0, 1]]
        rotY = [[m.cos(r), 0, m.sin(r), 0], [0, 1, 0, 0], [-m.sin(r), 0, m.cos(r), 0], [0, 0, 0, 1]]
        rotZ = [[m.cos(r), -m.sin(r), 0, 0], [m.sin(r), m.cos(r), 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
        rot = []
        x = self._center.x
        y = self._center.y
        z = self._center.z
        flag = self._worldcoor
        if (flag):
            self.returnCtoZ()

        if key == 0:
            rot = rotX
        elif key == 1:
            rot = rotY
        elif key == 2:
            rot = rotZ

        newpoints = []
        for p in self._points:
            newp = np.matmul([p.x, p.y, p.z, 1], rot)
            newpoints.append(P(newp[0], newp[1], newp[2]))
        self._points = newpoints

        if (flag):
            self.setcenter(x, y, z)
        return self

    # Вращение по 3 заданным углам вокруг осей X, Y, Z соответственно
    def rotationXYZ(self, rX=0, rY=0, rZ=0):
        self.rotation(rX, 0)
        self.rotation(rY, 1)
        self.rotation(rZ, 2)
        return self

    # Поворот вокруг линии, заданной 2-мя точками
    def rotationL(self, p1, p2, angle):
        r = m.radians(angle)
        d1 = p1.x ** 2 + p1.y ** 2 + p1.z ** 2
        d2 = p2.x ** 2 + p2.y ** 2 + p2.z ** 2

        if d1 > d2:
            pshift = p1 - p2
            pmin = p2
        else:
            pshift = p2 - p1
            pmin = p1

        self.shift(-pmin.x, -pmin.y, -pmin.z)
        norm = m.sqrt(pshift.x ** 2 + pshift.y ** 2 + pshift.z ** 2)
        l = pshift.x / norm
        h = pshift.y / norm
        n = pshift.z / norm

        rot = [[l ** 2 + m.cos(r) * (1 - l ** 2), l * (1 - m.cos(r)) * h + n * m.sin(r),
                l * (1 - m.cos(r)) * n - h * m.sin(r), 0],
               [l * (1 - m.cos(r)) * h - n * m.sin(r), h ** 2 + m.cos(r) * (1 - h ** 2),
                h * (1 - m.cos(r)) * n + l * m.sin(r), 0],
               [l * (1 - m.cos(r)) * n + h * m.sin(r), h * (1 - m.cos(r)) * n - l * m.sin(r),
                n ** 2 + m.cos(r) * (1 - n ** 2), 0],
               [0, 0, 0, 1]]

        newpoints = []
        for p in self._points:
            newp = np.matmul([p.x, p.y, p.z, 1], rot)
            newpoints.append(P(newp[0], newp[1], newp[2]))
        self._points = newpoints
        self.shift(pmin.x, pmin.y, pmin.z)
        return self

    # Масштабирование относительно провзольной точки
    def scaleP(self, point, xscale, yscale, zscale):
        scale = [[xscale, 0, 0, 0], [0, yscale, 0, 0], [0, 0, zscale, 0], [0, 0, 0, 1]]
        newpoints = []
        for p in self._points:
            pbas = p
            pend = 0
            if (self._worldcoor):
                pbas = p - point
                pend = point
            newp = np.matmul([pbas.x, pbas.y, pbas.z, 1], scale)
            newpoints.append(P(newp[0], newp[1], newp[2]) + pend)
        self._points = newpoints
        return self

    # Масштабирование относительно центра
    def scaleC(self, xscale, yscale, zscale):
        return self.scaleP(self._center, xscale, yscale, zscale)

    # Сдвиг координат
    def shift(self, xshift, yshift, zshift):
        shift = [[1, 0, 0, xshift], [0, 1, 0, yshift], [0, 0, 1, zshift], [0, 0, 0, 1]]
        newpoints = []
        for p in self._points:
            newp = np.matmul(shift, [p.x, p.y, p.z, 1])
            newpoints.append(P(newp[0], newp[1], newp[2]))
        self._points = newpoints
        c = self._center
        newc = np.matmul(shift, [c.x, c.y, c.z, 1])
        self._center = P(newc[0], newc[1], newc[2])
        if self._center != P():
            self._worldcoor = True
        else:
            self._worldcoor = False
        return self

    # key = 0 (относительно xy), 1 (относительно xz), 2 (относительно yz).
    def reflection(self, key):
        refl = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
        if key == 0:
            refl[2][2] = -1
        elif key == 1:
            refl[1][1] = -1
        elif key == 2:
            refl[0][0] = -1

        newpoints = []
        for p in self._points:
            pbas = p
            pend = 0
            if (self._worldcoor):
                pbas = p - self._center
                pend = self._center
            newp = np.matmul(refl, [pbas.x, pbas.y, pbas.z, 1])
            newpoints.append(P(newp[0], newp[1], newp[2]) + pend)
        self._points = newpoints
        return self


# Класс тетраэдр (пирамида)
class Tetrahedron(N_edge):

    def __init__(self, scale=50):
        self._center = P()
        self._worldcoor = False
        self._points = [P(m.sqrt(8 / 9), 0, -1 / 3), P(-m.sqrt(2 / 9), m.sqrt(2 / 3), -1 / 3),
                        P(-m.sqrt(2 / 9), -m.sqrt(2 / 3), -1 / 3), P(0, 0, 1)]
        self._edges = [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]]
        self._psize = 4
        self._esize = 6
        self = self.scaleC(scale, scale, scale)


# Класс гексаэдр (куб)
class Hexahedron(N_edge):

    def __init__(self, scale=50):
        self._center = P()
        self._worldcoor = False
        self._points = [P(1, 1, -1), P(1, -1, -1), P(1, -1, 1), P(1, 1, 1), P(-1, 1, -1),
                        P(-1, -1, -1), P(-1, -1, 1), P(-1, 1, 1)]
        self._edges = [[0, 1], [0, 4], [0, 3], [1, 2], [1, 5], [2, 3], [2, 6],
                       [3, 7], [4, 5], [4, 7], [5, 6], [6, 7]]
        self = self.scaleC(scale, scale, scale)


# Класс октаэдр (восьмигранник)
class Octahedron(N_edge):

    def __init__(self, scale=50):
        self._center = P()
        self._worldcoor = False
        self._points = [P(1, 0, 0), P(0, -1, 0), P(0, 1, 0), P(0, 0, -1), P(0, 0, 1), P(-1, 0, 0)]
        self._edges = [[0, 1], [0, 2], [0, 3], [0, 4], [1, 3], [1, 4],
                       [1, 5], [2, 3], [2, 4], [2, 5], [3, 5], [4, 5]]
        self = self.scaleC(scale, scale, scale)


# Класс икосаэдр (20-гранник)
class Icosahedron(N_edge):

    def __init__(self, scale=50):
        self._center = P()
        self._worldcoor = False
        r = (1 + m.sqrt(5)) / 2
        self._points = [P(0, -1, -r), P(0, 1, -r), P(1, r, 0), P(r, 0, -1),
                        P(1, -r, 0), P(-1, -r, 0), P(-r, 0, -1), P(-1, r, 0),
                        P(r, 0, 1), P(-r, 0, 1), P(0, -1, r), P(0, 1, r)]
        self._edges = [[0, 1], [0, 3], [0, 4], [0, 5], [0, 6],
                       [1, 2], [1, 3], [1, 6], [1, 7],
                       [2, 3], [2, 7], [2, 8], [2, 11],
                       [3, 4], [3, 8],
                       [4, 5], [4, 8], [4, 10],
                       [5, 6], [5, 9], [5, 10],
                       [6, 7], [6, 9],
                       [7, 9], [7, 11],
                       [8, 10], [8, 11],
                       [9, 10], [9, 11],
                       [10, 11]]
        self = self.scaleC(scale, scale, scale)


# Класс додекаэдр (12-гранник)
class Dodecahedron(N_edge):

    def __init__(self, scale=50):
        self._center = P()
        self._worldcoor = False
        r = (3 + m.sqrt(5)) / 2
        x = (1 + m.sqrt(5)) / 2
        self._points = [P(0, -1, -r), P(0, 1, -r), P(x, x, -x), P(r, 0, -1),
                        P(x, -x, -x), P(1, -r, 0), P(-1, -r, 0), P(-x, -x, -x),
                        P(-r, 0, -1), P(-x, x, -x), P(-1, r, 0), P(1, r, 0),
                        P(-x, -x, x), P(0, -1, r), P(x, -x, x), P(0, 1, r),
                        P(-x, x, x), P(x, x, x), P(-r, 0, 1), P(r, 0, 1)]

        self._edges = [[0, 1], [0, 4], [0, 7], [1, 2], [1, 9],
                       [2, 3], [2, 11], [3, 4], [3, 19], [4, 5],
                       [5, 6], [5, 14], [6, 7], [6, 12], [7, 8],
                       [8, 9], [8, 18], [9, 10], [10, 11], [10, 16],
                       [11, 17], [12, 13], [12, 18], [13, 14], [13, 15],
                       [14, 19], [15, 16], [15, 17], [16, 18], [17, 19]]
        self = self.scaleC(scale, scale, scale)
         

# Груфик функции двух переменных
class Func(N_edge):

    def __init__(self, f, x0, x1, y0, y1, step = 0.1):
        max1 = min1 = f(x0, y0)
        self._points = []
        self._edges = []
        x = x0
        i = 0
        while x <= x1 + step / 10000:
            y = y0
            while y <= y1 + step / 10000:
                z = f(x, y)
                if z < min1:
                    min1 = z
                if z > max1:
                    max1 = z
                self._points.append(P(x, y, z))
                if y != y0:
                    self._edges.append([i, i + 1])
                    i += 1
                y += step
            i += 1
            x += step

        self._worldcoor = False
        self._center = P((x1 - x0) / 2, (y1 - y0) / 2, (max1 - min1) / 2)


def normalize(p1, p2):
    if (p2.z < p1.z or (p2.z == p1.z and p2.y < p1.y) or (p2.z == p1.z and p2.y == p1.y) and p2.x < p1.x):
        tmp = p1
        p1 = p2
        p2 = tmp
    x = p2.x - p1.x
    y = p2.y - p1.y
    z = p2.z - p1.z
    d = np.sqrt(x * x + y * y + z * z)
    if d != 0:
        return P(x=x / d, y=y / d, z=z / d)
    return P(0, 0, 0)


class RotationFigure(N_edge):

    def __init__(self, points, partitions, key=1):
        self._points = []
        self._edges = []

        size = len(points)
        for point in points:
            self._points.append(P(x=point[0], y=point[1], z=point[2]))

        # соединяем грани для первой кривой
        for i in range(size - 1):
            self._edges.append([i, i + 1])

        rot = 360 / partitions

        self._worldcoor = False
        self._center = P()

        our_points = self._points
        our_edges = self._edges

        for j in range(1, partitions):
            print('angle: ', rot * j)
            self.rotation(rot * j, key)

            state = (j - 1) * size

            for i in range(size):
                our_edges.append([i + state, (i + state + size) % partitions * size])

            state = j * size

            # соединяем грани для последующих кривых
            self._edges = []
            for i in range(size - 1):
                our_edges.append([i + state, i + state + 1])

            our_points += self._points
            state += size

        # соединяем точки по горизонтали
        #for i in range(partitions):
         #   for j in range(size):
         #       our_edges.append([(size * i + j) % len(our_points), (size * i + j + 1) % len(our_points)])

        # соединяем точки первой кривой с точками последней кривой
        #for i in range(count_points):
        #    our_edges += [[i, i + state]]

        self._points = our_points
        self._edges = our_edges
        print(self._points)

        # self._points = [P(0, 100, 40), P(20, 60, 70), P(0, 30, 50), P(0, 10, 50),
        #                 P(-40.0, 100.0, 2.4492935982947065e-15), P(-70.0, 60.0, 20.000000000000004),
        #                 P(-50.0, 30.0, 3.061616997868383e-15), P(-50.0, 10.0, 3.061616997868383e-15)],

        # self._edges = [[0, 1], [1, 2], [2, 3], [4, 5], [5, 6], [6, 7], [0, 4], [1, 5], [2, 6], [3, 7]]

# class RotationFigure2(N_edge):
#
#     def __init__(self, *points, partitions, key=1):
#         self._points = []
#         self._edges = []
#
#         count_points = len(points[0])
#         for point in points[0]:
#             self._points.append(P(x=point[0], y=point[1], z=point[2]))
#
#         # соединяем грани для первой кривой
#         for i in range(len(self._points) - 1):
#             self._edges.append([i, i + 1])
#
#         rot = 360 / partitions
#
#         self._worldcoor = False
#         self._center = P()
#
#         our_points = self._points
#         our_edges = self._edges
#
#         angle = rot
#         state = len(self._points)
#         for new_p in range(1, partitions):
#             print('angle: ', angle)
#             self.rotation(angle, key)
#             state = new_p * len(self._points)
#
#             # соединяем грани для последующих кривых
#             self._edges = list()
#             for i in range(len(self._points) - 1):
#                 self._edges.append([i + state, i + state + 1])
#
#             our_points += self._points
#             our_edges += self._edges
#             angle += rot
#             state += len(self._points)
#
#         # соединяем точки по горизонтали
#         #for i in range(count_points + count_points * 2):
#         #    our_edges.append([i, i + count_points])
#
#         # соединяем точки первой кривой с точками последней кривой
#         #for i in range(count_points):
#         #    our_edges += [[i, i + state]]
#
#         self._points = our_points[:2]
#         self._edges = our_edges
#         print(self._points)
        # self._points = [P(0, 100, 40), P(20, 60, 70), P(0, 30, 50), P(0, 10, 50),
        #                 P(-40.0, 100.0, 2.4492935982947065e-15), P(-70.0, 60.0, 20.000000000000004),
        #                 P(-50.0, 30.0, 3.061616997868383e-15), P(-50.0, 10.0, 3.061616997868383e-15)],

        # self._edges = [[0, 1], [1, 2], [2, 3], [4, 5], [5, 6], [6, 7], [0, 4], [1, 5], [2, 6], [3, 7]]


# Класс додекаэдр (12-гранник) dodecahedron
def main():
    f = Func(f=lambda x, y: x + y, x0=1, x1=2, y0=1, y1=2, step=0.5)
    print(f._points)
    print(f._edges)


if __name__ == "__main__":
    main()
