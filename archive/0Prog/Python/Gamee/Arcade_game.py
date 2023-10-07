from tkinter import *
from math import pi, sin, cos
from time import time
from PIL import Image

ablak=Tk()
ablak.config(bg='white')
lastcoord=[-1, -1]
grabbed=False

radius=130

bullet_len=60
bullet_num=4
bullet_speed=20
bullet_width=3
bullet_color="#ffffff"

timeborder=0.01
shoot_time_period=0.4
time_to_shoot=time()+shoot_time_period

rogzit=time()

bullets=[]
rem=[]
bigrem=[]

def coord(arg1=None, arg2=None, r=0):
	if isinstance(arg1, tuple) or isinstance(arg1, list):
		x1, y1, x2, y2 = arg1
		r=arg2
		return x1+r, y1+r
	else:
		x, y = arg1, arg2
		return x-r, y-r, x+r, y+r
	
def click(event):
	x1, y1, x2, y2=rajz.coords(circle)
	if (event.x > x1 and event.x < x2 and 
		 event.y > y1 and event.y <y2):
		#rajz.itemconfig(lampa, state=HIDDEN)
		rajz.itemconfig(kep, image=csete_duhi)
		global grabbed; grabbed=True

def motion(event):
	"""global lastcoord
	if lastcoord!=[-1, -1]:
		rajz.create_line(lastcoord+[event.x, event.y], width=5, capstyle=ROUND, fill='white')
	lastcoord[0]=event.x
	lastcoord[1]=event.y"""
	"""x1, y1, x2, y2=rajz.coords(circle)
	if (event.x > x1 and event.x < x2 and 
		 event.y > y1 and event.y <y2):
		global grabbed; grabbed=True"""
	if grabbed:
		x, y = event.x, event.y
		if x < radius:
			x = radius
		elif x > width-radius:
			x = width-radius
		if y < radius:
			y = radius
		elif y > height-radius:
			y = height-radius
		rajz.coords(circle, coord(x, y, radius))
		rajz.coords(kep, x, y)
		
def release(event):
	#rajz.itemconfig(lampa, state=NORMAL)
	rajz.itemconfig(kep, image=csete_nyugi)
	global grabbed; grabbed=False

def bullet_coord(i):
	x, y = coord(rajz.coords(circle), radius)
	deg = -(i/(bullet_num+1)*pi)
	x1, y1 = x+cos(deg)*radius, y+sin(deg)*radius
	x2, y2 = x1, y1-bullet_len
	return x1-bullet_width, y1, x2+bullet_width, y2
	
def animation():
	global rem, bigrem, rogzit
	while time()-rogzit<timeborder:
		ablak.update()
	#rajz.coords(iteration_time, 50, 20, int(1/(time()-rogzit)*5), 20)
	rogzit=time()
	for bullet in bullets:
		for line in bullet:
			if rajz.coords(line)[1]>0:
				rajz.move(line, 0, -bullet_speed)
			else:
				rajz.delete(line)
				rem.append(line)
		for r in rem:
			bullet.remove(r)
		rem=[]
	for bullet in bullets:
		if bullet==[]:
			bullets.remove(bullet)
			
def check_shoot():
	global time_to_shoot
	if grabbed:
		if time_to_shoot-time()<0:
			time_to_shoot=time()+shoot_time_period
			bullets.append([rajz.create_oval(bullet_coord(i+1), fill=bullet_color, outline=bullet_color, width=1) for i in range(bullet_num)])

width = ablak.winfo_screenwidth()
height = ablak.winfo_screenheight()
rajz=Canvas(width=width, height=height, bg='black', highlightthickness=0)
rajz.pack()

circle=rajz.create_oval(coord(width/2, height/2, radius), width=3, outline='white')

csete1=Image.open('Csete_nyugodt.gif')
csete1= csete1.resize((width/4, width/4), Image.ANTIALIAS)
#csete_nyugi=PhotoImage(file='Csete_nyugodt.gif')
csete_nyugi=PhotoImage(csete1)
csete_duhi=PhotoImage(file='Csete_duhos.gif')
kep=rajz.create_image(width/2, height/2, image=csete_nyugi)

#lampa=rajz.create_oval(0, 0, 40, 40, fill='red', state=HIDDEN)
#iteration_time=rajz.create_line(50, 20, 50, 20, width=40, fill='red')

rajz.bind("<Button-1>", click)
rajz.bind("<Motion>", motion)
rajz.bind("<ButtonRelease-1>", release)

while 1:
	ablak.update()
	animation()
	check_shoot()