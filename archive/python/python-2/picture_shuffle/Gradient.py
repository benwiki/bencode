from PIL import Image
from time import sleep

img = Image.open(input('File dir & name: '))

w, h = img.size

gradient_border = int(input('Gradient border (max '+str(w)+'): '))
how_much = int(input('How much would you like to gradient: '))
other_side = w - gradient_border

product = Image.new('RGB', (w, h))
gradient = [[float(j)/gradient_border if j <= gradient_border
             else 1 for j in range(w)]
             for i in range(h)]

print (gradient[0][0])
print (img.getpixel((w-1,h-1)))

def multiply(pixel, x, y):
    cucc = [p for p in pixel]
    for i in range(3):
        cucc[i] *= pow(gradient[x][y], how_much)
    pixel = int(cucc[0]), int(cucc[1]), int(cucc[2])
    return pixel

for i in range(w):
    for j in range(h):
        product.putpixel((i, j), multiply(img.getpixel((i, j)), j, i))

product.save('Gradiented.png')

print('done')
