from tkinter import *
from math import pi, cos, sin, hypot
from random import uniform, randint
from time import time

outer_points_num = 15
r_min = 10
r_max = 30
circles=[]
start=0
clear_time=0.7

def circle_coord(x, y, r):
	return x-r, y-r, x+r, y+r

def click(event):
	global start
	start = time()
	
def release(event):
	global start
	if start==0:
		return 0
	start=0
	
	r = uniform(r_min, r_max)
	x, y = event.x, event.y
	choose_points = list(points)
	point_pcs = len(points)
	bind_num = 5
		
	for i in range(bind_num):
		bind=randint(0, len(choose_points)-1)
		draw.create_line(choose_points[bind] + [x, y], width=5)
		choose_points.pop(bind)
		
	circles.append(draw.create_oval(circle_coord(x, y, r), fill='white',outline='white'))
	for c in circles:
		draw.tag_raise(c)
			
	points.append([x, y])
	

def random_angle():
	return uniform(0, 2*pi)

window=Tk()

width = window.winfo_screenwidth()
height = window.winfo_screenheight()
draw=Canvas(width=width, height=height, bg='#0077bb', highlightthickness=0)
draw.pack()

radius = hypot(width/2, height/2)

random_angles= [random_angle() for i in range(outer_points_num)]

points = [[ width/2 + cos(angle)*radius,
				   height/2 + sin(angle)*radius ] 
				for angle in random_angles]

draw.bind("<Button-1>", click)
draw.bind("<ButtonRelease-1>", release)

while 1:
	window.update()
	if start>0 and time()-start>clear_time:
		draw.delete(ALL)
		start=0
		points=[[width/2 + cos(angle)*radius,
				       height/2 + sin(angle)*radius] 
						for angle in random_angles]