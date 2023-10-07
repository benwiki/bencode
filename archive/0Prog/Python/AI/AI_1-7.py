from tkinter import *
import math
from random import randint, uniform
from time import sleep
ablak=Tk()
w=700
h=700
rajz=Canvas(width=w, height=h, background='white')
rajz.pack()

x, y=350, 699
r=3
darab=100
mozdok=1000
ugras=10
fordulas=0.33
fordindex=100
periodus=100
celbaert=[0 for i in range(darab)]

final=0

rajz.create_oval(350,0,360,10, width=5, outline='red')
rajz.create_line(300, 410, 700, 410, width=20, fill='#00FFFF')
rajz.create_line(0,290,400,290, width=20, fill='#00FFFF')
rajz.create_line(0, 510, 400, 510, width=20, fill='#00FFFF')
rajz.create_line(300,190,700,190, width=20, fill='#00FFFF')

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

label = Label(text='nothing')
label.pack()

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
					targy[i]=rajz.create_oval(x-r, y-r, x+r, y+r, width=r)
					pont[i][0] = x
					pont[i][1] = y
				else:
					alive[i] = 0
		ablak.update()

def fittness():
	global bement, final
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
	a=pont[bestind][0]-350
	b=pont[bestind][1]
	curr=math.sqrt(a*a+b*b)
	label.configure(text=str(curr))
	if curr<15:
		final+=1
		label.configure(text='DONE')
	ablak.update()
	return bestind

def mutal():
	global mozgas, k, bind, final
	bind=fittness()
	for i in range(darab):
		if not final==1:
			for k in range(0, ment[bind]-17):
				mozgas[i][k][0]= mozgas[bind][k][0]
				mozgas[i][k][1]= mozgas[bind][k][1]
			for k in range(ment[bind]-16, mozdok):
				mozgas[i][k][0]=randint(0, ugras)
				mozgas[i][k][1]=mozgas[i][k-1][1]+ uniform(-fordulas, fordulas)
		else:
			for k in range(0, mozdok):
				mozgas[i][k][0]= mozgas[bind][k][0]
				mozgas[i][k][1]= mozgas[bind][k][1]
		

def indit():
	global x, y, final
	final=0
	while not final==2:
		rajzol()
		mutal()
		x, y=350, 699

gomb=Button(text='Inditsd!', command=indit)
gomb.pack()

ablak.mainloop()
		


