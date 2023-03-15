from time import time
from tkinter import Tk, Canvas
from keyboard import is_pressed
from random import randint, uniform
from math import radians, cos, sin, hypot

# To be rewrote!

width = 1400
height = 700
x, y = width/2, height/2
r = 50
speed = 6
shagpiles = []
chance = 1
chance_of_mould = 30
min, max = 10, 20

timeborder = 0.01
t = time()
kx, ky = 0, 0

win = Tk()
draw = Canvas(width=width, height=height, bg='white')
draw.pack()


def rect_coordinates(x, y):
    return [x-r, y-r, x+r, y+r]


def help(i):
    global min, max
    r = radians(uniform(0, 90)+i*90)
    d = uniform(min, max)
    a, b = cos(r)*d+kx, sin(r)*d+ky
    return [a, b]


def getshape():
    global kx, ky
    kx, ky = randint(5, width-5), randint(5, height-5)
    return help(0)+help(1)+help(2)+help(3)


def distance(sz):
    return hypot(sz[1][0]-x, sz[1][1]-y)


auto = draw.create_oval(rect_coordinates(x, y), width=5)

while True:
    while time()-t < timeborder:
        pass
    t = time()
    if randint(1, chance) == 1:
        if randint(1, chance_of_mould) == 1:
            color = 'lightgreen'
        else:
            color = 'grey'
        shagpiles.append([draw.create_polygon(
            getshape(), fill=color), [kx, ky]])
    if is_pressed('up_arrow') and not y-r-speed < 0:
        y -= speed
    elif is_pressed('down_arrow') and not y+r+speed > height:
        y += speed
    if is_pressed('left_arrow') and not x-r-speed < 0:
        x -= speed
    elif is_pressed('right_arrow') and not x+r+speed > width:
        x += speed

    to_remove = []
    for shag in shagpiles:
        if distance(shag) < min + r:
            to_remove.append(shag)
    for elem in to_remove:
        draw.delete(elem[0])
        shagpiles.remove(elem)
    draw.coords(auto, rect_coordinates(x, y))
    win.update()
