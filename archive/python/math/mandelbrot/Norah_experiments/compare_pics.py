from PIL import Image

pics = [Image.open(f"output{i+1}.jpg") for i in range(5)]
pixels = [list(pic.getdata()) for pic in pics]
new_pic: list[tuple] = []
pic1 = pixels[0]
pic2 = pixels[2]
minimum_value = min(pic1[i][j] - pic2[i][j] for i in range(len(pixels[0])) for j in range(3))
for i in range(len(pixels[0])):
    new_pic.append(tuple(pic1[i][j] - pic2[i][j] - minimum_value for j in range(3)))

print(pic1[:5])
print(pic2[:5])
print(new_pic[:5])

width, height = 900, 600
img = Image.new('RGB', (width, height))
for i in range(width):
    for j in range(height):
        img.putpixel((i, j), new_pic[i*height + j])
img.save("compare1-2.jpg", quality=95)
