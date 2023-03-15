from tkinter import *
from time import sleep
from math import sin, cos, pi
ablak=Tk()
w, h=700,700
rajz=Canvas(width=w, height=h, bg='black')
rajz.pack()

def coloring(a, b):
	which = 255*5*(a/b)
	if a==1:
		which= 0
	if which <256:
		color='#0000'
		if which<16:
			color+='0'
		color+= (str(hex(int(which)))[2:])
	elif which <511:
		color='#00'
		which -=255
		if which<16:
			color+='0'
		color+= (str(hex(int(which)))[2:])
		color+='ff'
	elif which <766:
		color='#00ff'
		which-=510
		which= 255-which
		if which<16:
			color+='0'
		color+= (str(hex(int(which)))[2:])
	elif which <1021:
		color='#'
		which-=765
		if which<16:
			color+='0'
		color+= (str(hex(int(which)))[2:])
		color+='ff00'
	elif which < 1276:
		color='#ff'
		which-=1020
		which= 255-which
		if which<16:
			color+='0'
		color+= (str(hex(int(which)))[2:])
		color+='00'
	return color
	
def color(a, b):
	arnyalat=255-255*a/b
	col="#ff"
	if arnyalat<16:
		col+='0'
	col+=str(hex(int(arnyalat)))[2:]
	if arnyalat<16:
		col+='0'
	col+=str(hex(int(arnyalat)))[2:]
	return col
	
def color2(a, b):
	arnyalat=255*a/b
	col="#"
	if arnyalat<16:
		col+='0'
	col+=str(hex(int(arnyalat)))[2:]
	col+="0000"
	return col

def loading(x, y, start, extent, db=400, r=100):
	start=int(db*start/100)
	extent=int(db*extent/100)
	teljesszog=2*pi
	for i in range(start, extent):
		arany=i/(db/2)
		if i<db/2:
			x1=x + cos(arany*teljesszog)*r
			y1=y + sin(arany*teljesszog)*r
			x2=x + cos(arany*teljesszog)*r*(1-arany)
			y2=y + sin(arany*teljesszog)*r*(1-arany)
		else:
			x1, y1=x, y
			x2=x + cos(arany*teljesszog)*r*(2-arany)
			y2=y + sin(arany*teljesszog)*r*(2-arany)
		rajz.create_line(x1, y1, x2, y2, width=5, fill=color(i, db))
		ablak.update()
		#sleep(0.02)

loading(w/2, h/2, 0, 100)
	
mainloop()
