import tkinter as tk
from math import hypot
from threading import Thread
from time import time


class Experiment(tk.Tk):
    def __init__(self):
        super().__init__()
        self.init_variables()
        self.init_window()
        self.init_bindings()
        
    def init_variables(self):
        self.screenwidth = self.winfo_screenwidth()
        self.screenheight = self.winfo_screenheight()
        self.w = self.screenwidth/2
        self.h = self.screenheight/2
        self.drawing = False
        self.running = True
        self.r = 10
        self.circles = dict()
    
    def init_window(self):
        self.draw = tk.Canvas(
            width=self.w, height=self.h,
            bg='black')
        self.draw.pack()
        
    def init_bindings(self):
        self.draw.bind(
            '<Motion>', self.mouse_click)
        self.draw.bind(
            '<1>', lambda _: self.toggle_draw(True))
        self.draw.bind(
            '<ButtonRelease-1>', lambda _: self.toggle_draw(False))
        self.bind('<Escape>', self.stop)
        self.protocol("WM_DELETE_WINDOW", self.stop)
        
    def mouse_click(self, event):
        if not self.drawing: return
        circle = self.draw.create_oval(
            self.get_circle_coords(event.x, event.y, self.r),
            fill='red')
        x_speed, y_speed = self.normalize(event.x-self.w/2, event.y-self.h/2)
        self.circles[circle] = (x_speed, y_speed)

    def get_circle_coords(self, x, y, r):
        return (x-r, y-r, x+r, y+r)

    def normalize(self, x, y):
        if x==0 and y==0: return (1, 0)
        d = hypot(x, y) 
        return (x/d, y/d)

    def toggle_draw(self, toggle_value):
        self.drawing = toggle_value

    def stop(self, event=None):
        self.running = False
        self.destroy()

    def start(self):
        self.draw_cross()
        while self.running:
            for circle in self.circles.copy():
                (x_speed, y_speed) = self.circles[circle]
                self.draw.move(circle, x_speed, y_speed)
                x, y, x2, y2 = self.draw.coords(circle)
                if x2 < 0 or x > self.w or y2 < 0 or y > self.h:
                    self.draw.delete(circle)
                    self.circles.pop(circle)
            self.update()

    def draw_cross(self):
        self.draw.create_line(
            self.w/2 - self.r, self.h/2, self.w/2 + self.r, self.h/2,
            fill='red')
        self.draw.create_line(
            self.w/2, self.h/2 - self.r, self.w/2, self.h/2 + self.r,
            fill='red')


exp = Experiment()
exp.start()