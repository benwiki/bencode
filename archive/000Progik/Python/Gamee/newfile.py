from tkinter import *
from math import *
from random import uniform
from time import time
ablak=Tk()

rajz=Canvas(width=700, height=700, bg='white')
rajz.pack()
x, y=350, 350
alseg=[]

def help(i):
	global min, max, alseg
	min=20
	max=40
	r=radians(uniform(0, 90)+i*90)
	d=uniform(min, max)
	alseg.append([r, d])
	a, b = cos(r)*d+x, sin(r)*d+y
	return [a, b]

alak=[help(0), help(1), help(2), help(3)]
enemy=rajz.create_polygon(alak, fill='white', outline='black')

#rajz.create_oval(x-min, y-min, x+min, y+min, outline='red')

hatar1=5
hatar2=5

def mozgat():
	global alak
	for i in range(4):
		r=degrees(alseg[i][0]) +uniform(-hatar1, hatar1)
		d=alseg[i][1]+uniform(-hatar2, hatar2)
		if r>90+i*90:
			r=90+i*90
		elif r<i*90:
			r=i*90
		if d < min:
			d=min
		elif d > max:
			d=max
		r=radians(r)
		a, b = cos(r)*d+x, sin(r)*d+y
		alak[i][0]=a
		alak[i][1]=b
		

while 1:
	rajz.delete(enemy)
	mozgat()
	#alak=[help(0), help(1), help(2), help(3)]
	enemy=rajz.create_polygon(alak, fill='white', outline='black')
	#rajz.create_oval(x-min, y-min, x+min, y+min, outline='red')
	for i in range(1000):
		i+=1
		i-=1
	ablak.update()
	
mainloop()




