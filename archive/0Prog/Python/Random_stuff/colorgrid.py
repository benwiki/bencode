from tkinter import *
win = Tk()
d = 1000
w, h = (d,)*2
draw = Canvas(bg='black', width=w, height=h)
draw.pack()

rectcoords = lambda i, j, h, w: (j*w/4,i*h/4,(j+1)*w/4, (i+1)*w/4)

draw.create_rectangle(w*1/12, h*1/12, w*11/12, h*3/6-5, fill='#ff0000')
draw.create_rectangle(w*1/24, h*1/6+5, w*23/24, h*2/6-5, fill='#00ff00')
draw.create_rectangle(w*1/24, h*3/6+5, w*23/24, h*4/6-5, fill='#00ff00')
draw.create_rectangle(w*5/10, h*3/24, w*21/24, h*21/24, fill='#0000ff')

for i in range(4):
	for j in range(4):
		draw.create_rectangle(rectcoords(i+1,j+1,h*2/3,w*2/3), fill="#"+("ff" if i<2 else "99" if not 0<j<3 else "00") + ("ff" if i==0 or i==2 else "99" if not 0<j<3 else "00") + ("ff" if j>1 else "99" if not 0<j<3 else "00"), outline="white", width=5)
		

mainloop()