
from math import cos, sin, pi
"""window=Tk()
#window.config(bg="black")
w, h = window.winfo_screenwidth(), window.winfo_screenheight()

draw=Canvas(width=w, height=h, bg='white', highlightthickness=0)
draw.pack()

line = draw.create_line(0,0,0,0, fill='red', width=5)"""
	
def coord(arg1=None, arg2=None, r=0):
	if isinstance(arg1, tuple) or isinstance(arg1, list):
		x1, y1, x2, y2 = arg1
		r=abs(x1-x2)/2
		return x1+r, y1+r, r
	else:
		x, y = arg1, arg2
		return x-r, y-r, x+r, y+r
	
def wait(x):
	from time import time
	t=time()
	while time()-t<x:
		window.update()
from PIL import Image, ImageDraw

szorzo=10

w, h=1000*szorzo, 1000*szorzo
kep=Image.new("1", (w, h), 1)
draw1=ImageDraw.Draw(kep)

bw, bh= 10*szorzo, 10*szorzo
db=10
wid=25*szorzo
x, y, r= bw, h-bh, w-bw
angle=-360/(2**(db-2))/2.6
#angle=0
draw1.arc(coord(x, y, h-bh), -90, 0, 0, wid)
for i in range(db-1, -1, -1):
	print(i)
	r-=wid-2
	for k in range(2**i//4):
		#draw.create_arc(coord(x, y, r), start=360/(2**i)*k-angle+90, extent=180/(2**i), width=wid, style='arc')
		e=360/(2**i)*(k)-90-angle
		s=e-180/(2**i)
		draw1.arc(coord(x, y, r), s, e, 0, wid)
		#wait(1)
	angle-=540/(2**(i+1))
	
"""for i in range(2**db):
	angle=2*pi/(2**db)*(i+0.5)
	kx, ky = w/2+cos(angle)*(r), h/2+sin(angle)*(r)
	draw.coords(line, w/2, h/2, kx, ky)
	digits=[int(str(bin(i))[2:][k]) for k in range(len(str(bin(i))[2:]))]
	for k in range(len)
	
	wait(1)"""

draw1.arc(coord(x, y, r+wid), 270, 315, 0, wid)
draw1.line((0, 0, 0, h), fill=0, width=bw*2)
draw1.line((0, 0, w, 0), fill=0, width=bw*2)
draw1.line((w, h, 0, h), fill=0, width=bw*2)
draw1.line((w, h, w, 0), fill=0, width=bw*2)
kep.save("ujkep.png")
#mainloop()