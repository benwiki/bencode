from tkinter import *
from time import sleep

lastcoords = None
vonal = []
vonalak = []


def coord(x, y, r):
    return x-r, y-r, x+r, y+r


def press(event):
    """x, y = event.x, event.y
    global lastcoords
    lastcoords=[x, y]
    vonal.append(lastcoords)"""
    global lastcoords
    x, y = event.x, event.y
    draw.create_oval(coord(x, y, 5), fill='black', width=5)
    lastcoords = [x, y]
    vonal.append(lastcoords)


def motion(event):
    global lastcoords
    x, y = event.x, event.y
    if lastcoords is not None:
        draw.create_line([x, y]+lastcoords, fill='black',
                         width=1, capstyle=ROUND)
        lastcoords = [x, y]
        vonal.append(lastcoords)


def release(event):
    global lastcoords
    x, y = event.x, event.y
    if lastcoords is not None:
        draw.create_line([x, y]+lastcoords, fill='black',
                         width=1, capstyle=ROUND)
        lastcoords = [x, y]
        vonal.append(lastcoords)
    # print (vonalak)


def save():
    f = open('gajjos.txt', 'w')
    f.write(str(vonalak))
    f.close()


def add():
    global vonal, lastcoords
    lastcoords = None
    vonalak.append(vonal)
    vonal = []


window = Tk()

w, h = window.winfo_screenwidth()/2, window.winfo_screenheight()/2
draw = Canvas(width=w, height=h, bg='white')
draw.pack()

saveButton = Button(text='MENTÉS', command=save)
saveButton.pack()

addButton = Button(text='hozzáad', command=add)
addButton.pack()

draw.bind('<Button-1>', press)
# draw.bind('<Motion>', motion)
# draw.bind('<ButtonRelease-1>', release)

mainloop()
