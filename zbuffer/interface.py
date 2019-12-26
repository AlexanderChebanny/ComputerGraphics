from poly3d import *
#from lib import *
from tkinter import *
from tkinter import ttk
import numpy as np
from PIL import Image, ImageTk, ImageDraw

def interpolate(i0, d0, i1, d1):
    if i0 == i1:
        return [d0]
    values = []
    a = (d1 - d0) / (i1 - i0)
    d = d0
    for i in range(i0, i1 + 1):
        values.append(d + 0.5)
        d = d + a
    return values


class Gui:
    CANVAS_WIDTH = 500
    CANVAS_HEIGHT = CANVAS_WIDTH
    
    def __init__(self):
        self.window = Tk()
        self.figure = None
        self.proection = None   # проецирование = 0 (ортографическое), 1 (изометрическое), 2 (перспективное)
        self.xyz = None         # проецирование = 0 (на yz), 1 (на xz), 2 (на xy) ДЛЯ ОРТОГРАФИЧЕСКИХ

        self.window.title("MECHMAT GOVNO EBANOE")
        self.window.resizable(False, False)
        # canvas
        self.canvas = Canvas(self.window, width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT, background='white')
        self.canvas.grid(row=0, column=0)
        # mouse clicks
        self.canvas.bind("<ButtonRelease-1>", self.left_button_release)
        
        # clear button
        self.clear_button = ttk.Button(self.window, text='Clear', command=self.clear_window)
        self.clear_button.grid(row=15, column=2)
        self.buffer = np.full((self.CANVAS_WIDTH, self.CANVAS_HEIGHT), np.inf)
        self.OPTIONS_figure = [
            "",
            "Тетраэдр",
            "Гексаэдр",
            "Октаэдр",
            "Икосаэдр",
            "Додекаэдр",
            "Функция",
            'Фигура вращения'
        ]
        self.label1 = ttk.Label(self.window, text='Фигура:                ')
        self.label1.grid(row=1, column=1)
        self.what_figure = StringVar(self.window)
        self.what_figure.set(self.OPTIONS_figure[2])
        self.option_menu1 = ttk.OptionMenu(self.window, self.what_figure, *self.OPTIONS_figure)
        self.option_menu1.grid(row=2, column=1)

        self.OPTIONS_proection = [
            "",
            "Ортографическая",
            "Изометрическая",
            "Перспективная"
        ]
        self.label2 = ttk.Label(self.window, text='Проекция:                     ')
        self.label2.grid(row=1, column=2)
        self.what_proection = StringVar(self.window)
        self.what_proection.set(self.OPTIONS_proection[1])
        self.option_menu2 = ttk.OptionMenu(self.window, self.what_proection, *self.OPTIONS_proection)
        self.option_menu2.grid(row=2, column=2)

        self.OPTIONS_xyz = [
            "",
            "xy",
            "xz",
            "yz"
        ]
        self.label3 = ttk.Label(self.window, text='Проецирование на: ')
        self.label3.grid(row=1, column=3)
        self.what_xyz = StringVar(self.window)
        self.what_xyz.set(self.OPTIONS_xyz[1])
        self.option_menu3 = ttk.OptionMenu(self.window, self.what_xyz, *self.OPTIONS_xyz)
        self.option_menu3.grid(row=2, column=3)

        # ПОВОРОТ
        ttk.Label(self.window, text="Angle: ").grid(row=3, column=2)
        self.angle_input = Entry(self.window, width=7)
        self.angle_input.insert(0, "180")
        self.angle_input.grid(row=4, column=2)

        self.OPTIONS_rotate = [
            "",
            "оси X",
            "оси Y",
            "оси Z"
        ]
        self.label4 = ttk.Label(self.window, text='Поворот относительно: ')
        self.label4.grid(row=3, column=3)
        self.what_rotate = StringVar(self.window)
        self.what_rotate.set(self.OPTIONS_rotate[1])
        self.option_menu4 = ttk.OptionMenu(self.window, self.what_rotate, *self.OPTIONS_rotate)
        self.option_menu4.grid(row=4, column=3)

        self.rotate_button = ttk.Button(self.window, text='Rotate', command=self.rotate_action)
        self.rotate_button.grid(row=3, column=1)
        self.rotate_button2 = ttk.Button(self.window, text='Rotate line', command=self.rotate_line_action)
        self.rotate_button2.grid(row=4, column=1)

        self.label5 = ttk.Label(self.window, text='p1: ')
        self.label5.grid(row=3, column=4)
        self.p1_x = Entry(self.window, width=5)
        self.p1_x.grid(row=3, column=5)
        self.p1_x.insert(0, "0")
        self.p1_y = Entry(self.window, width=5)
        self.p1_y.grid(row=3, column=6)
        self.p1_y.insert(0, "0")
        self.p1_z = Entry(self.window, width=5)
        self.p1_z.grid(row=3, column=7)
        self.p1_z.insert(0, "0")

        self.label6 = ttk.Label(self.window, text='p2: ')
        self.label6.grid(row=4, column=4)
        self.p2_x = Entry(self.window, width=5)
        self.p2_x.grid(row=4, column=5)
        self.p2_x.insert(0, "1")
        self.p2_y = Entry(self.window, width=5)
        self.p2_y.grid(row=4, column=6)
        self.p2_y.insert(0, "1")
        self.p2_z = Entry(self.window, width=5)
        self.p2_z.grid(row=4, column=7)
        self.p2_z.insert(0, "1")

        # ОТРАЖЕНИЕ
        self.reflection_button = ttk.Button(self.window, text='Отражение', command=self.reflection_action)
        self.reflection_button.grid(row=6, column=1)
        self.OPTIONS_xyz_reflection = [
            "",
            "xy",
            "xz",
            "yz"
        ]
        self.label3 = ttk.Label(self.window, text='Отражение относительно: ')
        self.label3.grid(row=6, column=3)
        self.what_xyz_reflection = StringVar(self.window)
        self.what_xyz_reflection.set(self.OPTIONS_xyz_reflection[1])
        self.option_menu5 = ttk.OptionMenu(self.window, self.what_xyz_reflection, *self.OPTIONS_xyz_reflection)
        self.option_menu5.grid(row=7, column=3)

        # СДВИГ
        self.reflection_button = ttk.Button(self.window, text='Сдвиг', command=self.shift_action)
        self.reflection_button.grid(row=8, column=1)

        ttk.Label(self.window, text="Shift: ").grid(row=8, column=3)

        self.label7 = ttk.Label(self.window, text='X: ')
        self.label7.grid(row=8, column=4)
        self.shift_x = Entry(self.window, width=5)
        self.shift_x.grid(row=8, column=5)

        self.label8 = ttk.Label(self.window, text='Y: ')
        self.label8.grid(row=8, column=6)
        self.shift_y = Entry(self.window, width=5)
        self.shift_y.grid(row=8, column=7)

        self.label9 = ttk.Label(self.window, text='Z: ')
        self.label9.grid(row=8, column=8)
        self.shift_z = Entry(self.window, width=5)
        self.shift_z.grid(row=8, column=9)

        # МАСШТАБИРОВАНИЕ
        self.scale_button = ttk.Button(self.window, text='Scale', command=self.scale_action)
        self.scale_button.grid(row=9, column=1)

        ttk.Label(self.window, text="Scale: ").grid(row=9, column=3)
        # self.scale_input = Entry(self.window, width=7)
        # self.scale_input.insert(0, "1")
        # self.scale_input.grid(row=9, column=2)

        self.label10 = ttk.Label(self.window, text='X: ')
        self.label10.grid(row=9, column=4)
        self.scale_x = Entry(self.window, width=5)
        self.scale_x.grid(row=9, column=5)

        self.label11 = ttk.Label(self.window, text='Y: ')
        self.label11.grid(row=9, column=6)
        self.scale_y = Entry(self.window, width=5)
        self.scale_y.grid(row=9, column=7)

        self.label12 = ttk.Label(self.window, text='Z: ')
        self.label12.grid(row=9, column=8)
        self.scale_z = Entry(self.window, width=5)
        self.scale_z.grid(row=9, column=9)

        self.label13 = ttk.Label(self.window, text='Camera dist:')
        self.label13.grid(row=4, column=8)
        self.dist_z = Entry(self.window, width=5)
        self.dist_z.grid(row=4, column=9)

        ttk.Label(self.window, text="Camera angle:").grid(row=1, column=10)

        self.label14 = ttk.Label(self.window, text='Ox: ')
        self.label14.grid(row=2, column=10)
        self.cscale_x = Entry(self.window, width=5)
        self.cscale_x.grid(row=3, column=10)

        self.label15 = ttk.Label(self.window, text='Oy: ')
        self.label15.grid(row=4, column=10)
        self.cscale_y = Entry(self.window, width=5)
        self.cscale_y.grid(row=5, column=10)

        self.label16 = ttk.Label(self.window, text='Oz: ')
        self.label16.grid(row=6, column=10)
        self.cscale_z = Entry(self.window, width=5)
        self.cscale_z.grid(row=7, column=10)

        self.move_button = ttk.Button(self.window, text='Move', command=self.move_camera)
        self.move_button.grid(row=8, column=10)

        ttk.Label(self.window, text="Camera shift:").grid(row=1, column=11)

        self.label17 = ttk.Label(self.window, text='X: ')
        self.label17.grid(row=2, column=11)
        self.cshift_x = Entry(self.window, width=5)
        self.cshift_x.grid(row=3, column=11)

        self.label18 = ttk.Label(self.window, text='Y: ')
        self.label18.grid(row=4, column=11)
        self.cshift_y = Entry(self.window, width=5)
        self.cshift_y.grid(row=5, column=11)

        self.label19 = ttk.Label(self.window, text='Z: ')
        self.label19.grid(row=6, column=11)
        self.cshift_z = Entry(self.window, width=5)
        self.cshift_z.grid(row=7, column=11)

        self.set_default_values()

        self.Ox = int(self.cscale_x.get()) % 360
        self.Oy = int(self.cscale_y.get()) % 360
        self.Oz = int(self.cscale_z.get()) % 360

        self.Sx = int(self.cshift_x.get())
        self.Sy = int(self.cshift_y.get())
        self.Sz = int(self.cshift_z.get())

        self.window.mainloop()

    def set_default_values(self):
        """
        Установка значений по умолчанию во всех элементах интерфейса.
        Функция вызывается при первом запуске.
        """
        self.what_figure.set(self.OPTIONS_figure[1])
        self.what_xyz.set(self.OPTIONS_xyz[1])
        self.what_proection.set(self.OPTIONS_proection[1])
        self.angle_input.delete(0, END)
        self.angle_input.insert(0, "10")
        self.what_rotate.set(self.OPTIONS_rotate[1])
        self.what_xyz_reflection.set(self.OPTIONS_xyz_reflection[1])

        self.shift_x.delete(0, END)
        self.shift_x.insert(0, "50")
        self.shift_y.delete(0, END)
        self.shift_y.insert(0, "50")
        self.shift_z.delete(0, END)
        self.shift_z.insert(0, "0")

        self.scale_x.delete(0, END)
        self.scale_x.insert(0, "2")
        self.scale_y.delete(0, END)
        self.scale_y.insert(0, "2")
        self.scale_z.delete(0, END)
        self.scale_z.insert(0, "2")

        self.dist_z.delete(0, END)
        self.dist_z.insert(0, "100")

        self.cscale_x.delete(0, END)
        self.cscale_x.insert(0, "0")
        self.cscale_y.delete(0, END)
        self.cscale_y.insert(0, "0")
        self.cscale_z.delete(0, END)
        self.cscale_z.insert(0, "0")

        self.cshift_x.delete(0, END)
        self.cshift_x.insert(0, "0")
        self.cshift_y.delete(0, END)
        self.cshift_y.insert(0, "0")
        self.cshift_z.delete(0, END)
        self.cshift_z.insert(0, "0")

    def rotate_action(self):
        """
        Поворот
        """
        angle = float(self.angle_input.get())
        key = 0
        if self.what_rotate.get() == "оси X":
            key = 0
        elif self.what_rotate.get() == "оси Y":
            key = 1
        elif self.what_rotate.get() == "оси Z":
            key = 2

        self.figure.rotation(angle=angle, key=key)
        self.plot_figure()

    def rotate_line_action(self):
        """
        Поворот относительно линии
        """
        angle = float(self.angle_input.get())

        p1 = P(x=float(self.p1_x.get()), y=float(self.p1_y.get()), z=float(self.p1_z.get()))
        p2 = P(x=float(self.p2_x.get()), y=float(self.p2_y.get()), z=float(self.p2_z.get()))

        self.figure.rotationL(p1=p1, p2=p2, angle=angle)
        self.plot_figure()

    def reflection_action(self):
        """
        Отражение
        """
        key = 0
        if self.what_xyz_reflection.get() == 'xy':
            key = 0
        elif self.what_xyz_reflection.get() == 'xz':
            key = 1
        elif self.what_xyz_reflection.get() == 'yz':
            key = 2
        print(key)
        self.figure.reflection(key=key)
        self.plot_figure()

    def scale_action(self):
        """
        Масштабирование
        """
        # scale = float(self.scale_input.get())
        # self.figure.scaleC(xscale=scale, yscale=scale, zscale=scale)
        # self.plot_figure()
        #print('center', self.figure._center)
        #print('c1', self.figure._points[0])
        self.figure = self.figure.scaleC(xscale=float(self.scale_x.get()),
                                         yscale=float(self.scale_y.get()),
                                         zscale=float(self.scale_z.get()))
        #print('c2', self.figure._points[0])
        self.plot_figure()

    def shift_action(self):
        """
        Сдвиг
        """
        self.figure = self.figure.shift(xshift=float(self.shift_x.get()),
                                        yshift=float(self.shift_y.get()),
                                        zshift=float(self.shift_z.get()))
        self.plot_figure()

    def clear_window(self):
        """
        Отчистка окна
        """
        self.canvas.delete("all")

    def move_camera(self):

        self.Ox = (self.Ox + int(self.cscale_x.get())% 360) % 360
        self.Oy = (self.Oy + int(self.cscale_y.get())% 360) % 360
        self.Oz = (self.Oz + int(self.cscale_z.get())% 360) % 360

        self.Sx += int(self.cshift_x.get())
        self.Sy += int(self.cshift_y.get())
        self.Sz += int(self.cshift_z.get())

        self.plot_figure()

    def bufferize(self, P0:(int, int, int), P1:(int, int, int), P2:(int, int, int), C = [1, 1, 1], fcolor = (255, 50, 150)):
        height = self.CANVAS_HEIGHT // 2
        width = self.CANVAS_HEIGHT // 2
        # Сортировка точек так, что y0 <= y1 <= y2
        y0, y1, y2 = P0[1], P1[1], P2[1]

        if y0 == y1 == y2:
            return

        if P1[1] < P0[1]:
            P1, P0 = P0, P1
            t = C[1]
            C[1] = C[0]
            C[0] = t

        if P2[1] < P0[1]:
            P2, P0 = P0, P2
            t = C[2]
            C[2] = C[0]
            C[0] = t

        if P2[1] < P1[1]:
            P2, P1 = P1, P2
            t = C[2]
            C[2] = C[1]
            C[1] = t

        x0, x1, x2 = P0[0], P1[0], P2[0]
        y0, y1, y2 = P0[1], P1[1], P2[1]
        z0, z1, z2 = P0[2], P1[2], P2[2]

        # Вычисление координат x и значений h для рёбер треугольника
        x01 = interpolate(y0, x0, y1, x1)
        z01 = interpolate(y0, z0, y1, z1)

        x12 = interpolate(y1, x1, y2, x2)
        z12 = interpolate(y1, z1, y2, z2)

        x02 = interpolate(y0, x0, y2, x2)
        z02 = interpolate(y0, z0, y2, z2)
        print(C)
        c0, c1, c2 = [max(0.05, ((c + 1) / 2) ** 0.9) for c in C]
        print('colors: ', c0, c1, c2)
        c01 = interpolate(y0, c0 * 100, y1, c1 * 100)
        c12 = interpolate(y1, c1 * 100, y2, c2 * 100)
        c02 = interpolate(y0, c0 * 100, y2, c2 * 100)
        # Конкатенация коротких сторон
        x01 = x01[:-1]
        x012 = x01 + x12
        #print('012 len: ', len(x012))
        z01 = z01[:-1]
        z012 = z01 + z12

        c01 = c01[:-1]
        c012 = c01 + c12
        #print('c012', c012)
        # Определяем, какая из сторон левая и правая
        m = len(x02) // 2

        x_left = x_right = z_left = z_right = 0

        if x02[m] < x012[m]:
            x_left = x02
            x_right = x012
            z_left = z02
            z_right = z012
            c_left = c02
            c_right = c012
        else:
            x_left = x012
            x_right = x02
            z_left = z012
            z_right = z02
            c_left = c012
            c_right = c02

        # Отрисовка горизонтальных отрезков
        for y in range(y0, y2):
            x_l = int(x_left[y - y0])
            x_r = int(x_right[y - y0])
            if x_l > x_r:
                continue
            z_segment = interpolate(x_l, z_left[y - y0], x_r, z_right[y - y0])
            print(z_segment)
            c_segment = interpolate(x_l, c_left[y - y0], x_r, c_right[y - y0])
            for x in range(x_l, x_r + 1):
                shaded_color = 'aa'#hex(int(255 * h_segment[x - x_l] + 100 / 1000))[2:].zfill(2)
                z = z_segment[x - x_l]# / 100 * 255
                #z = 255 - min(255, max(0, z))
                #z = hex(int(z))[2:].zfill(2)
                #self.canvas.create_oval(width + x, height - y, width + x + 1, height - y - 1, outline="#"+z+z+z)
                if z < self.buffer[width + x][height - y]:
                    self.buffer[width + x][height - y] = z

    def plot_figure(self):
        """
        Отрисовка изменённой фигуры
        """
        self.clear_window()
        height = self.CANVAS_HEIGHT / 2
        width = self.CANVAS_HEIGHT / 2
        a = 0
        b = 100
        #print(interpolate(0, 0, 0, 100))
        ys = interpolate(a, 0, b - 100, 200)
        i = 0
        #for x in range(a, b + 1):
            #self.canvas.create_oval(width + x, height - ys[i], width + x, height - ys[i])
            #i += 1
        #self.draw_shaded_triangle((47, 0, -16), (-23, 40, -16), (-23, -40, -16))#(0, 0, 100), (100,0, 100), (0, 100, 0))
        #print(P(1,1,1).to_tuple()[0])
        #'''
        pnts, edgs, faces, center = self.figure.projection(tp=self.proection, key=self.xyz)
        normals = []
        ls = []
        intensities = []
        Is = []
        # kd - свойство материала воспринимать рассеянное освещение,
        # id - мощность рассеянного освещения
        kd = 1
        Id = 1


        minz = 100000
        maxz = -100000
        for p in pnts:
            if p.z < minz:
                minz = p.z
            if p.z > maxz:
                maxz = p.z

        def normalize_z(p):
            x, y, z = p.x, p.y, p.z
            z -= minz
            z = z / (maxz - minz) * 100
            return P(x, y, z)

        for face in faces:
            p1 = normalize_z(pnts[face[0]])
            p2 = normalize_z(pnts[face[1]])
            p3 = normalize_z(pnts[face[2]])
            print(p1, p2, p3)

            self.bufferize(p1.to_tuple(), p2.to_tuple(), p3.to_tuple())

            '''
            self.canvas.create_line(width + p1.x, height - p1.y, width + p2.x, height - p2.y)
            self.canvas.create_line(width + p2.x, height - p2.y, width + p3.x, height - p3.y)
            self.canvas.create_line(width + p3.x, height - p3.y, width + p1.x, height - p1.y)
            p1n = p1 + normals[face[0]]
            p2n = p2 + normals[face[1]]
            p3n = p3 + normals[face[2]]
            p1l = p1 + ls[face[0]]
            p2l = p2 + ls[face[1]]
            p3l = p3 + ls[face[2]]
            self.canvas.create_line(width + p1.x, height - p1.y, width + p1n.x, height - p1n.y, fill='#ff33aa')
            self.canvas.create_line(width + p2.x, height - p2.y, width + p2n.x, height - p2n.y, fill='#ff33aa')
            self.canvas.create_line(width + p3.x, height - p3.y, width + p3n.x, height - p3n.y, fill='#ff33aa')

            self.canvas.create_line(width + p1.x, height - p1.y, width + p1l.x, height - p1l.y, fill='#33aaff')
            self.canvas.create_line(width + p2.x, height - p2.y, width + p2l.x, height - p2l.y, fill='#33aaff')
            self.canvas.create_line(width + p3.x, height - p3.y, width + p3l.x, height - p3l.y, fill='#33aaff')
            '''
            #break
            if len(face) == 4:
                p4 = normalize_z(pnts[face[3]])
                self.bufferize(p1.to_tuple(), p3.to_tuple(), p4.to_tuple())
                #'''
            # TODO вывести self.buffer на экран
            #   если == np.inf, то цвет белый
            #   ecли != np.inf, о лежит в [0, 100] (чем ближе, тем меньше значение)
            #   если buffer[x][y] = z, то с = 255 - max(0, min(255, z/100 * 255)) color[x][y] = (с, c, c)


        '''
        
        
        self.figure.shift(-self.Sx, -self.Sy, -self.Sz)
        self.figure.rotationL(P(0, 0, 0), P(1, 0, 0), -self.Ox)
        self.figure.rotationL(P(0, 0, 0), P(0, 1, 0), -self.Oy)
        self.figure.rotationL(P(0, 0, 0), P(0, 0, 1), -self.Oz)

        pnts, edgs, faces = self.figure.projection(tp=self.proection, key=self.xyz)
        camera_dist = float(self.dist_z.get())
        camera_point = P(0, 0, camera_dist)
        print(faces)
        print(pnts)
        print(edgs)
        for face in faces:
            p1 = pnts[face[0]]
            p2 = pnts[face[1]]
            if self.proection == 0:
                if self.xyz == 0:
                    self.canvas.create_line(width + p1.y, height - p1.z, width + p2.y, height - p2.z)
                elif self.xyz == 1:
                    self.canvas.create_line(width + p1.x, height - p1.z, width + p2.x, height - p2.z)
                elif self.xyz == 2:
                    self.canvas.create_line(width + p1.x, height - p1.y, width + p2.x, height - p2.y)
            elif self.proection == 1:
                self.canvas.create_line(width + p1.x, height - p1.y, width + p2.x, height - p2.y)
            elif self.proection == 2:
                self.canvas.create_line(width + p1.x, height - p1.y, width + p2.x, height - p2.y)
                
            p1 = pnts[face[1]]
            p2 = pnts[face[2]]
            if self.proection == 0:
                if self.xyz == 0:
                    self.canvas.create_line(width + p1.y, height - p1.z, width + p2.y, height - p2.z)
                elif self.xyz == 1:
                    self.canvas.create_line(width + p1.x, height - p1.z, width + p2.x, height - p2.z)
                elif self.xyz == 2:
                    self.canvas.create_line(width + p1.x, height - p1.y, width + p2.x, height - p2.y)
            elif self.proection == 1:
                self.canvas.create_line(width + p1.x, height - p1.y, width + p2.x, height - p2.y)
            elif self.proection == 2:
                self.canvas.create_line(width + p1.x, height - p1.y, width + p2.x, height - p2.y)
            if len(face) == 3:
                p1 = pnts[face[2]]
                p2 = pnts[face[0]]
                if self.proection == 0:
                    if self.xyz == 0:
                        self.canvas.create_line(width + p1.y, height - p1.z, width + p2.y, height - p2.z)
                    elif self.xyz == 1:
                        self.canvas.create_line(width + p1.x, height - p1.z, width + p2.x, height - p2.z)
                    elif self.xyz == 2:
                        self.canvas.create_line(width + p1.x, height - p1.y, width + p2.x, height - p2.y)
                elif self.proection == 1:
                    self.canvas.create_line(width + p1.x, height - p1.y, width + p2.x, height - p2.y)
                elif self.proection == 2:
                    self.canvas.create_line(width + p1.x, height - p1.y, width + p2.x, height - p2.y)
            elif len(face) == 4:
                p1 = pnts[face[2]]
                p2 = pnts[face[3]]
                if self.proection == 0:
                    if self.xyz == 0:
                        self.canvas.create_line(width + p1.y, height - p1.z, width + p2.y, height - p2.z)
                    elif self.xyz == 1:
                        self.canvas.create_line(width + p1.x, height - p1.z, width + p2.x, height - p2.z)
                    elif self.xyz == 2:
                        self.canvas.create_line(width + p1.x, height - p1.y, width + p2.x, height - p2.y)
                elif self.proection == 1:
                    self.canvas.create_line(width + p1.x, height - p1.y, width + p2.x, height - p2.y)
                elif self.proection == 2:
                    self.canvas.create_line(width + p1.x, height - p1.y, width + p2.x, height - p2.y)
                p1 = pnts[face[3]]
                p2 = pnts[face[0]]
                if self.proection == 0:
                    if self.xyz == 0:
                        self.canvas.create_line(width + p1.y, height - p1.z, width + p2.y, height - p2.z)
                    elif self.xyz == 1:
                        self.canvas.create_line(width + p1.x, height - p1.z, width + p2.x, height - p2.z)
                    elif self.xyz == 2:
                        self.canvas.create_line(width + p1.x, height - p1.y, width + p2.x, height - p2.y)
                elif self.proection == 1:
                    self.canvas.create_line(width + p1.x, height - p1.y, width + p2.x, height - p2.y)
                elif self.proection == 2:
                    self.canvas.create_line(width + p1.x, height - p1.y, width + p2.x, height - p2.y)
                

        self.figure.rotationL(P(self.Sx, self.Sy, self.Sz), P(self.Sx + 1, self.Sy, self.Sz), self.Ox)
        self.figure.rotationL(P(self.Sx, self.Sy, self.Sz), P(self.Sx, self.Sy + 1, self.Sz), self.Oy)
        self.figure.rotationL(P(self.Sx, self.Sy, self.Sz), P(self.Sx, self.Sy, self.Sz + 1), self.Oz)
        self.figure.shift(self.Sx, self.Sy, self.Sz)'''
        '''
        for e in edgs:
            p1 = pnts[e[0]]
            p1_scale = dist(p1, camera_point) / camera_dist# self.figure.norm # norm
            p2 = pnts[e[1]]
            p2_scale = dist(p2, camera_point) / camera_dist# self.figure.norm # norm
            if self.proection == 0:
                if self.xyz == 0:
                    self.canvas.create_line(width + p1.y, height - p1.z, width + p2.y, height - p2.z)
                elif self.xyz == 1:
                    self.canvas.create_line(width + p1.x, height - p1.z, width + p2.x, height - p2.z)
                elif self.xyz == 2:
                    self.canvas.create_line(width + p1.x, height - p1.y, width + p2.x, height - p2.y)
            elif self.proection == 1:
                self.canvas.create_line(width + p1.x, height - p1.y, width + p2.x, height - p2.y)
            elif self.proection == 2:
                self.canvas.create_line(width + p1.x / p1_scale, height - p1.y / p1_scale, width + p2.x / p2_scale, height - p2.y / p2_scale)
        '''

    def left_button_release(self, event):
        """
        Установка фигуры по левому нажатию мыши
        """
        self.Ox = int(self.cscale_x.get()) % 360
        self.Oy = int(self.cscale_y.get()) % 360
        self.Oz = int(self.cscale_z.get()) % 360

        self.Sx = int(self.cshift_x.get())
        self.Sy = int(self.cshift_y.get())
        self.Sz = int(self.cshift_z.get())

        camera_dist = float(self.dist_z.get())
        camera_point = P(0, 0, camera_dist)
        self.figure = Tetrahedron(camera_point)
        if self.what_figure.get() == "Тетраэдр":
            self.figure = Tetrahedron(camera_point)
        elif self.what_figure.get() == "Гексаэдр":
            self.figure = Hexahedron(camera_point)
        elif self.what_figure.get() == "Октаэдр":
            self.figure = Octahedron(camera_point)
        elif self.what_figure.get() == "Икосаэдр":
            self.figure = Icosahedron(camera_point)
        elif self.what_figure.get() == "Додекаэдр":
            self.figure = Dodecahedron(camera_point)
        elif self.what_figure.get() == "Функция":
                self.figure = Func(camera_point=camera_point, f=lambda x, y: np.sin((x + y) * 3), x0=0, x1=5, y0=0, y1=5, step=0.2)
                print(self.figure._points)
                # np.sin((x + y) * 3)
                # (x + y)
        elif self.what_figure.get() == "Фигура вращения":
            self.figure = RotationFigure(camera_point=camera_point, points=[[100, 0, 0], [25, 0, 100]], partitions=7, key=2) # [[0, 100, 40], [20, 60, 70], [0, 30, 50], [0, 10, 50]]
        
        tp = 0
        if self.what_proection.get() == 'Перспективная':
            tp = 2
        elif self.what_proection.get() == 'Изометрическая':
            tp = 1
        elif self.what_proection.get() == 'Ортографическая':
            tp = 0

        key = 2
        if self.what_xyz.get() == 'yz':
            key = 0
        elif self.what_xyz.get() == 'xz':
            key = 1
        elif self.what_xyz.get() == 'xy':
            key = 2

        self.proection = tp
        self.xyz = key
        #self.figure.setcenter(250, 250, 0)  # .rotationXYZ(20, 60, 60)
        self.plot_figure()


if __name__ == '__main__':
    Gui()
