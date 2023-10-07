
from tkinter import *
import math
from random import randint
ablak=Tk()
w=700
h=700
rajz=Canvas(width=w, height=h, background='white')
rajz.pack()

x, y=350, 350
r=2
darab=100
mozdok=300
ugras=10
szoras=1
periodus=50

rajz.create_oval(350,0,360,10, width=5, outline='red')

pont=[[x, y] for i in range(darab)]
mozgas=[[[randint(-ugras, ugras), randint(-ugras, ugras)] for i in range(mozdok)] for i in range(darab)]

targy=[rajz.create_oval(x-r, y-r, x+r, y+r, width=r) for i in range(darab)]

ablak.update()

alive = [1 for i in range(darab)]
ment=[mozdok for i in range(darab)]

def rajzol():
	global pontok, targy, x, y
	for i in range(darab):
		pont[i][0]=x
		pont[i][1]=y
		alive[i]=1
		rajz.delete(targy[i])
		targy[i]=rajz.create_oval(x-r, y-r, x+r, y+r, width=r)
	for k in range(mozdok):
		for i in range(darab):
			if alive[i]:
				x=pont[i][0]+mozgas[i][k][0]
				y=pont[i][1]+mozgas[i][k][1]
				if x>0 and x<700 and y>0 and y<700:
					rajz.delete(targy[i])
					targy[i]=rajz.create_oval(x-r, y-r, x+r, y+r, width=r)
					pont[i][0] = x
					pont[i][1] = y
				else:
					alive[i] = 0
					ment[i]=k
		for i in range(10000):
			x+=1
			x-=1
		ablak.update()

def fittness():
	a=pont[0][0]-350
	b=pont[0][1]
	best=math.sqrt(a*a+b*b)
	bement=ment[0]
	bestind=0
	for i in range(darab):
		a=pont[i][0]-350
		b=pont[i][1]
		curr=math.sqrt(a*a+b*b)
		if (curr<best):
			best=curr
			bestind = i
	return bestind
		
def mutal():
	global mozgas
	ind = fittness()
	for i in range(darab):
		for k in range(mozdok):
			if randint(0, 100)<szoras:
				mozgas[i][k][0]=randint(-ugras, ugras)
				mozgas[i][k][1]=randint(-ugras, ugras)
			else:
				mozgas[i][k][0]=mozgas[ind][k][0]
				mozgas[i][k][1]=mozgas[ind][k][1]

def indit():
	global x, y
	for i in range(periodus):
		x, y=350, 350
		rajzol()
		mutal()
		
gomb=Button(text='Inditsd!', command=indit)
gomb.pack()

ablak.mainloop()
		


