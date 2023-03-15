from tkinter import Scale, Tk, Canvas, Label
from tkinter.constants import HORIZONTAL
from hexconvert import to_hex
from multiplier import multiply

win = Tk()

w, h = 200, 200
draw = Canvas(width=w, height=h, bg='white')
draw.grid(columnspan=2)

# R_label = Label(text='R')
# G_label = Label(text='G')
# B_label = Label(text='B')

R_label, G_label, B_label = multiply(3, Label, kwargs={'text': })

def get_scale(w: int) -> Scale:
    return Scale(
        from_=0, to=255, length=w*0.7,
        width=20, orient=HORIZONTAL)


R, G, B = multiply(3, get_scale, args=(w))
lable_with_scale = zip((R_label, G_label, B_label), (R, G, B))
for i, (label, scale) in enumerate(lable_with_scale):
    label.grid(row=i + 1, column=0)
    scale.grid(row=i + 1, column=1)

colorlabel = Label()
colorlabel.grid(columnspan=2)

color = draw.create_rectangle(0, 0, w, h, fill='white', outline='white')

while True:
    fillcolor = to_hex(map(int, (R.get(), G.get(), B.get())))
    draw.itemconfig(color, fill=fillcolor, outline=fillcolor)
    colorlabel['text'] = fillcolor
    win.update()
