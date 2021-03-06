import numpy as np
from math import *
from shapely.geometry import LineString

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
def intersection( p1, p2, p3, p4 ): 
    line1 = LineString([(p1[0],p1[1]), (p2[0],p2[1])])
    line2 = LineString([(p3[0],p3[1]), (p4[0],p4[1])])
    if line1.intersection(line2).is_empty:
        return []
    else:
        return [line1.intersection(line2).x, line1.intersection(line2).y]

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



# не протестины
# принадлежит ли точка выпуклому многоугольнику

def belongs(points, x, y):
    for i in range(len(points) - 1):
        if not findside(points[i], points[i+1], x, y):
            return False
    return True


# принадлежит ли точка невыпуклому многоугольнику
def belongsnon(points, x, y):
    c = 0
    for i in range(len(points)):
        if intersection(points[i % len(points)], points[(i+1) % len(points)], [x, y], [x + 100000, y]) != []:
            c += 1
            inter = intersection(points[(i - 1 + len(points))% len(points)], points[(i+1) % len(points)], [x, y], [x + 100000, y])
            if points[i][1] == y and inter != []:
                c += 1

    if c % 2 == 1:
        return True
    else:
        return False


