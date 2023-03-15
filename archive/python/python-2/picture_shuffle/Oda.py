from PIL import Image
from random import randint, shuffle

img = Image.open('back.png')

w, h = img.size

shambled = Image.new('RGB', (w, h))

pos = []

for i in range(w):
    for j in range(h):
        pos.append((i, j))

shuffle(pos)

f = open("teszt2.txt", 'w')
print("file opened")
f.write(str(pos))
print("file done")
f.close()

print(len(pos), w, h)
print(pos[0], pos[1], pos[2])
print(img.getpixel((w-1,h-1)))

index = -1

for i in range(w):
    for j in range(h):
        index = index+1
        shambled.putpixel(pos[index], img.getpixel((i, j)))


print('done')

shambled.save('out22.png')



