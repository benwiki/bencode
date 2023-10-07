import tkinter as tk
from math import sin, cos, pi

root = tk.Tk()
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
draw = tk.Canvas(width=w, height=h)
draw.pack()

coord = lambda x, y, r: (x-r, y-r, x+r, y+r)

getCoord = lambda i, rot: coord(w/2+cos((i/numPts+rot)*2*pi)*r, h/2+sin((i/numPts+rot)*2*pi)*r, ptR)

r = 200
ptR = 50
numPts = 5
pointCoords = [getCoord(i, 0) for i in range(numPts)]
points = [draw.create_oval(ptCoord, fill="black") for ptCoord in pointCoords]

def rotate(event):
	for i, point in enumerate(points):
		draw.coords(point, getCoord(i, event.x / w))

draw.bind('<Motion>', rotate)

tk.mainloop()
