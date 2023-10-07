from tkinter import *
from random import uniform
ablak=Tk()
rajz=Canvas(width=700, height=700, bg='white')
rajz.pack()

db=50
x, y=0, 350
r=2

rajz.create_line(0, 200, 700, 200)
rajz.create_line(0, 500, 700, 500)

pont=[rajz.create_oval(x-r, y-r, x+r, y+r, width=r) for i in range(db)]

alive=[1 for i in range(db)]

input=[0, 0]
layer1=[0, 0, 0, 0, 0, 0, 0, 0]
output=[0, 0, 0, 0]
conn1=[[[uniform(-1, 1) for i in range(8)]for k in range(2) for j in range(db)]
conn2=[[[uniform(-1, 1) for i in range(8)]for k in range(4)] for j in range(db)]

def fsgn(x):
	if <=0:
		return 0
	else:
		return 1

def AllAlive():
	what = True
	for i in range(db):
		if not alive[i]:
			what=False
			break
	return what
	
def mozog():
	for i in range(db):
		if alive[i]:
			for j in range()

while 1:
	while AllAlive:
		