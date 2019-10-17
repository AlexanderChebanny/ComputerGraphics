from tkinter import *
import numpy as np
from PIL import Image, ImageTk, ImageDraw


def B(x, p1, p2, p3, p4):
    #np.array([[-1, 3, -3, 1],[3, -6, 3, 0],[-3, 3, 0, 0],[1, 0, 0, 0]]).dot(np.array([p1, p2, p3, p4])))
    return np.array([x**3, x**2, x, 1]) @ np.array([[-1, 3, -3, 1],[3, -6, 3, 0],[-3, 3, 0, 0],[1, 0, 0, 0]]) @ np.array([p1, p2, p3, p4])

DXDY = 3
CURVE_WIDTH = 2

class Gui:
    CANVAS_WIDTH = 1000
    CANVAS_HEIGHT = 1000
    #DXDY = 3
    def __init__(self):
        self.window = Tk()
        self.full_figure = False
        # point
        self.window.title("MEHMAT SILA")
        self.window.resizable(False, False)
        # current figure
        self.points = []
        # canvas
        self.canvas = Canvas(self.window, width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT-200, background='white')
        self.canvas.grid(row=0, column=0)
        # mouse clicks
        self.canvas.bind("<ButtonRelease-1>", self.left_button_release)
        self.canvas.bind("<ButtonRelease-2>", self.middle_button_release)
        self.canvas.bind("<ButtonRelease-3>", self.right_button_release)
        
        # clear button
        self.clear_button = Button(self.window, text='Clear', command=self.clear_window)
        self.clear_button.grid(row=2, column=1)

        self.window.mainloop()

    def clear_window(self):
        self.canvas.delete("all")
        self.full_figure = False
        self.points = []
        #self.image = Image.new('RGB', (self.DEFAULT_WIDTH, self.DEFAULT_WIDTH), 'white')
        #self.draw = ImageDraw.Draw(self.image)
    
    def left_button_release(self, event):
        x, y = event.x, event.y
        if len(self.points) < 4:
            self.canvas.create_text(x-DXDY*3,y-DXDY*3, text=str(len(self.points) + 1), width=1)
            self.canvas.create_oval(x + DXDY, y + DXDY, x - DXDY, y - DXDY, fill='black')
            self.points.append([x, y])

    def middle_button_release(self, event):
        if self.point:
            self.point = False
            self.polygon()
        self.point = True
        x, y = event.x, event.y
        self.point_x = x
        self.point_y = y
        self.canvas.create_oval(x+1,y+1,x-1,y-1, fill="green")

    def right_button_release(self, event):
        if len(self.points) == 4:
            p1, p2, p3, p4 = self.points
            #num = 
            for t in np.linspace(0, 1.0, num=500):
                x, y = B(t, p1, p2, p3, p4)
                r = CURVE_WIDTH / 2
                self.canvas.create_oval(x+r,y+r,x-r,y-r, fill="red", outline="red")

if __name__ == '__main__':
    Gui()
    #print(B(0.1, [1,2], [3,4], [5,6], [7,8])) 
