import tkinter as tk
from math import sin, cos, pi

root = tk.Tk()
root['bg'] = '#222222'
w, h = root.winfo_screenwidth(), root.winfo_screenheight()*0.75
draw = tk.Canvas(width=w, height=h)
draw.pack()

c1 = "#ffffff"
c2 = "#000000"

cols = ['ff']*3
numcols = [0]*3

def conv(pos: int):
	s = str(hex(pos))
	return s[2:].rjust(2,'0')

def convv(i, pos):
	global cols, numcols
	numcols[i] = int(pos)
	cols[i] = conv(255-int(pos))
	c1='#'+''.join(cols)
	c2='#'+''.join(conv(c) for c in numcols)
	draw.itemconfig(bg, fill=c1)
	draw.itemconfig(bg2, fill=c2)

bg = draw.create_rectangle(0, 0, w, h/2, fill=c1)
bg2 = draw.create_rectangle(0, h/2, w, h, fill=c2)

"""x, y = w/2, h/2
lines=[]
def drawline(event):
	global x, y, lines
	lines.append(
	    draw.create_line(x, y, event.x, event.y, fill=c2, width=20)
	)
	x, y = event.x, event.y
draw.bind("<Motion>", drawline)"""

r, g, b = [tk.Scale(from_=0, to=255, orient=tk.HORIZONTAL, width=90, length=w, sliderlength=150, command=lambda pos, i=i: convv(i, pos), troughcolor=('cyan','magenta','yellow')[i], bg='#222222', fg='white') for i in range(3)]
for comp in r,g,b:
	comp.pack()

"""def clear():
	global lines
	for line in lines:
		draw.delete(line)
	lines = []"""
#tk.Button(text="CLEAR", command=clear).pack()

tk.mainloop()