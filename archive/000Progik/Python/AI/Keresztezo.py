from math import *
from random import randint
from tkinter import *
ablak=Tk()
rajz=Canvas(width=700, height=700, bg='white')
rajz.pack();

label=Label()
label.pack()

fal=[[19, 86],[310, 518 ]]
vonal=[[175, 0],[135,600]]
rajz.create_line(fal[0][0],700-fal[0][1],fal[1][0], 700-fal[1][1], fill='red', width=3)
rajz.create_line(vonal[0][0],700-vonal[0][1],vonal[1][0], 700-vonal[1][1], width=3)

szeles=abs(fal[0][0]-fal[1][0])
magas=abs(fal[1][1]-fal[0][1])
z=magas/szeles
label.configure(text=str(z))
x1=175
y1=700-(vonal[0][0]*z)
r=4
rajz.create_oval(x1-r, y1-r, x1+r, y1+r, outline='red')

ablak.mainloop()






