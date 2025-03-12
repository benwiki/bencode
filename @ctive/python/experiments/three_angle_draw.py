from math import *
import tkinter as tk

class Drawer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cucc")
        self.geometry("700x700")
        self.resizable(False, False)
        self.draw = tk.Canvas(self, width=700, height=700)
        self.draw.pack()
        self.hold_it = False
        self.draw.bind("<Motion>", self.motion)
        self.draw.bind("<Button-1>", self.hold)
        self.draw.bind("<ButtonRelease-1>", self.release)
        self.bind("<d>", lambda e: self.draw.delete("all"))
        self.mainloop()

    def hold(self, e):
        self.hold_it = True

    def release(self, e):
        self.hold_it = False

    def motion(self, e):
        if not self.hold_it:
            return
        x, y = e.x, e.y
        w=0
        self.draw.create_oval(x-w, y-w, x+w, y+w)
        a, b = x-350, y-350
        d = hypot(a, b)
        angle = atan2(b,a)
        angle2=angle + 2*pi/3
        angle3=angle2 + 2*pi/3
        nx1, ny1 = 350+d*cos(angle2), 350+d*sin(angle2)
        nx2, ny2 = 350+d*cos(angle3), 350+d*sin(angle3)
        self.draw.create_oval(nx1-w, ny1-w, nx1+w, ny1+w)
        self.draw.create_oval(nx2-w, ny2-w, nx2+w, ny2+w)


Drawer()