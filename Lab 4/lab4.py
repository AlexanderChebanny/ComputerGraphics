import numpy as np
from math import *


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


if __name__ == '__main__':
    points = [
        [2,1,1],
        [2,4,1],
        [6,1,1],
        [6,4,1]
    ]
    # cent = barycenter(points)    # good
    # t = offset(points, -cent[0], -cent[1])
    # print(rotate_basic(t, np.pi/2))
    #print(intersection([390, 309], [657, 346], [518, 452], [318, 509]))
    #print(findside([183, 406], [617, 335], 502, 567))
    #print(findside([384, 486], [624, 261],402, 282))
    print(belongsnon([[0,0], [2,2], [4,0]], 1, 2))

    #print(intersection([1,1],[5,5],[1,5],[5,1]))
