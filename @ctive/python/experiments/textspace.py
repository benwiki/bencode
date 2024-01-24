"""
Description of the program:

The program creates a text in a random position with a random angle and
random size. The text is moving in the direction of the angle with a
predefined speed. The text is growing until it reaches a predefined
size. After that it disappears.
"""

import tkinter as tk
from math import cos, pi, sin
from random import randint, uniform

root = tk.Tk()
root.attributes("-fullscreen", True)
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
draw = tk.Canvas(width=w, height=h, bg="#081729", highlightthickness=0)
draw.pack()

texts: list[dict] = []
SPEED = 100

while True:
    texts.append({
        'obj': draw.create_text(
            # uniform(w/3, w*2/3), uniform(h/3, h*2/3),
            w/2, h/2,
            text="Üdvözöllek az Életben!", font=("Purisa", 0)),
        'size': 0,
        'angle': 0,
        'diff': 0,
    })
    to_delete = []

    for txt in texts:
        txt_obj, size, angle, diff = txt.values()

        if size >= 100:
            draw.delete(txt_obj)
            to_delete.append(txt)
            continue

        if size == 0:
            angle = randint(0, 1000)/1000*2*pi
            diff = w/150
            draw.move(txt_obj, diff*cos(angle), diff*sin(angle))
            txt['angle'] = angle
            txt['diff'] = diff
        else:
            diff += diff/SPEED
            draw.move(txt_obj, diff*cos(angle), diff*sin(angle))
            txt['diff'] = diff
        size += 1
        draw.itemconfig(txt_obj, font=("Purisa", size))
        txt['size'] = size

    for txt in to_delete:
        texts.remove(txt)
    root.update()
