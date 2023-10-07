from tkinter import *
from random import uniform, randint
from math import *
ablak=Tk()
rajz=Canvas(width=700, height=700, bg='white')
rajz.pack()

r=5
x,y=350,350
kor=rajz.create_oval(x-r, y-r, x+r, y+r, width=r)
irany=randint(1, 360)

def comm():
	global x, y, irany
	x, y=350,350
	#irany=radians(randint(1, 360))
	irany=170

button=Button(text="valtsd", command=comm).pack()
label=Label(text=str(irany))
label.pack()

while (1):
	rajz.delete(kor)
	x+=cos(radians(irany))
	y-=sin(radians(irany))
	kor=rajz.create_oval(x-r, y-r, x+r, y+r, width=r)
	for i in range(2000):
		x+=1
		x-=1
	if x<r or x>700-r:
		irany += 2*(270-irany)
	elif y<r or y>700-r:
		irany += 2*(360-irany)
	label.configure(text=str(irany))
	ablak.update()