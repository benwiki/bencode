from tkinter import *

ablak=Tk()
w, h = 700, 700
rajz=Canvas(width=w, height=h, bg='white')
rajz.pack()

lab=Label()
lab.pack()

#s1=Scale(side=HORIZONTAL)
#s1.pack()

nx=60
ny=-5
ny=-20
meddig = 200

def coord(x, y, r):
	return [x-r, y-r, x+r, y+r]
	
def draw(f):
	x=-w/meddig+0.0001
	u=1
	first=1
	while x<w/meddig:
		y=eval(f)*ny
		ex=x*nx
		if first:
			elx=ex
			ely=y
		rajz.create_line(ex+w/2, y+h/2, elx+w/2, ely+h/2)
		x+=0.1
		elx=ex
		ely=y
		first=0
		
f="(x**10)-5*(x**6)"
#f="-x**12+2*x**10+10*x**6-25*x**2"
#f="x"
draw(f)
i=0
#mainloop()
while 1:
	while i<3:
		rajz.delete(ALL)
		draw(f+"+"+str(i)+"*x")
		ablak.update()
		i+=0.1
	while i>-3:
		rajz.delete(ALL)
		draw(f+"+"+str(i)+"*x")
		ablak.update()
		i-=0.1
mainloop()
		