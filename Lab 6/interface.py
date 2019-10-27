from poly3d import *
from tkinter import *
from PIL import Image, ImageTk, ImageDraw


    
class Gui:
    CANVAS_WIDTH = 655
    CANVAS_HEIGHT = 712
    
    def __init__(self):
        self.window = Tk()
        self.full_figure = False
        # point
        self.point = False
        self.point_x = 0
        self.point_y = 0
        self.window.title("MECHMAT SILA")
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
        
        Label(self.window, text="x: ").grid(row=2, column=2)
        Label(self.window, text="y: ").grid(row=3, column=2)
        Label(self.window, text="angle: ").grid(row=2, column=4)
        Label(self.window, text="scale: ").grid(row=3, column=4)
        self.x_input_box = Entry(self.window)
        self.y_input_box = Entry(self.window)
        self.x_input_box.insert(0, "100")
        self.y_input_box.insert(0, "100")
        self.x_input_box.grid(row=2, column=3)
        self.y_input_box.grid(row=3, column=3)

        self.angle_input_box = Entry(self.window)
        self.angle_input_box.insert(0, "180")
        self.angle_input_box.grid(row=2, column=5)
        
        self.scale_input_box = Entry(self.window)
        self.scale_input_box.insert(0, "2")
        self.scale_input_box.grid(row=3, column=5)
        
        self.shift_button = Button(self.window, text='Shift', command=self.shift)
        self.shift_button.grid(row=3, column=1)
        
        self.shift_button = Button(self.window, text='Point Rotate', command=self.point_rotate)
        self.shift_button.grid(row=4, column=1)
        
        self.shift_button = Button(self.window, text='Rotate', command=self.rotate)
        self.shift_button.grid(row=5, column=1)
        
        self.shift_button = Button(self.window, text='Point Scale', command=self.point_scale)
        self.shift_button.grid(row=4, column=2)
        
        self.shift_button = Button(self.window, text='Scale', command=self.scale)
        self.shift_button.grid(row=5, column=2)
        
        self.shift_button = Button(self.window, text='Segment Rotate 90', command=self.segment_rotate_90)
        self.shift_button.grid(row=1, column=3)
        
        self.shift_button = Button(self.window, text='Segments Intersection', command=self.segments_intersection)
        self.shift_button.grid(row=1, column=4)
        
        
        self.shift_button = Button(self.window, text='In Convex Polygon', command=self.in_convex_polygon)
        self.shift_button.grid(row=0, column=1)
        
        self.shift_button = Button(self.window, text='In Concave Polygon', command=self.in_concave_polygon)
        self.shift_button.grid(row=0, column=3)
        
        self.shift_button = Button(self.window, text='Point Position', command=self.point_position)
        self.shift_button.grid(row=4, column=3)
        
        
        self.window.mainloop()
        
    def clear_window(self):
        self.canvas.delete("all")
        self.full_figure = False
        self.points = []
        #self.image = Image.new('RGB', (self.DEFAULT_WIDTH, self.DEFAULT_WIDTH), 'white')
        #self.draw = ImageDraw.Draw(self.image)
        
    def left_button_release(self, event):
        x, y = event.x, event.y
        print(x, y)
        if self.points == []:
            self.points.append([x, y])
            self.canvas.create_oval(x,y,x-1,y-1)
        else:
            x0, y0 = self.points[-1]
            self.canvas.create_line(x0,y0,x,y)
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
        #obj = N_edge()
        #obj.fileread('n_edge_1.txt')
        obj = Tetrahedron().setcenter(300,300,0).rotationXYZ(20, 60, 60)
        #obj
        pnts, edgs = obj.proj_2d()
        for e in edgs:
            p1 = pnts[e[0]]
            p2 = pnts[e[1]]
            self.canvas.create_line(p1.x, p1.y, p2.x, p2.y)
        
                
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
    
