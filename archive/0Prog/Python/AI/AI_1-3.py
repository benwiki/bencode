#GLICH: ottmaradnak a pontok a pályán

from tkinter import *
import math
from random import randint
ablak=Tk()
w=700
h=700
rajz=Canvas(width=w, height=h, background='white')
rajz.pack()

x, y=350, 699
r=2
darab=130
mozdok=100
ugras=10
szoras=1
periodus=150

rajz.create_oval(350,0,360,10, width=5, outline='red')

pont=[[x, y] for i in range(darab)]
mozgas=[[[randint(-ugras, ugras), randint(-ugras, ugras)] for i in range(mozdok)] for i in range(darab)]

targy=[rajz.create_oval(x-r, y-r, x+r, y+r, width=r) for i in range(darab)]

ablak.update()

alive = [1 for i in range(darab)]
ment=[mozdok for i in range(darab)]
celelerve=0
bement=ment[0]

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
				if (x>0 and x<700 and y>0 and y<700) and not (celelerve and k <= bement):
					rajz.delete(targy[i])
					targy[i]=rajz.create_oval(x-r, y-r, x+r, y+r, width=r)
					pont[i][0] = x
					pont[i][1] = y
				else:
					alive[i] = 0
					ment[i]=k
		ablak.update()

def fittness():
	global szoras, bement
	kivalaszt=int(darab/30)
	a=pont[0][0]-350
	b=pont[0][1]
	best=math.sqrt(a*a+b*b)
	bestind=0
	for i in range(darab):
		a=pont[i][0]-350
		b=pont[i][1]
		curr=math.sqrt(a*a+b*b)
		if (curr<best):
			best=curr
			bestind = i
	bement=ment[bestind]
	a=pont[bestind][1]
	b=pont[bestind][0]-350
	curr=math.sqrt(a*a+b*b)
	if curr<10:
		celelerve=1
		rajz.create_oval(0,0,10,10, width=5, outline='#00FF00')
	return bestind
		
def mutal(szor):
	global mozgas
	ind = fittness()
	for i in range(darab):
		for k in range(mozdok):
			if randint(0, 100)<szor:
				mozgas[i][k][0]=randint(-ugras, ugras)
				mozgas[i][k][1]=randint(-ugras, ugras)
			else:
				mozgas[i][k][0]=mozgas[ind][k][0]
				mozgas[i][k][1]=mozgas[ind][k][1]

#scale =Scale(from_=0, to=20, orient=HORIZONTAL, width=70, length=700, sliderlength=80)
#scale.pack()

def indit():
	global x, y
	for i in range(periodus):
		x, y=350, 699
		rajzol()
		mutal(szoras)
		
gomb=Button(text='Indítsd!', command=indit)
gomb.pack()

ablak.mainloop()
		


