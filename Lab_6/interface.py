from Lab_6.poly3d import *
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw


class Gui:
    CANVAS_WIDTH = 500
    CANVAS_HEIGHT = 500
    
    def __init__(self):
        self.window = Tk()
        self.figure = None
        self.proection = None   # проецирование = 0 (ортографическое), 1 (изометрическое), 2 (перспективное)
        self.xyz = None         # проецирование = 0 (на yz), 1 (на xz), 2 (на xy) ДЛЯ ОРТОГРАФИЧЕСКИХ
        # self.full_figure = False
        # point
        # self.point = False
        # self.point_x = 0
        # self.point_y = 0
        self.window.title("MECHMAT SILA")
        self.window.resizable(False, False)
        # current figure
        # self.points = []
        # canvas
        self.canvas = Canvas(self.window, width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT)   # , background='white'
        self.canvas.grid(row=0, column=0)
        # mouse clicks
        self.canvas.bind("<ButtonRelease-1>", self.left_button_release)
        # self.canvas.bind("<ButtonRelease-2>", self.right_button_release)
        
        # clear button
        self.clear_button = ttk.Button(self.window, text='Clear', command=self.clear_window)
        self.clear_button.grid(row=15, column=2)

        self.ok_button = ttk.Button(self.window, text='Ok', command=self.ok)
        self.ok_button.grid(row=16, column=2)

        OPTIONS_figure = [
            "",
            "Тетраэдр",
            "Гексаэдр",
            "Октаэдр",
            "Икосаэдр",
            "Додекаэдр"
        ]
        self.label1 = ttk.Label(self.window, text='Фигура:                ')
        self.label1.grid(row=1, column=1)
        self.what_figure = StringVar(self.window)
        self.what_figure.set(OPTIONS_figure[1])
        self.option_menu1 = ttk.OptionMenu(self.window, self.what_figure, *OPTIONS_figure)
        self.option_menu1.grid(row=2, column=1)

        OPTIONS_proection = [
            "",
            "Ортографическая",
            "Изометрическая",
            "Перспективная"
        ]
        self.label2 = ttk.Label(self.window, text='Проекция:                     ')
        self.label2.grid(row=1, column=2)
        self.what_proection = StringVar(self.window)
        self.what_proection.set(OPTIONS_proection[1])
        self.option_menu2 = ttk.OptionMenu(self.window, self.what_proection, *OPTIONS_proection)
        self.option_menu2.grid(row=2, column=2)

        OPTIONS_xyz = [
            "",
            "xy",
            "xz",
            "yz"
        ]
        self.label3 = ttk.Label(self.window, text='Проецирование на: ')
        self.label3.grid(row=1, column=3)
        self.what_xyz = StringVar(self.window)
        self.what_xyz.set(OPTIONS_xyz[1])
        self.option_menu3 = ttk.OptionMenu(self.window, self.what_xyz, *OPTIONS_xyz)
        self.option_menu3.grid(row=2, column=3)

        # ПОВОРОТ
        ttk.Label(self.window, text="Angle: ").grid(row=3, column=2)
        self.angle_input = Entry(self.window, width=7)
        self.angle_input.insert(0, "180")
        self.angle_input.grid(row=4, column=2)

        OPTIONS_rotate = [
            "",
            "оси X",
            "оси Y",
            "оси Z"
        ]
        self.label4 = ttk.Label(self.window, text='Поворот относительно: ')
        self.label4.grid(row=3, column=3)
        self.what_rotate = StringVar(self.window)
        self.what_rotate.set(OPTIONS_rotate[1])
        self.option_menu4 = ttk.OptionMenu(self.window, self.what_rotate, *OPTIONS_rotate)
        self.option_menu4.grid(row=4, column=3)

        self.rotate_button = ttk.Button(self.window, text='Rotate', command=self.rotate_action)
        self.rotate_button.grid(row=3, column=1)
        self.rotate_button2 = ttk.Button(self.window, text='Rotate line', command=self.rotate_line_action)
        self.rotate_button2.grid(row=4, column=1)

        self.label5 = ttk.Label(self.window, text='p1: ')
        self.label5.grid(row=3, column=4)
        self.p1_x = Entry(self.window, width=5)
        self.p1_x.grid(row=3, column=5)
        self.p1_y = Entry(self.window, width=5)
        self.p1_y.grid(row=3, column=6)
        self.p1_z = Entry(self.window, width=5)
        self.p1_z.grid(row=3, column=7)

        self.label6 = ttk.Label(self.window, text='p2: ')
        self.label6.grid(row=4, column=4)
        self.p2_x = Entry(self.window, width=5)
        self.p2_x.grid(row=4, column=5)
        self.p2_y = Entry(self.window, width=5)
        self.p2_y.grid(row=4, column=6)
        self.p2_z = Entry(self.window, width=5)
        self.p2_z.grid(row=4, column=7)

        # ОТРАЖЕНИЕ
        self.reflection_button = ttk.Button(self.window, text='Отражение', command=self.reflection_action)
        self.reflection_button.grid(row=6, column=1)
        OPTIONS_xyz_reflection = [
            "",
            "xy",
            "xz",
            "yz"
        ]
        self.label3 = ttk.Label(self.window, text='Отражение относительно: ')
        self.label3.grid(row=6, column=3)
        self.what_xyz_reflection = StringVar(self.window)
        self.what_xyz_reflection.set(OPTIONS_xyz_reflection[1])
        self.option_menu5 = ttk.OptionMenu(self.window, self.what_xyz_reflection, *OPTIONS_xyz_reflection)
        self.option_menu5.grid(row=7, column=3)

        # МАСШТАБИРОВАНИЕ
        self.scale_button = ttk.Button(self.window, text='Scale', command=self.scale_action)
        self.scale_button.grid(row=8, column=1)

        ttk.Label(self.window, text="Scale: ").grid(row=8, column=2)
        self.scale_input = Entry(self.window, width=7)
        self.scale_input.insert(0, "50")
        self.scale_input.grid(row=9, column=2)

        # ttk.Label(self.window, text="x: ").grid(row=2, column=2)
        # Label(self.window, text="y: ").grid(row=3, column=2)
        # Label(self.window, text="angle: ").grid(row=2, column=4)
        # Label(self.window, text="scale: ").grid(row=3, column=4)
        # self.x_input_box = Entry(self.window)
        # self.y_input_box = Entry(self.window)
        # self.x_input_box.insert(0, "100")
        # self.y_input_box.insert(0, "100")
        # self.x_input_box.grid(row=2, column=3)
        # self.y_input_box.grid(row=3, column=3)
        #
        # self.angle_input_box = Entry(self.window)
        # self.angle_input_box.insert(0, "180")
        # self.angle_input_box.grid(row=2, column=5)
        #
        # self.scale_input_box = Entry(self.window)
        # self.scale_input_box.insert(0, "2")
        # self.scale_input_box.grid(row=3, column=5)
        #
        # self.shift_button = Button(self.window, text='Shift', command=self.shift)
        # self.shift_button.grid(row=3, column=1)
        #
        # self.shift_button = Button(self.window, text='Point Rotate', command=self.point_rotate)
        # self.shift_button.grid(row=4, column=1)
        #
        # self.shift_button = Button(self.window, text='Rotate', command=self.rotate)
        # self.shift_button.grid(row=5, column=1)
        #
        # self.shift_button = Button(self.window, text='Point Scale', command=self.point_scale)
        # self.shift_button.grid(row=4, column=2)
        #
        # self.shift_button = Button(self.window, text='Scale', command=self.scale)
        # self.shift_button.grid(row=5, column=2)
        #
        # self.shift_button = Button(self.window, text='Segment Rotate 90', command=self.segment_rotate_90)
        # self.shift_button.grid(row=1, column=3)
        #
        # self.shift_button = Button(self.window, text='Segments Intersection', command=self.segments_intersection)
        # self.shift_button.grid(row=1, column=4)
        #
        # self.shift_button = Button(self.window, text='In Convex Polygon', command=self.in_convex_polygon)
        # self.shift_button.grid(row=0, column=1)
        #
        # self.shift_button = Button(self.window, text='In Concave Polygon', command=self.in_concave_polygon)
        # self.shift_button.grid(row=0, column=3)
        #
        # self.shift_button = Button(self.window, text='Point Position', command=self.point_position)
        # self.shift_button.grid(row=4, column=3)

        self.window.mainloop()

    def ok(self):
        print("value is: " + self.what_figure.get())

    def rotate_action(self):
        angle = int(self.angle_input.get())

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
        angle = int(self.angle_input.get())

        p1 = P(x=int(self.p1_x.get()), y=int(self.p1_y.get()), z=int(self.p1_z.get()))
        p2 = P(x=int(self.p2_x.get()), y=int(self.p2_y.get()), z=int(self.p2_z.get()))
        self.canvas.create_line(p1.x, p1.y, p2.x, p2.y)

        self.figure.rotationL(p1=p1, p2=p2, angle=angle)
        self.plot_figure()

    def reflection_action(self):
        key = 2
        if self.what_xyz_reflection.get() == 'xy':
            key = 0
        elif self.what_xyz_reflection.get() == 'xz':
            key = 1
        elif self.what_xyz_reflection.get() == 'yz':
            key = 2
        self.figure.reflection(key=key)
        self.plot_figure()

    def scale_action(self):
        scale = int(self.scale_input.get())
        self.figure.scaleC(xscale=scale, yscale=scale, zscale=scale)
        self.plot_figure()

    def clear_window(self):
        self.canvas.delete("all")

    def plot_figure(self):
        """
        Отрисовка изменённой фигуры
        """
        self.clear_window()
        obj = self.figure.setcenter(300, 300, 0).rotationXYZ(20, 60, 60)
        pnts, edgs = obj.projection(tp=self.proection, key=self.xyz)
        for e in edgs:
            p1 = pnts[e[0]]
            p2 = pnts[e[1]]
            self.canvas.create_line(p1.x, p1.y, p2.x, p2.y)

    def left_button_release(self, event):
        """
        Установка фигуры по левому нажатию мыши
        """
        self.figure = Tetrahedron()
        if self.what_figure.get() == "Тетраэдр":
            self.figure = Tetrahedron()
        elif self.what_figure.get() == "Гексаэдр":
            self.figure = Hexahedron()
        elif self.what_figure.get() == "Октаэдр":
            self.figure = Octahedron()
        elif self.what_figure.get() == "Икосаэдр":
            self.figure = Icosahedron()
        elif self.what_figure.get() == "Додекаэдр":
            self.figure = Dodecahedron()

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
        self.plot_figure()
                
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
                self.canvas.create_oval(x+1,y+1,x-1,y-1, fill="green", width=2)
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
            print(self.point_x, self.point_y)
            if findside(self.points[0], self.points[1], self.point_x, self.point_y):
                Label(self.window, text="Right").grid(row=4, column=4)
            else:
                Label(self.window, text="Left").grid(row=4, column=4)
        else:
            Label(self.window, text="Draw A Valid Segment").grid(row=4, column=4)


if __name__ == '__main__':
    Gui()
