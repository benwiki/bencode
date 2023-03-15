from PIL import Image, ImageDraw
from time import sleep

import tkinter as tk
window = tk.Tk()


def coord(x, y, r):
    return (x-r, y-r, x+r, y+r)


def draw_gaj_fractal(depth, x, y, size=2.0):
    if depth > 0:
        new_size = size / len(gaj)/20
        i = 0
        for line in gaj:
            j = 0
            for point in line:
                draw_gaj_fractal(
                    depth-1, x+point[0]*size, y+point[1]*size, new_size)
                j += 1
            i += 1
    else:
        # draw.create_oval(coord(x, y, size), fill = 'black')
        draw2.ellipse(coord(int(x), int(y), size),
                      fill='black', outline='black')


w, h = window.winfo_screenwidth(), window.winfo_screenheight()
"""draw = Canvas(width = w, height = h, bg = 'white')
draw.pack()"""

f = open('gajjos.txt', 'r')
gaj = eval(f.read())
f.close()
print(len(gaj), len(gaj[0]))

width_koz = w/len(gaj[0])
height_koz = h/len(gaj)
print(width_koz, height_koz)

image1 = Image.new("RGB", (w, h), (255, 255, 255))
draw2 = ImageDraw.Draw(image1)

"""draw_gaj_fractal(3, 0, 0, 2.01)
#draw.ellipse((50, 50, 50.5, 50.5), fill='black')

image1.save("myimage.png")

print('done')"""

s = 2.0
count = 1
local_x, local_y = 0.0, 0.0
for i in range(95):
    # draw.delete(ALL)
    draw_gaj_fractal(3, local_x, local_y, s)
    # window.update()
    local_x -= 45.48*2
    local_y -= 37.48*2
    s += 0.4
    image1.save("myimage"+str(count)+".png")
    draw2.rectangle((0, 0, w, h), fill=(255, 255, 255))
    print(count)
    count += 1

# mainloop()
