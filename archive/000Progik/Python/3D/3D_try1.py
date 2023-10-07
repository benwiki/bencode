from tkinter import *
ablak = Tk()

rajz=Canvas(background='white', width=700, height=700)
rajz.pack()
pont = [[100,80],[600,80]]
'''for i in range(2):
	rajz.create_oval(pont[i][0]-4, pont[i][1]-4,pont[i][0]+4,pont[i][1]+4,width=4,fill='#42efb6')'''
pontok=2

x,y=350, 520
#rajz.create_oval(x-4,y-4,x+4,y+4,width=4,fill='#42efb6')

add=0

def start():
	global add
	rajz.delete("all")
	for i in range(2):
		x,y=350, 520+add
		rajz.create_line(x, y, pont[i][0]+add*(-1+i*2), pont[i][1],fill='#42efb6', width=1)
		for k in range(10):
			x, y = (pont[i][0]+add*(-1+i*2)+x)/2, (pont[i][1]+y)/2
			if i==0:
				c=1
			else:
				c=0
			rajz.create_line(x, y, pont[c][0]-add*(-1+i*2), pont[c][1],fill='#42efb6', width=1)
	add+=40
		


gomb= Button(text='Rajzold', command=start)
gomb.pack()

ablak.mainloop()