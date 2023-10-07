import PIL.Image as Img
import numpy as np
import tkinter as tk
import math

root = tk.Tk()
sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
draw = tk.Canvas(width=sw, height=sh, bg="white")
draw.pack()

#im = Img.open("dance.png")
#w, h = im.size
# pix = np.array(im)
#print(w, h)
#imTk = tk.PhotoImage(file="dance.png")

#def resizeImg(img, sz, nev):
#	a = img.zoom(sz, sz)
#	b = a.subsample(nev, nev)
#	return b
#	
#cucc = resizeImg(imTk,3,2)

#imm = draw.create_image(0,0, anchor=tk.NW, image=cucc)

#def blue(pix):
#	r, g, b = pix
#	return b>1.15*r or b>1.15*g
#	
#def orange(pix):
#	r, g, b = pix
#	return (b<=0.98*r and b<=0.98*g)
#	
#def tohex(pix):
#	return '#'+''.join(f'{comp:02X}' for comp in pix)

c=lambda x,y,r:(x-r,y-r,x+r,y+r)
#inv=lambda pix:[int((255-p)*0.6) for p in pix]
#dist=lambda p,q:math.hypot(p[0]-q[0], p[1]-q[1])

#pic={}

#for i in range(w):
#	for j in range(h):
#		pix = im.getpixel((i, j))
#		if orange(pix):
#			pix=inv(pix)
#		if i>w/2-j and j<h+(w*2/3-i) and (blue(pix) or orange(pix)):
#			pic[(i,j)] = draw.create_oval(c(i/w*sw, j/h*sh, 1), width=1, fill=tohex(pix), outline='')

storage={}
erase = False
drawingframe = True
framepos=None
frame=None
frames=[]
colored=[]
coloring=[]
bluecolor = "#1f78c9"
orangecolor = '#fa1a16'
#bluecolor = 'black'
#orangecolor = '#ff00ff'

oswitch = True

with open('pic.txt', 'r') as f:
	dance=eval(f.read())
	d = tuple(dance)
	for x,y in d:
		storage[(x,y)] = draw.create_oval(c(x, y, 1), width=1, outline='',fill=bluecolor)



def press(e):
	global framepos,frame
	framepos=(e.x,e.y)
	frame=draw.create_rectangle(framepos, framepos, width=3, outline=orangecolor, fill='')
	
def release(e):
	global framepos,frame,orangecolor,oswitch
	
	for (x, y), p in storage.items():
		if bw(framepos[0],x,e.x) and bw(framepos[1],y,e.y):
			draw.itemconfig(p, fill=orangecolor)
	framepos=None
	frames.append(frame)
	frame=None
	#orangecolor=('#00ff00' if oswitch else '#ff00ff')
#	oswitch = not oswitch

def bw(a, b, c): #between
	return a<b<c or a>b>c

def motion(e):
	r=4
	if drawingframe:
		if framepos:
			draw.coords(frame, framepos+(e.x, e.y))
	elif erase:
		for i in range(e.x-r, e.x+r):
			for j in range(e.y-r, e.y+r):
				pos=(i,j)
				if pos in storage:
					draw.delete(storage[pos])
					del storage[pos]
	elif (e.x,e.y) not in storage:
		storage[(e.x,e.y)] = draw.create_oval(c(e.x, e.y, 1), width=1, outline='',fill=bluecolor)
	
		
	#r = 8
	#x, y = int(e.x/sw*w), int(e.y/sh*h)
	#draw.itemconfigure(l, text=f"{(x,y,e.x,e.y, (x,y) in pic)}")
	#for i in range(x-r, x+r):
#		for j in range(y-r, y+r):
#			if (i,j) in pic:
#				draw.delete(pic[(i,j)])
#				del pic[(i,j)]
			
#def toggleerase():
#	global erase
#	erase = not erase
#	
#def save():
#	with open("pic.txt", "w") as f:
#		f.write(str(storage))
#		
#def toggleframe():
#	global drawingframe
#	drawingframe = not drawingframe
#	
def framedel(e):
	for f in frames:
		draw.delete(f)
	frames.clear()
	for p in storage.values():
		draw.itemconfig(p, fill=bluecolor)

#tk.Button(text="toggle erase", command=toggleerase).pack()
#tk.Button(text="save", command=save).pack()
#tk.Button(text="toggle frame",command=toggleframe).pack()
#tk.Button(text="delete frames",command=framedel).pack()

#l=draw.create_text(50,50,text="",fill='black', justify='left')

draw.bind('<Motion>', motion)
draw.bind('<1>', press)
draw.bind('<ButtonRelease-1>', release)
root.bind('<d>', framedel)

tk.mainloop()