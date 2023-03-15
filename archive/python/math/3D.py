# -*- coding: ISO-8859-2 -*-
from tkinter import *
from random import randint
from time import sleep
from keyboard import is_pressed
from functools import partial

'''#///////////////////////
ballSize = 50
decreasePerMeter = 8
meter = 100
dim = 2
ablwidth = 3*meter
ablheight = 3*meter
depth = 3*meter
stpt = [meter, meter, meter]
midp = [ablwidth/2, ablheight/2]
#///////////////////////

space = [[[0 for x in range(dim)] for x in range(dim)] for x in range(dim)]

ablak = Tk()
rajz = Canvas(ablak, bg = 'white', height = ablheight, width = ablwidth)
rajz.pack()

for i in range(dim):
    for j in range(dim):
        for k in range(dim):
            x = stpt[0]+k*meter
            y = stpt[1]+j*meter
            rajz.create_oval()'''
#///////////////////////////////////
pontok = 2
ablwidth = 1000
ablheight = 700
#///////////////////////////////////
    
def rajzol(x1, y1, x2, y2):
    #--------
    vastag = 1
    #--------
    color = '#42ebf4'
    rajz.create_line(x1,y1,x2,y2, width=vastag, fill=color)

ablak = Tk()
rajz = Canvas(ablak, bg = 'white', height = ablheight, width = ablwidth)
rajz.pack()

scale = Scale(ablak, from_ =0, to =10,tickinterval=1, orient=HORIZONTAL,
length=200)
scale.pack(side=LEFT)

#pont = [[randint(0, 500), randint(0, 400)] for x in range(pontok)]
pont = [[ablwidth/2,80], [80,ablheight/2], [ablwidth-80,ablheight/2]]

def start(x, y, stop):
    for i in range(pontok):
        a, b = (pont[i][0]+x)/2, (pont[i][1]+y)/2
        #rajz.create_oval(a, b, a+1, b+1, width=0, fill='#42ebf4', outline='#42ebf4')
        rajzol(pont[i][0], pont[i][1], x, y)
        #ablak.update()
        if stop < scale.get():
            start(a, b, stop+1)

#x, y = randint(0, 500), randint(400, 500)
x, y = ablwidth/2, ablheight-80
stpont = rajz.create_oval(x, y, x+4, y+4, width=2, fill='red', outline='red')

ovals = [0, 0, 0]
for i in range(pontok):
    ovals[i] = rajz.create_oval(pont[i][0],pont[i][1],pont[i][0]+4,pont[i][1]+4, width=2, fill='black')

while (1):
    ablak.update()
    if is_pressed('q') and pont[0][1] > 0:
        pont[0][1] -= 1
    if is_pressed('a') and pont[0][1] < ablheight:
        pont[0][1] += 1
    if is_pressed('w') and pont[0][0] > 0:
        pont[0][0] -= 1
    if is_pressed('e') and pont[0][0] < ablwidth:
        pont[0][0] += 1
    if is_pressed('s') and pont[1][1] > 0:
        pont[1][1] -= 1
    if is_pressed('x') and pont[1][1] < ablheight:
        pont[1][1] += 1
    if is_pressed('d') and pont[1][0] > 0:
        pont[1][0] -= 1
    if is_pressed('f') and pont[1][0] < ablwidth:
        pont[1][0] += 1
    if is_pressed('h'):
        y -= 1
    if is_pressed('n'):
        y += 1
    if is_pressed('j'):
        x -= 1
    if is_pressed('k'):
        x += 1
        
    if is_pressed('r'):
        start(x, y, 0)
    if is_pressed('space'):
        rajz.delete("all")

    if is_pressed('enter'):
        ablak.destroy()
        break
    
    for i in range(pontok):
        rajz.delete(ovals[i])
        ovals[i] = rajz.create_oval(pont[i][0],pont[i][1],pont[i][0]+4,pont[i][1]+4, width=2, fill='black')

    rajz.delete(stpont)
    stpont = rajz.create_oval(x, y, x+4, y+4, width=2, fill='red', outline='red')


