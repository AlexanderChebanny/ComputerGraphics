"""
Чебанный Александр и Лысенко Никита 4.8

Лабораторная работа №5. L-системы. Diamond-square. Cплайны

3. Кубические сплайны Безье
Реализовать программу для визуализации составной кубической кривой Безье.
Программа должна позволять добавлять, удалять  и перемещать опорные точки.
"""

from tkinter import *
import numpy as np


DXDY = 3


def the_world_exist():
    return 2 * 2 == 4


def B(x, p1, p2, p3, p4):
    return np.array([x**3, x**2, x, 1]) @ \
           np.array([
               [-1, 3, -3, 1],
               [3, -6, 3, 0],
               [-3, 3, 0, 0],
               [1, 0, 0, 0]
           ]) @ \
           np.array([p1, p2, p3, p4])


def middle_of_line(p1, p2):
    return [(p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2]


class Main:
    size = 700

    def __init__(self):
        self.window = Tk()
        self.full_figure = False
        # point
        self.window.title("MEHMAT SILA")
        self.window.resizable(False, False)
        # current figure
        self.points = list()
        self.bezye_points = list()
        # canvas
        self.canvas = Canvas(self.window, width=self.size, height=self.size, background='white')
        self.canvas.grid(row=0, column=0)
        # mouse clicks
        self.canvas.bind("<ButtonRelease-1>", self.left_button_release)
        # self.canvas.bind("<ButtonRelease-2>", self.right_button_release)
        
        # clear button
        self.clear_button = Button(self.window, text='Clear', command=self.clear_window)
        self.clear_button.grid(row=2, column=1)

        # Go button
        self.clear_button = Button(self.window, text='Go', command=self.go)
        self.clear_button.grid(row=1, column=1)

        self.window.mainloop()

    def clear_window(self):
        self.canvas.delete("all")
        self.full_figure = False
        self.points = list()
        self.bezye_points = list()
    
    def left_button_release(self, event):
        x, y = event.x, event.y
        self.canvas.create_text(x-DXDY*3, y-DXDY*3, text=str(len(self.points) + 1), width=0)
        self.canvas.create_oval(x + DXDY, y + DXDY, x - DXDY, y - DXDY, fill='black')
        self.points.append([x, y])

    def print_middle(self, middle, i):
        self.canvas.create_text(middle[0] - DXDY * 3, middle[1] - DXDY * 3,
                                text=str(i) + '.5', width=0)
        self.canvas.create_oval(middle[0] + DXDY, middle[1] + DXDY, middle[0] - DXDY, middle[1] - DXDY,
                                fill='black')
        self.canvas.update()

    def go(self):
        self.points_for_bazye()
        for i in range(len(self.bezye_points)):
            p1, p2, p3, p4 = self.bezye_points[i]
            for t in np.linspace(0, 1.0, num=500):
                x, y = B(t, p1, p2, p3, p4)
                r = 1
                self.canvas.create_oval(x+r, y+r, x-r, y-r, fill="red", outline="red")

    def points_for_bazyeq(self):
        if len(self.points) == 4:
            self.bezye_points.append([
                self.points[0],
                self.points[1],
                self.points[2],
                self.points[3],
            ])
        else:
            # Обработка первых 3х точек
            middle = middle_of_line(self.points[2], self.points[3])
            # рисуем middle точку
            self.print_middle(middle, 3)
            self.bezye_points.append([
                self.points[0],
                self.points[1],
                self.points[2],
                middle
            ])
            i = 3   # количество пройденных точек

            if len(self.points) % 2 == 0:
                start_point = middle

                while the_world_exist():
                    # если осталось 3 точки, то их и добавляем в конечные точки кривой Безье
                    if len(self.points) - i == 3:
                        self.bezye_points.append([
                            start_point,
                            self.points[i],
                            self.points[i + 1],
                            self.points[i + 2]
                        ])
                        break
                    else:
                        middle = middle_of_line(self.points[i + 1], self.points[i + 2])
                        self.print_middle(middle, i + 2)
                        self.bezye_points.append([
                            start_point,
                            self.points[i],
                            self.points[i + 1],
                            middle
                        ])
                        start_point = middle
                        i += 2

            elif len(self.points) % 2 != 0:
                start_point = middle

                while the_world_exist():
                    # если осталось 2 точки, то их и добавляем в конечные точки кривой Безье
                    if len(self.points) - i == 2:
                        middle = middle_of_line(self.points[-1], self.points[-2])
                        self.print_middle(middle, i + 1)
                        self.bezye_points.append([
                            start_point,
                            self.points[i],
                            middle,
                            self.points[i + 1]
                        ])
                        break
                    else:
                        middle = middle_of_line(self.points[i + 1], self.points[i + 2])
                        self.print_middle(middle, i + 2)
                        self.bezye_points.append([
                            start_point,
                            self.points[i],
                            self.points[i + 1],
                            middle
                        ])
                        start_point = middle
                        i += 2


if __name__ == '__main__':
    Main()

