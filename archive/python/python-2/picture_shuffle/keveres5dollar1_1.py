from PIL import Image
from tkinter import *
from imageio import imread
from numpy import array
from random import choice
from skimage.io import imsave

global addr 
form = Tk()
form.title('Shuffle Picture')
lenn = ''
addr = StringVar()
addr2 = StringVar()
addr3 = StringVar()

def Kever():
    f = open(str(addr3.get()), 'w')
    pic = imread(str(addr.get()))
    a = array(pic)
    lenn = a.shape
    newarr = [[[0 for b in range(0, 3)]for c in range(lenn[1])] for d in range(lenn[0])]
    list1 = [x for x in range(0, int(lenn[0])*int(lenn[1]))]
    
    for i in range(0, lenn[0]):
        for j in range(0, lenn[1]):
            choo = choice(list1)
            r1 = int(choo/float(lenn[1]))
            r2 = choo%lenn[1]
            newarr[r1][r2][0] = int(pic[i, j, 0])
            newarr[r1][r2][1] = int(pic[i, j, 1])
            newarr[r1][r2][2] = int(pic[i, j, 2])
            list1.remove(choo)
        print("cuc");
    
    imsave(str(addr2.get()), newarr)
    
lab1 = Label(form, text = 'Add meg az eleresi helyet: ').grid()
beadas = Entry(form, textvariable = addr).grid(row = 0, column = 1)
lab2 = Label(form, text = 'Add meg a krealando kep\neleresi helyet es nevet: ').grid(row = 1)
beadas2 = Entry(form, textvariable  = addr2).grid(row = 1, column = 1)
lab3 = Label(form, text = 'Add meg a kulcsfile eleresi\nhelyet, es nevet: ').grid(row = 2, column = 0)
beadas3 = Entry(form, textvariable = addr3).grid(row = 2, column = 1)
kevr = Button(form, text='SHUFFLE', command = Kever).grid(row = 3, column = 1)

form.mainloop()
