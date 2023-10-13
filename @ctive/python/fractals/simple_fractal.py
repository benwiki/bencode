from dataclasses import dataclass
import tkinter as tk
from numpy import sin, cos, pi

SIZE = 500

@dataclass
class Point:
    x: float
    y: float
    angle: int | None = None


class FractalApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Fractal App")
        
        self.pts = [Point(SIZE/2, SIZE/2, None)]
        self.size = SIZE/4
        self.n = 4
        self.w, self.h = SIZE, SIZE
        self.canvas = tk.Canvas(self, width=self.w, height=self.h)
        self.canvas.pack()
        self.bind("<space>", self.draw_next_layer)
        self.draw_next_layer()

    def draw_next_layer(self, _=None):
        self.pts = self.draw_fractal_layer(self.pts, self.size)
        self.size /= 2
        self.update()

    def point_on_circle(self, pos: Point, size: float, angle: float):
        return Point(pos.x + size * cos(angle), pos.y + size * sin(angle))

    def draw_fractal(self, depth=1, pos=Point(SIZE/2, SIZE/2), size=SIZE/4, angle=None):
        if depth == 0: return
        for i in range(self.n):
            if angle is not None and i == (angle+2)%self.n:
                continue
            end = self.point_on_circle(pos, size, i/self.n * pi*2)
            self.canvas.create_line(pos.x, pos.y, end.x, end.y)
            self.draw_fractal(depth-1, end, size/2, i)

    def draw_fractal_layer(self, points: list[Point], size=SIZE/4):
        new_points = []
        for p in points:
            for i in range(self.n):
                if p.angle is not None and i == (p.angle+2)%self.n:
                    continue
                end = self.point_on_circle(p, size, i/self.n * pi*2)
                self.canvas.create_line(p.x, p.y, end.x, end.y)
                end.angle = i
                new_points.append(end)
        return new_points


if __name__ == "__main__":
    app = FractalApp()
    # app.draw_fractal(4)
    app.mainloop()
