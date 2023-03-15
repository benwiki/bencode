# -*- coding: ISO-8859-2 -*-
from Tkinter import *
win = Tk()
var1 = IntVar()
var2 = IntVar()
scale1 = Scale(win, from_ =100, to =-100,tickinterval=50, orient=VERTICAL,
length=300)
scale2 = Scale(win, from_ =-100, to =100,tickinterval=50, orient=HORIZONTAL,
length=300)

scale1.grid()
scale2.grid(row=0,column=1, sticky=N)

win.mainloop()
