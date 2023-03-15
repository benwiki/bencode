from colorsys import *
from tkinter import *
from random import uniform
import struct
from time import sleep


# def to_rgb(amount):
#     return '#' + struct.pack(
#         'BBB', *[c*255 for c in hsv_to_rgb(
#             amount*0.7, 1, 1)]).encode('hex')


width = 1500
height = 500
db = 1000
lw = width/db

heights = [uniform(0, height) for i in range(db)]

window = Tk()
draw = Canvas(window, bg='white', height=height, width=width)
draw.pack()

lines = [draw.create_line(lw*2/3+i*lw, height-heights[i], lw*2/3+i*lw, height,
                          width=lw)
         for i in range(db)]

# -------------------------------------------------------------------------


def counting_sort(arr, exp1):
    n = len(arr)
    output = [0] * (n)
    count = [0] * (10)

    for i in range(n):
        index = (arr[i] / exp1)
        count[int(index % 10)] += 1

    for i in range(1, 10):
        count[i] += count[i - 1]

    lineoutput = [0]*n

    i = n - 1
    while i >= 0:
        index = (arr[i] / exp1)
        output[count[int(index % 10)] - 1] = arr[i]
        lineoutput[count[int(index % 10)] - 1] = lines[i]

        count[int(index % 10)] -= 1
        i -= 1

    for i in range(n):
        # window.update()
        arr[i] = output[i]
        lines[i] = lineoutput[i]
        draw.coords(lines[i], lw*2/3+i*lw, height-arr[i], lw*2/3+i*lw, height)


def radix_sort(arr):
    max1 = max(arr)

    exp = 1
    while max1 / exp > 1:
        print(max1, exp)
        window.update()
        sleep(1)
        counting_sort(arr, exp)
        exp *= 10


def slow_sort(arr):
    window.update()
    rendben = False
    while not rendben:
        window.update()
        rendben = True
        for i in range(1, db):
            if arr[i-1] < arr[i]:
                arr[i-1], arr[i] = arr[i], arr[i-1]
                x1 = draw.coords(lines[i-1])[0]
                x2 = draw.coords(lines[i])[0]
                draw.move(lines[i-1], -x1+x2, 0)
                draw.move(lines[i], -x2+x1, 0)
                lines[i], lines[i-1] = lines[i-1], lines[i]
                rendben = False


radix_sort(heights)
# slow_sort(heights)

mainloop()
