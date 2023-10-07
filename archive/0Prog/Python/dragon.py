from math import pi, cos, sin
from colorsys import hsv_to_rgb


def dragon(level, maxdir=4):
	product=[0 for i in range(2**level)]
	for lvl in range(level):
		for i in range(2**lvl):
			j = 2**(lvl+1)-1 - i
			if product[i] >= maxdir-1:
				product[j] = 0
			else:
				product[j] = product[i] + 1
	return product


def calc_dir(x, y, dir, maxdir=4):
	return (
		x+cos(dir/maxdir*pi*2)*length,
		y+sin(dir/maxdir*pi*2)*length
	)


def tohex(pix):
	return '#'+('{:02X}'*3).format(*pix)

		
def coloring(ratio):
	return tohex(int(comp*255) for comp in hsv_to_rgb(ratio, 1, 1))


from tkinter import *
from time import sleep
ablak=Tk()
w, h=ablak.winfo_screenwidth(), ablak.winfo_screenheight()
rajz=Canvas(width=w, height=h, bg='black')
rajz.pack()

level=16
directions=dragon(level)
x, y = w*0.66, h*0.8
length=100/level/1.5

dlen = len(directions)
for i, dir in enumerate(directions):
	new_xy = calc_dir(x, y, (dir-1)%4)
	rajz.create_line(x, y, new_xy, fill=(coloring(i / dlen)), width=3)
	x, y = new_xy
	#ablak.update()
	#sleep(1/20)
	
mainloop()