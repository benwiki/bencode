from tkinter import *
from time import sleep

root=Tk()
w, h = root.winfo_screenwidth(), root.winfo_screenwidth()
draw=Canvas(width=w, height=h, bg='white')
draw.pack()

def click(event):
	global can_move; can_move=True
	
	#first_click=[event.x, event.y]
	
def release(event):
	global lastcoord; lastcoord=None
	global can_move; can_move=False
	
def subtract(a, b):
	return a[0]-b[0], a[1]-b[1]

def move_grid(grid, event):
	global lastcoord
	if not can_move:
		return 0
	if lastcoord is not None:
		x_move, y_move = event.x-lastcoord[0], event.y-lastcoord[1]
		v1, v2 = draw.coords(grid[0])[1:4:2]
		h1, h2 = draw.coords(grid[1])[0:3:2]
		for item in grid:
			if v1+x_move>0:
				draw.move(item, 0, -w/density)
			elif v2+x_move<h:
				draw.move(item, 0, w/density)
			if h1+y_move>0:
				draw.move(item, -w/density, 0)
			elif h2+y_move<w:
				draw.move(item, w/density, 0)
			draw.move(item, x_move, y_move)
	lastcoord=[event.x, event.y]
		
	
def set_grid(density=10, width=2, color='#777777', correct_line=2):
	grid=[]
	d = w/density
	starting_p=(correct_line-1)*d
	for i in range(density-1+correct_line*2):
		grid.append(draw.create_line(i*d-starting_p, -d*correct_line, i*d-starting_p, w+d*correct_line, width=width, fill=color))
		grid.append(draw.create_line(-d*correct_line, i*d-starting_p, w+d*correct_line, i*d-starting_p, width=width, fill=color))
		root.update()
	#	sleep(1)
	return grid
	
draw.bind("<Button-1>", click)
draw.bind("<ButtonRelease-1>", release)
draw.bind("<Motion>", lambda event: move_grid(grid, event))
	
density=10
lastcoord=None
can_move=False
grid=set_grid(density=density)
mainloop()