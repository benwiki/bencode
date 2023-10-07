from tkinter import *
import math
ablak = Tk()

rajz = Canvas(ablak, background='white', width= 700, height=700)
rajz.pack()

x=-300
z=20

def ind():
	global x, z
	rajz.create_line(350, 400, 350, 700,width= 4,fill='red')
	ablak.update()
	for i in range(500000):
		x+=1
		x-=1
	while(x<1000):
		#a=math.atan(x/z)*200+350
		cucc=rajz.create_line(x, 400, 350,700,width= 4,fill='black')
		ablak.update()
		for i in range(4000):
			x+=1
			x-=1
		x+=1
		rajz.delete(cucc)
		
'''button = Button(text='indit', command=ind)
button.pack(side=LEFT)'''
ind()

#ablak.mainloop()
	
	
	
	
	