# -*- coding: cp1250 -*-
from tkinter import *

from random import randint 

from time import sleep, time

from math import sqrt

from keyboard import is_pressed

height = 500
width = 800
ablak = Tk()

ablak.title("Buborék Pukkaszto.")
v = Canvas(ablak, width = width, height = height, bg = 'darkblue')
v.pack()



hajo1 = v.create_polygon(7, 2, 7, 28, 30, 15, fill = 'red')
hajo2 = v.create_oval(0, 0, 30, 30, outline = 'red')
hajo_r = 15
kp_x = width / 2
kp_y = height / 2
v.move(hajo1, kp_x, kp_y)
v.move(hajo2, kp_x, kp_y)

hseb = 10
def hajomozgatas():
    x, y = v.coords(hajo2)[:2]
    if is_pressed('up_arrow') and y-hseb>0:
        v.move(hajo1, 0, -hseb)
        v.move(hajo2, 0, -hseb)
    elif is_pressed('down_arrow') and y+30+hseb<height:
        v.move(hajo1, 0, hseb)
        v.move(hajo2, 0, hseb)
    if is_pressed('left_arrow') and x-hseb>0:
        v.move(hajo1, -hseb, 0)
        v.move(hajo2, -hseb, 0)
    elif is_pressed('right_arrow') and x+30+hseb<width:
        v.move(hajo1, hseb, 0)
        v.move(hajo2, hseb, 0)
#v.bind_all('<Key>', hajomozgatas)

bubid = list() 
bubr = list()
bubse = list()
minbubr = 10
maxbubr = 30
maxbubse = 10
diff = 100

def buborekgyartas():
    x = width + diff
    y = randint(0, height)
    r = randint(minbubr, maxbubr)

    id1 = v.create_oval(x - r, y - r, x + r, y + r, outline = 'white')
    bubid.append(id1)
    bubr.append(r)
    bubse.append(randint(1, maxbubse))


def buborekmozgat():
    for i in range(len(bubid)):
        v.move(bubid[i], -bubse[i], 0)

def koorker(azonosito):
    poz = v.coords(azonosito)
    x = (poz[0] + poz[2])/2
    y = (poz[1] + poz[3])/2
    return x, y

def bubtorol(i):
    del bubr[i]
    del bubse[i]
    v.delete(bubid[i])
    del bubid[i]

def bubtakarit():
    for i in range(len(bubid)-1, -1, -1):
        x, y = koorker(bubid[i])
        if x < -diff:
            bubtorol(i)
def tavolsag(id1, id2):
    x1, y1 = koorker(id1)
    x2, y2 = koorker(id2)
    return sqrt((x2 - x1)**2 + (y2 - y1)**2)

def utkozes():
    pontok = 0
    for bub in range(len(bubid)-1, -1, -1):
        if tavolsag(hajo2, bubid[bub]) < (hajo_r + bubr[bub]):
            pontok += (bubr[bub] + bubse[bub])
            bubtorol(bub)
    return pontok

v.create_text(50, 30, text = 'IDŐ', fill = 'white')
v.create_text(150, 30, text = 'PONSZÁM', fill = 'white')
idoszoveg = v.create_text(50, 50, fill = 'white')
pontszoveg = v.create_text(150, 50, fill = 'white')

def pontmutat(pontszam):
    v.itemconfig(pontszoveg, text = str(pontszam))

def idotmutat(maradekido):
     v.itemconfig(idoszoveg, text = str(maradekido))



bubvsz = 10
idolimit = 60
bonuszpont = 1000
pontszam = 0
bonusz = 0
vege = time() + idolimit
while time() < vege:
    hajomozgatas()
    if randint(1, bubvsz) == 1: 
        buborekgyartas()
    buborekmozgat()
    bubtakarit()
    pontszam += utkozes()
    if (int(pontszam / bonuszpont)) > bonusz:
        bonusz += 1
        vege += idolimit
    pontmutat(pontszam)
    idotmutat(int(vege - time()))                                  
    ablak.update()
    sleep(0.01)


v.create_text(kp_x, kp_y, \
    text = 'Vége a játéknak', fill = 'white', font = ('Helvetica', 30))
v.create_text(kp_x, kp_y + 30, \
    text = 'Pontszámod: '+ str(pontszam), fill = 'white')
v.create_text(kp_x, kp_y + 45,  \
    text = 'Bonuszidö: '+ str(bonusz*idolimit), fill = 'white')

ablak.update()
ablak.mainloop()
