import tkinter as tk
from random import choice
from math import hypot

class Experiment(tk.Tk):
    def __init__(self):
        super().__init__()
        self.w, self.h = self.winfo_screenwidth(), self.winfo_screenheight()
        self.draw = tk.Canvas(width=self.w, height=self.h, bg='black')
        self.draw.pack()
        self.circles = {}
        self.colchanged = {}
        self.draw.bind('<Motion>', self.mouse_click)
        self.draw_cross()
        self.after(0, self.start)

    def mouse_click(self, event):
        circle = self.draw.create_rectangle((event.x-20, event.y-20, event.x+20, event.y+20), outline='red')
        x, y = event.x - self.w/2, event.y - self.h/2
        d = hypot(x, y)/8
        self.circles[circle] = (x/d, y/d)

    def start(self):
        for circle in self.circles:
            x_speed, y_speed = self.circles[circle]
            self.draw.move(circle, x_speed, y_speed)
            x, y, x2, y2 = self.draw.coords(circle)
            cx, cy = (x + x2)/2, (y + y2)/2
            if x2 < 0:
                self.draw.move(circle, self.w + 40, 2 * (self.h/2 - cy))
            if x > self.w:
                self.draw.move(circle, -self.w - 40, 2 * (self.h/2 - cy))
            if y2 < 0:
                self.draw.move(circle, 2 * (self.w/2 - cx), self.h + 40)
            if y > self.h:
                self.draw.move(circle, 2 * (self.w/2 - cx), -self.h - 40)
            if circle not in self.colchanged and (x2 < 0 or x > self.w or y2 < 0 or y > self.h):
                self.draw.itemconfig(circle, outline=choice(('white', 'lightgreen', 'green', 'lightblue', 'blue', 'yellow', 'orange')))
                self.colchanged[circle] = None
        self.update()
        self.after(0, self.start)

    def draw_cross(self):
        self.draw.create_line(self.w/2-20, self.h/2, self.w/2+20, self.h/2, fill='red', width=3)
        self.draw.create_line(self.w/2, self.h/2-20, self.w/2, self.h/2+20, fill='red', width=3)

exp = Experiment()
exp.mainloop()
