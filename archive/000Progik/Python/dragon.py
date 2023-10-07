def dragon(lvl, product=None):
	if product is None:
		product=[0 for i in range(2**level)]
	for i in range(2**lvl-1, -1, -1):
		if product[i] == 3:
			product[2**(lvl+1)-i-1]=0
		else:
			product[2**(lvl+1)-i-1]=product[i]+1
	if lvl<level-1: dragon(lvl+1, product)
	return product

def calc_dir(x, y, dir):
	if dir==0:
		return x+length, y
	elif dir==1:
		return x, y+length
	elif dir==2:
		return x-length, y
	else:
		return x, y-length
		
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

		
from tkinter import *
from time import sleep
ablak=Tk()
w, h=700,700
rajz=Canvas(width=w, height=h, bg='white')
rajz.pack()

level=13
directions=dragon(0)
x, y=350, 350
length=100/level/2
ind=0
dlen=len(directions)
for d in directions:
	rajz.create_line(x, y, calc_dir(x, y, d), fill=coloring(ind, dlen))
	x, y = calc_dir(x, y, d)
	ablak.update()
	ind+=1
	
mainloop()