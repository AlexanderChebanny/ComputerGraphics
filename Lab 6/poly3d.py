import math as m
import numpy as np

# Класс точка
class P(object):
    
    def __init__(self, x = 0, y = 0, z = 0):
        self.x = x
        self.y = y
        self.z = z
        
    def __add__(self, p): 
        if type(p) == int:
            return  P(self.x + p, self.y + p, self.z + p)
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
    
    def __str__(self):
        return "(%s, %s, %s)" % (self.x, self.y, self.z)
    
    def __repr__(self):
        return "(%s, %s, %s)" % (self.x, self.y, self.z)
        

# Класс линия     
class L(object):
    
    def __init__(self, p1 = P(), p2 = P()):
        self.x1 = p1.x
        self.y1 = p1.y
        self.z1 = p1.z
        self.x2 = p2.x
        self.y2 = p2.y
        self.z2 = p2.z


# Класс многоугольник
class N_edge(object):
    
    def __init__(self, points = [], edges = [], worldcoor = False):
        self._points = points
        self._edges = edges
        self._psize = len(points)
        self._esize = len(edges)
        self._worldcoor = worldcoor
        if self._points != []:
            self.center()
    
    def typecoor(self):
        return self._worldcoor
    
    def fileread(self, filename):
        self._points = []
        self._edges = []
        f = open(filename, 'r')
        for line in f:
            pline = line.split(' ')
            if len(pline) == 3:
                self._points.append(P(int(pline[0]), int(pline[1]), int(pline[2])))
            if len(pline) == 2:
                self._edges.append([int(pline[0]), int(pline[1])])
            if len(pline) == 1:
                self._worldcoor = bool(pline[0])
        f.close()
        if self._points != []:
            self.center()
        return self
        
    def filesave(self, filename):
         f = open(filename, 'w')
         for p in self._points:
             f.write(str(p.x) + ' ' + str(p.y) + ' ' + str(p.z))
         for e in self._edges:
             f.write(str(e[0]) + ' ' + str(e[1]))
         f.write(str(False))
         f.close()
         return self
    
    def center(self):
        x = y = z = 0
        for p in self._points:
            x += p.x
            y += p.y
            z += p.z
        self._center = P(x/len(self._points), y/len(self._points), z/len(self._points))
        return self._center
    
    def setcenter(self, x = 0, y = 0, z = 0):
        if (self._worldcoor):
            x -= self._center.x
            y -= self._center.y
            z -= self._center.z
        addp = P(x, y, z)
        self._center = self._center + addp
        newp = []
        for p in self._points:
            newp.append(p + addp)
        self._points = newp
        self._worldcoor = True
        return self
    
    def returCtoZ(self):
        x = self._center.x
        y = self._center.y
        z = self._center.z
        newp = []
        addp = P(x, y, z)
        for p in self._points:
            newp.append(p - addp)
        self._points = newp
        self._center = P(0, 0, 0)
        self._worldcoor = False
        
    def proj_2d(self):
        pnts = []
        for p in self._points:
            pnts.append(P(p.x / p.z, p.y / p.z))
        return self._points, self._edges
    
    def rotationX(self, angle):
        r = m.radians(angle)
        rot = [[1, 0, 0, 0], [0, m.cos(r), -m.sin(r), 0], [0, m.sin(r), m.cos(r), 0], [0, 0, 0, 1]]
        newpoints = []
        
        for p in self._points:
            pbas = p
            pend = 0
            if (self._worldcoor):
                pbas = p - self._center
                pend = self._center
            newp = np.matmul([pbas.x, pbas.y, pbas.z, 1], rot)
            newpoints.append(P(newp[0], newp[1], newp[2]) + pend)
        self._points = newpoints
        return self
        
    def rotationY(self, angle):
        r = m.radians(angle)
        rot = [[m.cos(r), 0, m.sin(r), 0], [0, 1, 0, 0],[-m.sin(r), 0, m.cos(r), 0], [0, 0, 0, 1]]
        newpoints = []
        
        for p in self._points:
            pbas = p
            pend = 0
            if (self._worldcoor):
                pbas = p - self._center
                pend = self._center
            newp = np.matmul([pbas.x, pbas.y, pbas.z, 1], rot)
            newpoints.append(P(newp[0], newp[1], newp[2]) + pend)
        self._points = newpoints
        return self
   
    def rotationZ(self, angle):
        r = m.radians(angle)
        rot = [[m.cos(r), -m.sin(r), 0, 0], [m.sin(r), m.cos(r), 0, 0],[0, 0, 1, 0], [0, 0, 0, 1]]
        newpoints = []
        
        for p in self._points:
            pbas = p
            pend = 0
            if (self._worldcoor):
                pbas = p - self._center
                pend = self._center
            newp = np.matmul([pbas.x, pbas.y, pbas.z, 1], rot)
            newpoints.append(P(newp[0], newp[1], newp[2]) + pend)
        self._points = newpoints
        return self
    
    def rotationXYZ(self, rotX = 0, rotY = 0, rotZ = 0):
        return self.rotationX(rotX).rotationY(rotY).rotationZ(rotZ)
        
    def scale(self, xscale, yscale, zscale):
        scale = [[xscale, 0, 0, 0], [0, yscale, 0, 0], [0, 0, zscale, 0], [0, 0, 0 ,1]]
        newpoints = []
        for p in self._points:
            pbas = p
            pend = 0
            if (self._worldcoor):
                pbas = p - self._center
                pend = self._center
            newp = np.matmul([pbas.x, pbas.y, pbas.z, 1], scale)
            newpoints.append(P(newp[0], newp[1], newp[2]) + pend)
        self._points = newpoints
        return self
    
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
        self._worldcoor = True
        return self


# Класс тетраэдр (пирамида)
class Tetrahedron(N_edge):
    
     def __init__(self, scale = 50):
         self._center = P()
         self._worldcoor = False
         self._points = [P(m.sqrt(8/9), 0, -1/3 ), P(-m.sqrt(2/9), m.sqrt(2/3), -1/3), P(-m.sqrt(2/9), -m.sqrt(2/3), -1/3), P(0, 0, 1)]      
         self._edges = [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]]
         self._psize = 4
         self._esize = 6
         self = self.scale(scale, scale, scale)
         
         
# Класс гексаэдр (куб)
class Hexahedron(N_edge):    
     
    def __init__(self, scale = 50):
         self._center = P()
         self._worldcoor = False
         self._points = [P(1, 1, -1), P(1, -1, -1), P(1, -1, 1), P(1, 1, 1), P(-1, 1, -1), P(-1, -1, -1), P(-1, -1, 1), P(-1, 1, 1)]      
         self._edges = [[0, 1], [0, 4], [0 ,3], [1, 2], [1, 5], [2, 3], [2, 6], [3, 7], [4, 5], [4, 7], [5, 6], [6, 7]]
         self._psize = 8
         self._esize = 12
         self = self.scale(scale, scale, scale)
         
         
# Класс октаэдр (восьмигранник)
class Octahedron(N_edge):     
    
     def __init__(self, scale = 50):
         self._center = P()
         self._worldcoor = False
         self._points = [P(1, 0, 0), P(0, -1, 0), P(0, 1, 0), P(0, 0, -1), P(0, 0, 1), P(-1, 0, 0)]     
         self._edges = [[0, 1], [0, 2], [0, 3], [0, 4], [1, 3], [1, 4], [1, 5], [2, 3], [2, 4], [2, 5], [3, 5], [4, 5]]
         self._psize = 8
         self._esize = 12
         self = self.scale(scale, scale, scale)
         
         
# Класс икосаэдр (20-гранник)
class Icosahedron(N_edge):
    
     def __init__(self, scale = 50):
         self._center = P()
         self._worldcoor = False
         self._points = []     
         self._edges = []
         self._psize = 8
         self._esize = 12
         self = self.scale(scale, scale, scale)
    
 
# Класс додекаэдр (12-гранник) dodecahedron
def main():
    print(type(3))
    
if __name__ == "__main__":
    main()