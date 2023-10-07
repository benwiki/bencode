from tkinter import *
from math import *
ablak=Tk()
rajz=Canvas(width=700, height=700, bg='white')
rajz.pack()

x, y=350, 350
r=1
bigr=30
db=360

pont=[rajz.create_oval(x+cos(i)*bigr-r, y+sin(i)*bigr-r, x+cos(i)*bigr+r, y+sin(i)*bigr+r, width=r) for i in range(db)]

def mozg():
	for i in range(db):
		pont[i].configure(x, y, 360, 360)
		
button=Button(text='mozg', command=mozg)
button.pack()

ablak.mainloop()



