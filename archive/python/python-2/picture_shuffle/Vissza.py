from PIL import Image
from random import randint, shuffle
from pathlib import Path

img = Image.open("C:\out22.png")

w, h = img.size

shambled = Image.new('RGB', (w, h))

kevert = open("teszt2.txt", 'r').read()
print 'Beolvasas kesz'

pos = []
pos = eval(kevert)
print 'Fejtes kesz'

print(len(pos), w, h)
print(pos[0], pos[1], pos[2])
print(img.getpixel((w-1,h-1)))

index = -1

for i in range(w):
    for j in range(h):
        index = index+1
        shambled.putpixel((i, j), img.getpixel(pos[index]))


print('done')

shambled.save('back.png')



