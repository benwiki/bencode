#It fucks up!!!!! wtf!! look at the coded example

from tkinter import *
import math
from random import randint, uniform
from time import sleep
ablak=Tk()
w=700
h=700
rajz=Canvas(width=w, height=h, background='white')
rajz.pack()

x, y=350, 670
r=2
darab=150
mozdok=1000
ugras=10
fordulas=1
fordindex=10
szoras=6
periodus=50
celbaert=[0 for i in range(darab)]

rajz.create_oval(350,0,360,10, width=5, outline='red')

pont=[[x, y] for i in range(darab)]
mozgas=[[[0, 0] for i in range(mozdok)] for i in range(darab)]

for i in range(darab):
	mozgas[i][0][0]=randint(0, ugras)
	mozgas[i][0][1]=randint(0,360)
	for k in range(1, mozdok):
		mozgas[i][k][0]=randint(0, ugras)
		mozgas[i][k][1]=mozgas[i][k-1][1]
		if randint(0, 100)<fordindex:
			mozgas[i][k][1]+=randint(-fordulas, fordulas)

targy=[rajz.create_oval(x-r, y-r, x+r, y+r, width=r) for i in range(darab)]

ablak.update()

alive = [1 for i in range(darab)]
ment=[mozdok for i in range(darab)]
bement=mozdok

fittnessek=[0 for i in range(darab)]
sumfittness=0

label = Label(text='nothing')
label.pack()
label2 = Label(text='nothing')
label2.pack()

def rajzol():
	global pontok, targy, x, y
	for i in range(darab):
		pont[i][0]=x
		pont[i][1]=y
		alive[i]=1
		rajz.delete(targy[i])
		targy[i]=rajz.create_oval(x-r, y-r, x+r, y+r, width=r)
		ment[i]=0
	for k in range(mozdok):
		for i in range(darab):
			if alive[i]:
				ment[i]=k
				x=pont[i][0]+round(math.sin( mozgas[i][k][1])*mozgas[i][k][0])
				y=pont[i][1]+round(math.cos( mozgas[i][k][1])*mozgas[i][k][0])
				if x>0 and x<700 and y>0 and y<700 and k<= bement:
					rajz.delete(targy[i])
					if not i==0:
						color='black'
					else:
						color='#00FF00'
					targy[i]=rajz.create_oval(x-r, y-r, x+r, y+r, width=r, outline=color)
					pont[i][0] = x
					pont[i][1] = y
				else:
					alive[i] = 0
		ablak.update()

v=0
def fittness():
	global fittnessek, sumfittness, v, bement
	v=0
	sumfittness=0
	for i in range(darab):
		a=pont[i][0]-350
		b=pont[i][1]
		curr=math.sqrt(a*a+b*b)
		if curr<30:
			fittnessek[i]=10000/ (ment[i]*ment[i])
		else:
			fittnessek[i]=1/(curr*curr)
		sumfittness+=fittnessek[i]
	label2.configure(text=str(sumfittness))
		
	best=fittnessek[0]
	ind=0
	for i in range(1, darab):
		if fittnessek[i]>best:
			best=fittnessek[i]
			ind=i
	a=pont[ind][0]-350
	b=pont[ind][1]
	curr=math.sqrt(a*a+b*b)
	label.configure(text=str(curr))
	if curr<30:
		bement=ment[ind]
	label3.configure(text=str(bement))
	ablak.update()
	return ind
		
label3=Label(text='cucc')
label3.pack()
def kivalaszt():
	global v
	kival=uniform(0, sumfittness)
	runningsum=0
	ind=0
	for i in range(darab):
		runningsum+=fittnessek[i]
		if runningsum>kival:
			return i
	return 0
		
def mutal():
	global mozgas, k
	ind=fittness()
	for k in range(mozdok):
		mozgas[0][k][0]=mozgas[ind][k][0]
		mozgas[0][k][1]=mozgas[ind][k][1]

	for i in range(1, darab):
		ind = kivalaszt()
		if randint(0, 100)<szoras:
			mozgas[i][0][0]=randint(0, ugras)
			mozgas[i][0][1]=mozgas[i][1][1]+ randint(-fordulas, fordulas)
		else:
			mozgas[i][0][0]=mozgas[ind][0][0]
			mozgas[i][0][1]=mozgas[ind][0][1]
		for k in range(1, mozdok):
			if randint(0, 100)<szoras:
				mozgas[i][k][0]=randint(0, ugras)
				mozgas[i][k][1]=mozgas[i][k-1][1]+ randint(-fordulas, fordulas)
			else:
				mozgas[i][k][0]=mozgas[ind][k][0]
				mozgas[i][k][1]=mozgas[ind][k][1]

def indit():
	global x, y
	for i in range(periodus):
		rajzol()
		mutal()
		x, y=350, 670

gomb=Button(text='Inditsd!', command=indit)
gomb.pack()

ablak.mainloop()
		


