import numpy as np
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw
from timeit import default_timer as timer


class P2:

    def __init__(self, x, y):
        self.x = x
        self.y = y


class Horizon:
    WIDTH = 400
    HEIGHT = 300

    def __init__(self, func):
        self.window = Tk()

        self.canvas = Canvas(self.window, width=self.WIDTH, height=self.HEIGHT, background='white')
        self.canvas.grid(row=0, column=0)

        self.image = Image.new('RGB', (self.WIDTH, self.HEIGHT), 'white')
        self.draw = ImageDraw.Draw(self.image)

        self.func = func
        self.upHorizon = np.full(shape=self.WIDTH, fill_value=np.NaN)
        self.downHorizon = np.full(shape=self.WIDTH, fill_value=np.NaN)

        # угла для отображения
        self.phi: float = 60.
        self.psi: float = 100.

        start_time = timer()
        self.draw_graphic()
        duration = timer() - start_time
        print("\nDuration: {:g} secs".format(duration))

        # ПОВОРОТ
        ttk.Label(self.window, text="X: ").grid(row=4, column=1)
        self.x_input = Entry(self.window, width=7)
        self.x_input.insert(0, "10")
        self.x_input.grid(row=4, column=2)

        ttk.Label(self.window, text="Y: ").grid(row=5, column=1)
        self.y_input = Entry(self.window, width=7)
        self.y_input.insert(0, "10")
        self.y_input.grid(row=5, column=2)

        self.rotate_button = ttk.Button(self.window, text='Rotate', command=self.rotate_action)
        self.rotate_button.grid(row=10, column=2)

        # self.clear_button = ttk.Button(self.window, text='Clear', command=self.erase)
        # self.clear_button.grid(row=15, column=2)

        self.window.mainloop()

    def rotate_action(self):
        self.erase()

        on_x = int(self.x_input.get())
        on_y = int(self.y_input.get())

        self.psi += on_x
        self.phi += on_y

        start_time = timer()
        self.draw_graphic()
        duration = timer() - start_time
        print("\nDuration: {:g} secs".format(duration))

    def erase(self):
        self.image = Image.new('RGB', (self.WIDTH, self.HEIGHT), 'white')
        self.draw = ImageDraw.Draw(self.image)

        self.canvas.image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, image=self.canvas.image, anchor='nw')

    def draw_graphic(self):
        # Заполняем границы горизонты
        self.upHorizon: np.array = np.full(shape=self.WIDTH, fill_value=0)
        self.downHorizon: np.array = np.full(shape=self.WIDTH, fill_value=1000)

        for x in np.arange(-3, 3.001, 0.2):
            current_curve = list()

            for y in np.arange(-3, 3.001, 0.2):
                z: float = self.func(x, y)

                # отображение координат на данной проекции
                _phi: float = self.phi * np.pi / 180
                _psi: float = self.psi * np.pi / 180

                fx: float = x * np.cos(_psi) - (-np.sin(_phi) * y + np.cos(_phi) * z) * np.sin(_psi)
                fy: float = y * np.cos(_psi) + z * np.sin(_phi)
                k: float = 50.

                p1 = int(np.round(self.WIDTH / 2 + fx * k))
                p2 = int(np.round(self.HEIGHT / 2 + fy * k))

                current_curve.append(P2(p1, p2))
            self.draw_curve(curve=current_curve)

    def draw_curve(self, curve):
        for i in range(1, len(curve)):
            p1: P2 = curve[i - 1]
            p2: P2 = curve[i]

            x1: int = p1.x
            x2: int = p2.x
            y1: int = p1.y
            y2: int = p2.y

            need_change: bool = np.abs(y2 - y1) > np.abs(x2 - x1)

            if need_change:
                x1, y1 = y1, x1
                x2, y2 = y2, x2
            if x1 > x2:
                x1, x2 = x2, x1
                y1, y2 = y2, y1

            # находим градиент
            df: float = (y2 * 1. - y1) / (x2 * 1. - x1)
            y: float = y1 + df

            for x in np.arange(x1 + 1, x2):
                if need_change:
                    xx1: int = int(np.round(y))
                    xx2: int = int(np.round(y))
                    yy1: int = int(x)
                    yy2: int = int(x)
                else:
                    xx1: int = int(np.round(x))
                    xx2: int = int(np.round(x))
                    yy1: int = int(np.round(y))
                    yy2: int = int(np.round(y + 1))

                if xx1 < 0 or xx2 < 0 or yy1 < 0 or yy2 < 0:
                    continue

                if xx1 >= self.WIDTH or xx2 >= self.WIDTH or yy1 >= self.HEIGHT or yy2 >= self.HEIGHT:
                    continue

                if yy1 >= self.upHorizon[xx1] and yy2 >= self.upHorizon[xx2]:
                    self.draw.point([(xx2, yy2)], (1, 1, 1))
                    self.upHorizon[xx1] = yy1
                    self.upHorizon[xx2] = yy2

                elif yy1 <= self.downHorizon[xx1] and yy2 <= self.downHorizon[xx2]:
                    self.draw.point([(xx1, yy1)], (1, 1, 1))
                    self.draw.point([(xx2, yy2)], (1, 1, 1))
                    self.downHorizon[xx1] = yy1
                    self.downHorizon[xx2] = yy2

                self.canvas.image = ImageTk.PhotoImage(self.image)
                self.canvas.create_image(0, 0, image=self.canvas.image, anchor='nw')

                y += df


if __name__ == '__main__':
    start_time = timer()

    func = lambda x, y: np.cos(np.sqrt(x * x + y * y))
    Horizon(func=func)

    duration = timer() - start_time
    print("\nDuration: {:g} secs".format(duration))
