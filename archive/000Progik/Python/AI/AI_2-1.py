from tkinter import *
from random import uniform, randint
from math import *
ablak=Tk()
rajz=Canvas(width=700, height=700, bg='white')
rajz.pack()

db=50
r=150
x, y=0, 350-r/2
randdir=50
hatar=10

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

input=[[350, 350] for i in range(db)]
layer=[[0,0,0] for i in range(db)]
output=[0 for i in range(db)]

mech=[rajz.create_line(x+5, y, x+5, y+r, width=5, fill=coloring(i+1, db)) for i in range(db)]
alive=[1 for i in range(db)]
w1=[[[uniform(-1, 1) for i in range(3)]for k in range(2)] for j in range(db)]
w2=[[uniform(-1, 1) for i in range(3)] for j in range(db)]

br=5
x,y=350, 350
ball=[rajz.create_oval(x-br, y-br, x+br, y+br, width=br, outline=coloring(i+1, db)) for i in range(db)]
dir=[uniform(0, 360) for i in range(db)]

def fsgn(x):
	if x <=0:
		return 0
	else:
		return 1

def AllDead():
	what = True
	for i in range(db):
		if alive[i]:
			what=False
			break
	return what

def mozog():
	global dir
	i=0
	while not AllDead():
		i+=1
		if i%10==0:
			ablak.update()
		for j in range(db):
			if alive[j]:
				inp1=rajz.coords(ball[j])[0]
				inp2=rajz.coords(mech[j])[1]
				for k in range(3):
					sum=0
					sum+=w1[j][0][k]*inp1
					sum+=w1[j][1][k]*inp2
					layer[j][k]=fsgn(sum)
				sum=0
				for k in range(3):
					sum+=w2[j][k]*layer[j][k]
				output[j]=sum
				rel=rajz.coords(mech[j])[1]+sum
				#----------
				cx=inp1
				cy=rajz.coords(ball[j])[1]
				my=inp2
				if cx>700-br:
					dir[j] += 2*(270-dir[j])
					if randint(0, 100)<randdir:
						dir[j]+=uniform(-hatar, hatar)
				elif cy<br or cy>700-br:
					dir[j] += 2*(360-dir[j])
					if randint(0, 100)<randdir:
						dir[j]+=uniform(-hatar, hatar)
				elif cx<br+10 and my<=cy and my+r >= cy:
					dir[j] += 2*(270-dir[j])
					if randint(0, 100)<randdir:
						dir[j]+=uniform(-hatar, hatar)
				elif cx<br:
					alive[j]=0
				x = cos(radians(dir[j]))*2
				y = -sin(radians(dir[j]))*2
				#----------
				if not rel<0 and not rel>700-r:
					rajz.move(mech[j], 0, output[j])
				rajz.move(ball[j], x, y)
					
def paintweights(which, x, y, size):
	r=5
	hoy = y
	rajz.create_oval(x-r, y-r, x+r, y+r, width=r)
	y+=size
	rajz.create_oval(x-r, y-r, x+r, y+r, width=r)
	y=hoy
	for i in range(2):
		y+=i*size
		for j in range(3):
			z, w=x+size, (hoy-size/2+j*size)
			rajz.create_oval(z-r, w-r, z+r, w+r, width=r)
			if w1[which][i][j] < 0:
				color="blue"
			else:
				color="red"
			rajz.create_line(x, y, z, w, width = abs(size/20*w1[which][i][j]), fill=color)
			
	z, w=x+2*size, hoy+size/2
	rajz.create_oval(z-r, w-r, z+r, w+r, width=r)
	x+=size
	for i in range(3):
		y=hoy-size/2+i*size
		if w2[which][i] < 0:
			color="blue"
		else:
			color="red"
		rajz.create_line(x, y, z, w, width = abs(size/20*w2[which][i]), fill=color)

#paintweights(0, 100, 100, 70)
mozog()

ablak.mainloop()