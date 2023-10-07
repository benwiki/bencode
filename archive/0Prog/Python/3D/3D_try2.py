from tkinter import *
import math
ablak = Tk()

rajz = Canvas(ablak, background='white', width= 700, height=700)
rajz.pack()

z=1
x=-(z*12)
speed=10

def ind():
	global x, z
	rajz.create_oval(350, 400, 358, 408,width= 4,fill='red')
	ablak.update()
	for i in range(500000):
		x+=1
		x-=1
	while(1):
		rajz.delete("all")
		a=math.atan(x/z)*222+350
		rajz.create_oval(a-4, 396, a+4,404,width= 4,fill='red')
		ablak.update()
		for i in range(int(50000/speed)):
			x+=1
			x-=1
		x+=1
		
'''button = Button(text='indit', command=ind)
button.pack(side=LEFT)'''
ind()

#ablak.mainloop()
	
	
	
	
	