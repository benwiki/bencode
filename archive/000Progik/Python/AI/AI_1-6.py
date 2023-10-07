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
darab=140
mozdok=1000
ugras=10
fordulas=0.33
fordindex=100
szoras=7
periodus=1000
celbaert=[0 for i in range(darab)]

bind=0

rajz.create_oval(350,0,360,10, width=5, outline='red')
rajz.create_line(300, 410, 700, 410, width=20, fill='#8888FF')
rajz.create_line(0,290,400,290, width=20, fill='#8888FF')
rajz.create_line(0, 510, 400, 510, width=20, fill='#8888FF')
rajz.create_line(300,190,700,190, width=20, fill='#8888FF')

pont=[[x, y] for i in range(darab)]
mozgas=[[[0, 0] for i in range(mozdok)] for i in range(darab)]

for i in range(darab):
	mozgas[i][0][0]=randint(0, ugras)
	mozgas[i][0][1]=uniform(0, 360)
	for k in range(1, mozdok):
		mozgas[i][k][0]=randint(0, ugras)
		mozgas[i][k][1]=mozgas[i][k-1][1]
		if randint(0, 100)<fordindex:
			mozgas[i][k][1]+=uniform(-fordulas, fordulas)

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
	global pontok, targy, x, y, bind
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
				if x>0 and x<700 and y>0 and y<700 and not (y>280 and y<300 and x<400) and not (y>400 and y<420 and x>300) and not (y>180 and y<200 and x>300) and not (y>500 and y<520 and x<400) and k<= bement:
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
	global mozgas, k, bind
	bind=fittness()
	for i in range(darab):
		for k in range(0, ment[bind]-17):
			mozgas[i][k][0]=mozgas[bind][k][0]
			mozgas[i][k][1]=mozgas[bind][k][1]
		ind = kivalaszt()
		for k in range(ment[bind]-16, mozdok):
			if randint(0, 100)<szoras:
				mozgas[i][k][0]=randint(0, ugras)
				mozgas[i][k][1]=mozgas[i][k-1][1]+ uniform(-fordulas, fordulas)
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
		


