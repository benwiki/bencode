from tkinter import *
from random import uniform
from time import sleep
ablak=Tk()
rajz=Canvas(width=700, height=700, bg='white')
rajz.pack()

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

q=35
for i in range(20):
	for j in range(20):
		n,m=i,j+1
		color=coloring(n*20+m, 400)
		for k in range(1000):
			k+=1
			k-=1
		rajz.create_rectangle(q*i,q*j, q*i+q, q*j+q, fill=color, outline=color)
		ablak.update()
		sleep(0.03)
		
		
ablak.mainloop()