from tkinter import *
from math import sin, cos, pi, hypot, asin, acos, radians, degrees
from random import uniform, randint
from time import time

def circle_coord(x, y, r):
	return x-r, y-r, x+r, y+r

def calcDeg(Ln, start=0):
	def easy(x):
		if x >= 0: return 1
		else: return -1
	def repair(x):
		if x<0: return 360+x
		else: return x
	c = (Ln[2]-Ln[0])/hypot(Ln[1]-Ln[3], Ln[0]-Ln[2])
	s = (Ln[3]-Ln[1])/hypot(Ln[1]-Ln[3], Ln[0]-Ln[2])
	recovery=acos(c)*easy(s)-radians(start)
	dgc=acos(cos(recovery))
	elojel=sin(recovery)
	return repair(degrees(dgc*easy(elojel)))

def get_point(i):
	r=uniform(0, pi*2/point_pcs)+i*pi*2/point_pcs
	d=uniform(min_size, max_size)
	a, b = cos(r)*d+kx, sin(r)*d+ky
	return [a, b]
	
def get_shape():
	return [get_point(i) for i in range(point_pcs)]
	
def out_of_range(x, y, i):
	if mode==1:
		return x<0 or x>width or y<0 or y>height
	elif mode==2:
		min_border= i/point_pcs*360
		max_border=(i+1)/point_pcs*360
		angle=calcDeg([kx, ky, x, y])
		distance=hypot(x-kx, y-ky)
		return distance>=max_size or distance<=min_size or angle<=min_border or angle>=max_border

def move_enemy(enemy):
	global points
	bumszli= bumszlik[enemies.index(enemy)]
	points = [[rajz.coords(enemy['object'])[i*2+j] for j in range(2)] for i in range(point_pcs)]
	new_points=[]
	directions=enemy['directions']
	for i in range(point_pcs):
		x, y = points[i]
		angle = directions[i]
		if out_of_range(x, y, i):
			directions[i]+=pi/2
			angle+=pi/2
		x, y = x+cos(angle)*speed, y+sin(angle)*speed
		rajz.coords(bumszli[i], circle_coord(x, y, br))
		new_points+=[x,y]
		if randint(0, 100)<fordindex:
			directions[i] += uniform(-ford, ford)
	rajz.coords(enemy['object'], new_points)
	
def move_all():
	for enemy in enemies:
		move_enemy(enemy)
		
#rajz.create_oval(circle_coord(kx, ky, alap_r), outline='red', fill='black')

ablak=Tk()

width = ablak.winfo_screenwidth()
height = ablak.winfo_screenheight()
rajz=Canvas(width=width, height=height, bg='black', highlightthickness=0)
rajz.pack()
alap_x, alap_y=width/2, height/2

speed=3
fordindex=50
ford=0.1
point_pcs=5
enemy_pcs=1

min_size=200
max_size=350

mode=2

alap_r = 50
br=10

kx, ky = alap_x, alap_y
stopped=0

rajz.create_oval(circle_coord(alap_x, alap_y, max_size), fill='black', outline='white')
		
enemies=[{'object':rajz.create_polygon(get_shape(), fill='black', outline="white", width=3), 
					'directions':[uniform(0, 2*pi) for i in range(point_pcs)]} 
					for i in range(enemy_pcs)]

rajz.create_oval(circle_coord(alap_x, alap_y, min_size), fill='black', outline='white')
for i in range(point_pcs):
	border= i/point_pcs*2*pi
	rajz.create_line(alap_x+cos(border)*min_size, alap_y+sin(border)*min_size, alap_x+cos(border)*max_size, alap_y+sin(border)*max_size, fill='white')
	
bumszlik=[[rajz.create_oval(circle_coord(rajz.coords(enemy['object'])[i*2], rajz.coords(enemy['object'])[i*2+1], br), outline='white', fill='white') for i in range(point_pcs)] for enemy in enemies]
					
def click(event):
	global stopped
	if stopped: stopped=False
	else: stopped=True

rajz.bind('<Button-1>', click)
	
def main():
	while True:
		ablak.update()
		if not stopped:
			move_all()
	
main()