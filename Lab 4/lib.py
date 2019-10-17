import numpy as np
from PIL import Image, ImageDraw

class Point:
    def __init__(self, *args):
        if len(args) == 1 and len(args[0]) == 3:
            self.coors = np.array(args[0])
        elif len(args) == 3:
            self.coors = np.array(args)
    def x(self):
        return self.coors[0]
    def y(self):
        return self.coors[1]
    def z(self):
        return self.coors[2]
    def __getitem__(self, key):
        return self.coors[key]
    def __iter__(self):
        return self.coors.__iter__()
    def __len__(self):
        return 3
    def apply_transform(self, transform):
        pt = np.ones((4,1))
        pt[:3,:] = self.coors.reshape((3,1))
        m = transform.matrix.dot(pt).reshape((4))
        m /= m[3]
        return Point(m[:3])
    def __str__(self):
        return self.coors.__str__()
    def __repr__(self):
        return self.__str__()

class Line:
    def __init__(self, *args):
        if len(args) == 2:
            self.data = np.hstack((
                np.array(args[0]).reshape((3,1)),
                np.array(args[1]).reshape((3,1))
            ))
    def __getitem__(self, key):
        if key == 0:
            return Point(self.data[:,0])
        elif key == 1:
            return Point(self.data[:,1])

class Polygon:
    def __init__(self, *args):
        if len(args) == 1:
            points = args[0]
        else:
            points = args
        self.data = np.hstack(
            map(lambda x: np.array(x).reshape((3,1)), points)
        )
    def __len__(self):
        return self.data.shape[1]
    def __getitem__(self, key):
        return self.data[:, key]

class Polyhedron:
    def __init__(self, points, sides): # side is an iterable of indexes of points

        self.points = np.hstack(
            map(lambda x: np.array(x).reshape((3,1)), points)
        ).astype(np.float64)
        self.sides = sides
        self.center = self.find_center()

    def find_center(self):
        s = self.points.sum(axis=1)
        s /= self.points.shape[1]
        return Point(s.reshape(3))

    def apply_transform(self, transform):
        l = self.points.shape[1]
        p = np.ones((4, l))
        p[:3,:]  = self.points
        r = transform.matrix.dot(p)
        r / r[3,:]
        return Polyhedron(r[:3,:].T, self.sides)

    def apply_relative_transform(self, transform):
        tr = Transform.translate(
            self.center[0],
            self.center[1],
            self.center[2]
        ).compose(transform).compose(Transform.translate(
            -self.center[0],
            -self.center[1],
            -self.center[2]
        ))
        return self.apply_transform(tr)

    @staticmethod
    def Tetrahedron(center, radius):
        tetrahedral_angle = np.arccos(-1/3)
        tr_rot = Transform.rotate('z',120/180*np.pi)
        p1 = Point(0,0,radius)
        p2 = p1.apply_transform(Transform.rotate('x', tetrahedral_angle))
        p3 = p2.apply_transform(tr_rot)
        p4 = p3.apply_transform(tr_rot)
        p = Polyhedron([p1,p2,p3,p4],[
            [0,1,2],
            [0,2,3],
            [0,3,1],
            [1,2,3]
        ])
        p=p.apply_transform(Transform.translate(center.x(), center.y(), center.z()))
        return p
    @staticmethod
    def Cube(center, side):
        points = [
            Point(0,0,0),
            Point(0,side,0),
            Point(side,side,0),
            Point(side,0,0),
            Point(0,0,side),
            Point(0,side,side),
            Point(side,side,side),
            Point(side,0,side)
        ]
        sides = [
            [0,1,2,3],
            [4,5,6,7],
            [0,1,5,1],
            [3,0,4,7],
            [1,2,6,5],
            [2,3,7,6]
        ]
        p = Polyhedron(points, sides)
        p=p.apply_transform(Transform.translate(
            center.x()-side/2,
            center.y()-side/2,
            center.z()-side/2
        ))
        return p
    @staticmethod
    def Octahedron(center, radius):
        points = [
            Point(0,0,radius),
            Point(radius, 0, 0),
            Point(0, radius,0),
            Point(-radius, 0, 0),
            Point(0,-radius,0),
            Point(0,0,-radius)
        ]
        sides = [
            [0,1,2],
            [0,2,3],
            [0,3,4],
            [0,4,1],
            [5,1,2],
            [5,2,3],
            [5,3,4],
            [5,4,1]
        ]
        p = Polyhedron(points, sides)
        p=p.apply_transform(Transform.translate(
            center.x(),
            center.y(),
            center.z()
        ))
        return p

class Transform:
    def __init__(self, matrix):
        self.matrix = np.ndarray((4,4))
        self.matrix[...] = matrix

    def compose(self, transform):
        return Transform(self.matrix.dot(transform.matrix))

    @staticmethod
    def identity():
        return Transform(np.identity(4))
    @staticmethod
    def translate(dx,dy,dz):
        return Transform([
            [1,0,0,dx],
            [0,1,0,dy],
            [0,0,1,dz],
            [0,0,0, 1]
        ])
    @staticmethod
    def scale(sx,sy,sz):
        return Transform([
            [sx, 0, 0, 0],
            [ 0,sy, 0, 0],
            [ 0, 0,sz, 0],
            [ 0, 0, 0, 1]
        ])
    @staticmethod
    def rotate(axis, angle):
        sin = np.sin(angle)
        cos = np.cos(angle)
        if axis == 'x':
            return Transform([
                [1,   0,   0,0],
                [0, cos,-sin,0],
                [0, sin, cos,0],
                [0,   0,   0,1]
            ])
        elif axis == 'y':
            return Transform([
                [ cos,  0, sin,0],
                [   0,  1,   0,0],
                [-sin,  0, cos,0],
                [   0,  0,   0,1]
            ])
        elif axis == 'z':
            return Transform([
                [ cos,-sin,  0,0],
                [ sin, cos,  0,0],
                [   0,  0,   1,0],
                [   0,  0,   0,1]
            ])
    @staticmethod
    def rotate_around_line(line, angle):
        dx = line[1].x() - line[0].x()
        dy = line[1].y() - line[0].y()
        dz = line[1].z() - line[0].z()
        angle_to_yz = np.arctan2(dx, dz)
        angle_to_xz = np.arctan2(dy, dz)
        tr = Transform.rotate('y', angle_to_xz).compose(
            Transform.rotate('x', angle_to_yz)
        )
        untr = Transform.rotate('x', -angle_to_yz).compose(
            Transform.rotate('y', -angle_to_xz)
        )
        return untr.compose(
            Transform.rotate('z', angle)
        ).compose(tr)
    @staticmethod
    def reflect(plane):
        if plane == 'xy':
            return Transform([
                [1,0,0,0],
                [0,1,0,0],
                [0,0,-1,0],
                [0,0,0,1]
            ])
        elif plane == 'xz':
            return Transform([
                [1,0,0,0],
                [0,-1,0,0],
                [0,0,1,0],
                [0,0,0,1]
            ])
        elif plane == 'yz':
            return Transform([
                [-1,0,0,0],
                [0,1,0,0],
                [0,0,1,0],
                [0,0,0,1]
            ])


class Camera:
    def __init__(self, matrix):
        self.matrix = np.ndarray((3,4))
        self.matrix[...] = matrix

    def draw(self, size, points, lines):
        image = Image.new('RGB', size)
        size=np.array(size)
        l = points.shape[1]
        p = np.ones((4, l))
        p[:3,:]  = points
        r = self.matrix.dot(p)
        pts = (r / r[2,:])[:2,:]
        draw = ImageDraw.Draw(image)
        for line in lines:
            for i in range(len(line)):
                b = pts[:,line[i]].T+size/2
                e = pts[:,line[(i+1)%len(line)]].T+size/2
                # draw.line((b[0], size[1]-b[1], e[0], size[1]-e[1]), fill=(255,0,0))
                for j in range(10):
                    pb = b + (e-b)/10*j
                    pe = b + (e-b)/10*(j+1)
                    pz = points[:, line[i]][1]+(points[:, line[(i+1)%len(line)]][1] - points[:, line[i]][1])*j/10
                    k = pz/50
                    k = 1 if k > 1 else (0 if k < 0 else k)
                    red = np.array((255,0,0))
                    blue = np.array((0,0,255))
                    col = (red+k*(blue-red)).astype('int')
                    draw.line((pb[0], size[1]-pb[1], pe[0], size[1]-pe[1]), fill=tuple(col))

        return image

    @staticmethod
    def ortho():
        return Camera([
            [1,0,0,0],
            [0,0,1,0],
            [0,0,0,1]
        ])
    @staticmethod
    def persp(k):
        return Camera([
            [1,0,0,0],
            [0,0,1,0],
            [0,k,0,1]
        ])
    @staticmethod
    def iso(a = np.arcsin(np.tan(30/180*np.pi)),b = np.pi/4):
        tr = Transform.rotate('x', a).compose(
            Transform.rotate('z', b)
        )
        m = np.array([
            [1,0,0,0],
            [0,0,1,0],
            [0,0,0,1]
        ]).dot(tr.matrix)
        return Camera(m)


if __name__ == "__main__":
    import imageio as iio
    t = Polyhedron.Octahedron(Point(10,0,0),7)
    # print(t.points)
    c = Camera.iso()
    with iio.get_writer("test.gif", fps=30) as w:
        for i in range(1000):
            tr = Transform.scale(5,5,5).compose(
                Transform.rotate('x', 0).compose(
                    # Transform.rotate('z', 2*np.pi*i/100)
                    # Transform.identity()
                    Transform.rotate_around_line(
                        Line(Point(0,0,0), Point(1-i/1000,0,i/1000)),
                        2*np.pi*i/100
                    )
                )
            )
            # tr = Transform.reflect('yz').compose(tr)
            p = t.apply_relative_transform(tr)
            im=np.array(c.draw((112,112), p.points, p.sides))
            w.append_data(im)
