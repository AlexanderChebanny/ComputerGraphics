from lab4 import *
from tkinter import *
from PIL import Image, ImageTk, ImageDraw


    
class Gui:
    DEFAULT_WIDTH = 1000
    DEFAULT_HEIGHT = 1000
    DEFAULT_COLOR = 'black'
    
    def __init__(self):
        self.window = Tk()
        self.window.title("3DPRO")
        self.window.resizable(False, False)
        #
        self.points = []
        # clear
        self.clear_button = Button(self.window, text='Clear', command=self.clear_window)
        self.clear_button.grid(row=3, column=1)
        
        self.canvas = Canvas(self.window, width=self.DEFAULT_WIDTH, height=self.DEFAULT_HEIGHT-200, background='white')
        self.canvas.grid(row=0, column=0)
         # button
        self.canvas.bind("<ButtonRelease-1>", self.left_button_release)
        self.canvas.bind("<ButtonRelease-3>", self.right_button_release)
        self.canvas.create_line(0,0,400,400)
        
        
        self.window.mainloop()
        
    def clear_window(self):
        self.canvas.delete("all")
        self.points = []
        #self.image = Image.new('RGB', (self.DEFAULT_WIDTH, self.DEFAULT_WIDTH), 'white')
        #self.draw = ImageDraw.Draw(self.image)
        
    def left_button_release(self, event):
        x, y = event.x, event.y
        if self.points == []:
            self.points.append((x, y))
            self.canvas.create_oval(x,y,x-1,y-1)
        else:
            x0, y0 = self.points[-1]
            self.canvas.create_line(x0,y0,x,y)
            self.points.append((x, y))
    
    def right_button_release(self, event):
        if len(self.points) > 2:
            x0, y0 = self.points[-1]
            x, y = self.points[0]
            self.canvas.create_line(x0,y0,x,y)
            
if __name__ == '__main__':
    Gui()
    
