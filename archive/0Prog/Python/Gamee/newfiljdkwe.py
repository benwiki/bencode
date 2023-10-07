from tkinter import *
from random import *
from time import time
ablak=Tk()

rajz=Canvas(ablak, width=700, height=700, bg='white')
rajz.pack()

szov=rajz.create_text(100, 100, text='cucc', font=("Courier", 10))
Label(text=str(rajz.itemcget(szov, "font").split()[1])).pack()

mainloop()