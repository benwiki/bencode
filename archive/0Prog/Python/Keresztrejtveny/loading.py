from tkinter import *
from time import sleep
from math import sin, cos, pi
from random import randint
ablak=Tk()
w, h=700,700
rajz=Canvas(width=w, height=h, bg='black')
rajz.pack()
	
def colorizer(a, b, choice, ground=1):
	arnyalat=255*a/b
	part=''
	if ground:
		g='ff'
		arnyalat=255-arnyalat
	else:
		g='00'
	if arnyalat<16:
		part+='0'
	part+=str(hex(int(arnyalat)))[2:]
	if choice=='red':
		col=part+2*g
	elif choice=='green':
		col=g+part+g
	elif choice=='blue':
		col=2*g+part
	elif choice=='yellow':
		col=2*part+g
	elif choice=='magenta':
		col=part+g+part
	elif choice=='cyan':
		col=g+2*part
	else:
		col=3*part
	return "#"+col

def loading(x, y, start, extent, color, db=150, r=100, lines=None):
	if lines is None:
		lines=[]
	start=int(db*start/100)
	extent=int(db*extent/100)
	teljesszog=2*pi
	for i in range(start, extent):
		arany=i/(db/2)
		if i<db/2:
			if i>db*5/16:
				rajz.delete(lines[0])
				lines.remove(lines[0])
			x1=x + cos(arany*teljesszog)*r
			y1=y + sin(arany*teljesszog)*r
			x2=x + cos(arany*teljesszog)*r*(1-arany)
			y2=y + sin(arany*teljesszog)*r*(1-arany)
		else:
			rajz.delete(lines[0])
			lines.remove(lines[0])
			x1, y1=x, y
			x2=x + cos(arany*teljesszog)*r*(2-arany)
			y2=y + sin(arany*teljesszog)*r*(2-arany)
		lines.append(rajz.create_line(x1, y1, x2, y2, width=20, fill=colorizer(i, db, color, 0), capstyle=ROUND))
		ablak.update()
		sleep(0.03)
	return lines
	
def loading2(x, y, color='', colground=1, db=30, r=100, wid=22):
	def line(i):
		ablak.update()
		sleep(0.006)
		deg=i/db*pi
		return rajz.create_line(x+cos(deg)*r, 
											y+sin(deg)*r, 
											x+cos(deg)*-r, 
											y+sin(deg)*-r, 
											width=wid, 
											fill=colorizer(i, db, color, colground))
	lines=[line(i) for i in range(db)]
	while 1:
		rajz.tag_raise(lines[0])
		lines=lines[1:]+[lines[0]]
		for i in range(db):
			rajz.itemconfig(lines[i], fill=colorizer(i, db, color, colground))
		ablak.update()
		sleep(0.03)
	mainloop()
	
#loading2(w/2, h/2, 'cyan', 0)
colors=['red', 'green', 'blue', 'cyan', 'magenta', 'yellow', 'white']

while 1:
	lines=loading(w/2, h/2, 0, 97, colors[randint(0, len(colors)-1)])
	for L in lines:
		rajz.delete(L)
		ablak.update()
		sleep(0.03)