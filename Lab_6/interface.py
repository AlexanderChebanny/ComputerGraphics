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
        self.what_scale = None

        self.x_shift = 300.0
        self.y_shift = 300.0
        self.z_shift = 300.0

        self.x_scale = 1.0
        self.y_scale = 1.0
        self.z_scale = 1.0

        self.window.title("MECHMAT SILA")
        self.window.resizable(False, False)
        # canvas
        self.canvas = Canvas(self.window, width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT)   # , background='white'
        self.canvas.grid(row=0, column=0)
        # mouse clicks
        self.canvas.bind("<ButtonRelease-1>", self.left_button_release)
        
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
        self.p2_x.insert(0, "0")
        self.p2_y = Entry(self.window, width=5)
        self.p2_y.grid(row=4, column=6)
        self.p2_y.insert(0, "0")
        self.p2_z = Entry(self.window, width=5)
        self.p2_z.grid(row=4, column=7)
        self.p2_z.insert(0, "0")

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

        # СДВИГ
        self.reflection_button = ttk.Button(self.window, text='Сдвиг', command=self.shift_action)
        self.reflection_button.grid(row=8, column=1)

        ttk.Label(self.window, text="Shift: ").grid(row=8, column=3)

        self.label7 = ttk.Label(self.window, text='X: ')
        self.label7.grid(row=8, column=4)
        self.shift_x = Entry(self.window, width=5)
        self.shift_x.grid(row=8, column=5)
        self.shift_x.insert(0, "0")

        self.label8 = ttk.Label(self.window, text='Y: ')
        self.label8.grid(row=8, column=6)
        self.shift_y = Entry(self.window, width=5)
        self.shift_y.grid(row=8, column=7)
        self.shift_y.insert(0, "0")

        self.label9 = ttk.Label(self.window, text='Z: ')
        self.label9.grid(row=8, column=8)
        self.shift_z = Entry(self.window, width=5)
        self.shift_z.grid(row=8, column=9)
        self.shift_z.insert(0, "0")

        # МАСШТАБИРОВАНИЕ
        self.scale_button = ttk.Button(self.window, text='Scale', command=self.scale_action)
        self.scale_button.grid(row=10, column=1)

        ttk.Label(self.window, text="Scale: ").grid(row=10, column=3)

        self.label10 = ttk.Label(self.window, text='X: ')
        self.label10.grid(row=10, column=4)
        self.scale_x = Entry(self.window, width=5)
        self.scale_x.grid(row=10, column=5)
        self.scale_x.insert(0, "1")

        self.label11 = ttk.Label(self.window, text='Y: ')
        self.label11.grid(row=10, column=6)
        self.scale_y = Entry(self.window, width=5)
        self.scale_y.grid(row=10, column=7)
        self.scale_y.insert(0, "1")

        self.label12 = ttk.Label(self.window, text='Z: ')
        self.label12.grid(row=10, column=8)
        self.scale_z = Entry(self.window, width=5)
        self.scale_z.grid(row=10, column=9)
        self.scale_z.insert(0, "1")

        self.window.mainloop()

    def ok(self):
        print("value is: " + self.what_figure.get())

    def shift_action(self):
        """
        Сдвиг
        """
        self.x_shift += float(self.shift_x.get())
        self.y_shift += float(self.shift_y.get())
        self.z_shift += float(self.shift_z.get())

        self.figure.shift(xshift=self.x_shift-300, yshift=self.y_shift-300, zshift=self.z_shift-300)
        self.plot_figure()

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

        print(key)
        self.figure.rotation(angle=angle, key=key)
        self.plot_figure()

    def rotate_line_action(self):
        """
        Поворот относительно линии
        """
        angle = float(self.angle_input.get())

        p1 = P(x=float(self.p1_x.get()), y=float(self.p1_y.get()), z=float(self.p1_z.get()))
        p2 = P(x=float(self.p2_x.get()), y=float(self.p2_y.get()), z=float(self.p2_z.get()))
        self.canvas.create_line(p1.x, p1.y, p2.x, p2.y)

        self.figure.rotationL(p1=p1, p2=p2, angle=angle)
        self.plot_figure()

    def reflection_action(self):
        """
        Отражение
        """
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
        """
        Масштабирование
        """
        if float(self.scale_x.get()) == 0.0:
            self.x_scale = 0.0
        else:
            self.x_scale *= float(self.scale_x.get())

        if float(self.scale_y.get()) == 0.0:
            self.y_scale = 0.0
        else:
            self.y_scale *= float(self.scale_y.get())

        if float(self.scale_z.get()) == 0.0:
            self.z_scale = 0.0
        else:
            self.z_scale *= float(self.scale_z.get())

        self.figure.scaleC(xscale=self.x_scale, yscale=self.y_scale, zscale=self.z_scale)
        self.plot_figure()

    def clear_window(self):
        """
        Отчистка окна
        """
        self.canvas.delete("all")

    def plot_figure(self):
        """
        Отрисовка изменённой фигуры
        """
        self.clear_window()
        pnts, edgs = self.figure.projection(tp=self.proection, key=self.xyz)

        for e in edgs:
            p1 = pnts[e[0]]
            p2 = pnts[e[1]]
            if self.xyz == 2:
                self.canvas.create_line(p1.x, p1.y, p2.x, p2.y)
            elif self.xyz == 1:
                self.canvas.create_line(p1.x, p1.z, p2.x, p2.z)
            elif self.xyz == 0:
                self.canvas.create_line(p1.y, p1.z, p2.y, p2.z)

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

        self.shift_x.delete(0, END)
        self.shift_x.insert(0, "0")
        self.shift_y.delete(0, END)
        self.shift_y.insert(0, "0")
        self.shift_z.delete(0, END)
        self.shift_z.insert(0, "0")

        self.scale_x.delete(0, END)
        self.scale_x.insert(0, "1")
        self.scale_y.delete(0, END)
        self.scale_y.insert(0, "1")
        self.scale_z.delete(0, END)
        self.scale_z.insert(0, "1")

        self.x_shift = 300.0
        self.y_shift = 300.0
        self.z_shift = 300.0

        self.x_scale = 1.0
        self.y_scale = 1.0
        self.z_scale = 1.0

        self.proection = tp
        self.xyz = key
        self.figure.setcenter(x=300, y=300, z=300)
        self.plot_figure()


if __name__ == '__main__':
    Gui()
