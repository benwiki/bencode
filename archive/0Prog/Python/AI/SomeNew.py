from tkinter import *
from math import *
ablak=Tk()
rajz=Canvas(width=700, height=700, bg='white')
rajz.pack()

x, y=350, 350
r=1
bigr=30
db=360

oval_coords = lambda x, y, r: (x-r, y-r, x+r, y+r)

pont=[rajz.create_oval(oval_coords(x+cos(i)*bigr, y+sin(i)*bigr, r), width=r) for i in range(db)]

def mozg():
	for i in range(db):
		rajz.coords(pont[i], (x, y, 360, 360))
		
button=Button(text='mozg', command=mozg)
button.pack()

ablak.mainloop()



