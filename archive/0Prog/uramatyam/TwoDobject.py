from dataclasses import dataclass, field
import tkinter as tk
import time


@dataclass
class TwoDObject:
    cv: tk.Canvas
    x: float
    y: float
    index: int = field(default=0, init=False)

    def move(self, xchange: float = 0, ychange: float = 0):
        self.x += xchange
        self.y += ychange
        if self.cv and self.index:
            self.cv.move(self.index, xchange, ychange)


@dataclass
class Circle(TwoDObject):
    radius: float

    def __post_init__(self):
        self.index = self.cv.create_oval(self.x - self.radius, self.y - self.radius,
                                         self.x + self.radius, self.y + self.radius)
        assert self.index != 0


@dataclass
class Line(TwoDObject):
    x2: float
    y2: float

    def __post_init__(self):
        self.index = self.cv.create_line(self.x,
                                         self.y,
                                         self.x + self.x2,
                                         self.y + self.y2)
        assert self.index != 0


def setup_canvas(height: int = 600, width: int = 600):
    root = tk.Tk()
    cv = tk.Canvas(root, height=height, width=width)
    cv.pack()
    return cv


def geo_ex() -> int:
    cv = setup_canvas()
    return Circle(cv, 200, 300, radius=50)
