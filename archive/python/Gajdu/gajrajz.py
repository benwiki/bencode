from tkinter import *
from PIL import Image, ImageDraw
from time import sleep, time
window = Tk()

def coord(x, y, r):
    return x-r, y-r, x+r, y+r

def draw_gaj_fractal(depth, x, y, size = 2.0):
    if depth > 0:
        new_size = size/len(gaj)/20
        for line in gaj:
            for point in line:
                draw_gaj_fractal(depth-1, x+point[0]*size, y+point[1]*size, new_size)
    else:
        #draw.create_oval(coord(x, y, size), fill = 'black')
        draw_image.ellipse(coord(int(x), int(y), size), fill='black', outline='black')

w, h = window.winfo_screenwidth(), window.winfo_screenheight()
"""draw = Canvas(width = w, height = h, bg = 'white')
draw.pack()"""

f = open('gajjos.txt', 'r')
gaj = eval(f.read())
f.close()
print (len(gaj), len(gaj[0]))

width_koz = w/len(gaj[0])
height_koz = h/len(gaj)
print (width_koz, height_koz)

image1 = Image.new("RGB", (w, h), (255,255,255))
draw_image = ImageDraw.Draw(image1)

"""draw_gaj_fractal(2, 0.0, 0.0)

image1.save("elso.png")

print('done')
"""

s=2.0
local_x, local_y = 0.0, 0.0
for i in range(95):
    draw_gaj_fractal(3, local_x, local_y, s)
    """local_x-=20
    local_y-=16
    window.update()
    s+=0.1"""

    #window.update()
    local_x-=45.48*2
    local_y-=37.48*2
    """local_x-=114.53
    local_y-=56.27"""
    s*=1.2
    image1.save("Gaj-"+str(i+1)+".png")
    draw_image.rectangle([0, 0, w, h], fill=(255, 255, 255))

mainloop()
