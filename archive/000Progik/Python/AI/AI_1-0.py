from tkinter import *
from random import randint
ablak=Tk()
rajz=Canvas(width=700, height=700, background='white')
rajz.pack()

moves=200
r=2
pos=[350,700]
thedot=rajz.create_oval(pos[0]-r, pos[1]-r, pos[0]+r, pos[1]+r, width=r)

class Dot:
	def __init__(self):
		self.taken=0
		self.move= [[randint(-5, 5), randint(-5, 5)] for i in range(moves)]
		#self.thedot=rajz.create_oval(pos[0]-r, pos[1]-r, pos[0]+r, pos[1]+r, width=r)
	
	def move():
		if pos[0]>0 and pos[0]<700 and pos[1] > 0 and pos[1] < 700:
			rajz.delete(thedot)
			x=pos[0]+move[taken][0]
			y=pos[1]+move[taken][1]
			thedot=rajz.create_oval(x-r, y-r, x+r, y+r, width=r)
			pos[0]=x
			pos[1]=y
			taken += 1

ablak.update()
dots=Dot()
a=1
for i in range(moves):
	for k in range(1):
		dots.move()
	for k in range(10):
		a+=1
		a-=1
	ablak.update()