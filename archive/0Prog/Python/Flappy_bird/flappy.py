from tkinter import *
from random import *
from time import time
ablak=Tk()

rajz=Canvas(ablak, width=700, height=700, bg='white')
rajz.pack()

colnum=5

gapmin=100
gapmax=150

cols=[] 
for i in range(colnum):
	r=randint(gapmin, gapmax)
	c=randint(0, 700-r)
	cols.append([r, c])
	
r = 30
gap=700/colnum
start=700+r

colour= '#00ffff'

def createcols():
	global drawcols
	drawcols= [[rajz.create_rectangle(start+gap*i-r/2, 0, start+gap*i+r/2, cols[i][1], fill=colour), rajz.create_rectangle(start+gap*i-r/2, cols[i][1]+cols[i][0], start+gap*i+r/2, 700, fill=colour)] for i in range(colnum)]
createcols()

birdvel=0
t=time()
x, y = 300, 10
stpt = y
color = 'lightblue'
g=300
br=5
death=False

bird = rajz.create_oval(x-br, y-br, x+br, y+br, width=br, outline=color)

def swipe():
	global drawcols, start
	rajz.delete(drawcols[0][0])
	rajz.delete(drawcols[0][1])
	for i in range(4):
		drawcols[i]=drawcols[i+1]
	new0=randint(gapmin, gapmax)
	new1=randint(0, 700-new0)
	drawcols[4]= [rajz.create_rectangle(start-r/2, 0, start+r/2, new1, fill=colour), rajz.create_rectangle(start-r/2, new1+new0, start+r/2, 700, fill=colour)]

vel=Label()
#vel.pack()

def movebird():
	global birdvel, t, y
	curt=(time()-t)
	newy = stpt+birdvel*curt+g/2*pow(curt, 2)
	#vel['text']=str(int(newy-y/curt))
	rajz.move(bird, 0, newy-y)
	y=newy
	
def jump():
	global birdvel, t, stpt
	stpt=y
	t=time()
	birdvel=-250
	
jumpbutton=Button(text='JUMP', command=jump, width=300, height=7)
jumpbutton.pack()

def newg():
	global death, start, birdvel, stpt, x, y, t, bird, cols
	cols=[] 
	for i in range(colnum):
		r=randint(gapmin, gapmax)
		c=randint(0, 700-r)
		cols.append([r, c])
	x, y = 300, 10
	birdvel=0
	stpt=y
	t=time()
	rajz.delete(ALL)
	bird = rajz.create_oval(x-br, y-br, x+br, y+br, width=br, outline=color)
	start=700+r
	createcols()
	death=False

newgamebut=Button(text="New game", command=newg, width=100, height=5)
newgamebut.pack()

def check():
	global death
	for i in range(colnum):
		for j in range(2):
			c=rajz.coords(drawcols[i][j])
			if x+br>= c[0] and x-br<= c[2] and y+br>= c[1] and y-br<= c[3]:
				death=True
	if y-br<=0 or y+br>=700:
		death=True

while 1:
	if death:
		ablak.update()
		continue
	for i in range(30):
		check()
		movebird()
		ablak.update()
	for k in range(colnum):
		rajz.move(drawcols[k][0], -2,0)
		rajz.move(drawcols[k][1], -2,0)
	if rajz.coords(drawcols[0][0])[0] < 0:
		swipe()
mainloop()


	