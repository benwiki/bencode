from typing import Any
from PIL import Image
from tkinter import LEFT, Frame, Label, Scale, Tk, Canvas, Button
"""
Oh my God, what have I done...
"""

w, h = 900, 1000
rejtveny = Image.new('RGB', (w, h))

for i in range(w):
    for j in range(h):
        rejtveny.putpixel((i, j), (0, 0, 0))

print('cleared')


def drect(line, col):
    for i in range(line[0], line[2]):
        for j in range(line[1], line[3]):
            rejtveny.putpixel((i, j), col)


v = 5
rows, cols = 10, 9
x = h//rows
y = w//cols

kell = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 0, 0, 0, 1, 0, 0],
        [0, 1, 1, 1, 0, 1, 1, 0, 0],
        [0, 2, 2, 2, 2, 2, 2, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 0, 0],
        [0, 1, 3, 3, 3, 3, 3, 3, 0],
        [0, 1, 0, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]]

color = (255, 255, 255)

for i in range(rows):
    for j in range(cols):
        if kell[i][j] == 0:
            a, b, c, d = 0, 0, 0, 0
            if i > 0 and kell[i-1][j]:
                b = v
            if i < rows-1 and kell[i+1][j]:
                d = v
            if j > 0 and kell[i][j-1]:
                a = v
            if j < cols-1 and kell[i][j+1]:
                c = v
            r = [j*x+a, i*y+b, j*x+x-c, i*y+y-d]
            drect(r, color)
        elif kell[i][j] == 1:
            r = [j*x+v, i*y+v, j*x+x-v, i*y+y-v]
            drect(r, color)
        elif kell[i][j] == 2:
            r = [j*x-v, i*y-v, j*x+x+v, i*y+y+v]
            drect(r, (255, 0, 0))
            r = [j*x+v, i*y+v, j*x+x-v, i*y+y-v]
            drect(r, color)
        else:
            r = [j*x, i*y, j*x+x, i*y+y]
            drect(r, (150, 150, 150))
            r = [j*x+v, i*y+v, j*x+x-v, i*y+y-v]
            drect(r, color)


class CrosswordGenerator(Tk):
    def __init__(self) -> None:
        super().__init__()
        self.define_variables()
        self.add_objects()
        self.config_objects()
        self.place_objects()
        self.draw_grid()
        self.mainloop()

    def define_variables(self):
        self.color = 'black'
        self.rect_borderwidth = 5
        self.w, self.h = 500, 500
        self.row_num, self.col_num = 5, 5
        self.confirmed = True
        self.edited: dict[tuple[float, float], Any] = {}
        self.last_block: tuple[int, int] = (-1, -1)

    def add_objects(self):
        self.draw = Canvas(self, width=self.w, height=self.h, bg='white')
        self.row_scale = Scale(
            self, from_=1, to=20, length=self.w*2/3,
            label='Number of rows', orient='horizontal',
            command=lambda _: self.draw_grid())
        self.col_scale = Scale(
            self, from_=1, to=20, length=self.w*2/3,
            label='Number of columns', orient='horizontal',
            command=lambda _: self.draw_grid())

    def config_objects(self):
        self.row_scale.set(self.row_num)
        self.col_scale.set(self.col_num)
        self.bind('<Key>', self.key_pressed)
        self.draw.bind('<B1-Motion>', self.mouse_moved)

    def key_pressed(self, key):
        if key.char == 'r':
            self.color = 'red'
        elif key.char == 'g':
            self.color = 'gray'
        elif key.char == 'b':
            self.color = 'black'
        elif key.char == ' ':
            self.color = ''

    def mouse_moved(self, event):
        self.edit_in_progress = True
        w = self.w / self.row_num
        h = self.h / self.col_num
        x = self.adjust(event.x, w)
        y = self.adjust(event.y, h)
        if (x, y) in self.edited:
            self.draw.delete(self.edited[(x, y)])
        self.edited[(x, y)] = self.draw.create_rectangle(
            self.rect_coords(x, y, w, h),
            width=self.rect_borderwidth, outline=self.color)

    def adjust(self, x: float, y: float) -> float:
        return x - x % y

    def rect_coords(self, x, y, w, h):
        return (x, y, x + w, y + h)

    def place_objects(self):
        self.draw.pack()
        self.row_scale.pack()
        self.col_scale.pack()

    def draw_grid(self):
        if not self.confirmed:
            return
        if len(self.edited) != 0:
            if not self.confirm_window(
                    'Editing in progress. \nAre you sure, '
                    'you want to \nchange the grid size?'):
                self.confirmed = True
                self.row_scale.set(self.row_num)
                self.col_scale.set(self.col_num)
                return
        self.edited = {}

        self.draw.delete('all')
        self.row_num = int(self.row_scale.get())
        self.col_num = int(self.col_scale.get())
        for i in range(1, self.row_num):
            self.draw.create_line(self.line_coords(i, self.row_num, 'HOR'))
        for i in range(1, self.col_num):
            self.draw.create_line(self.line_coords(i, self.col_num, 'VER'))

    def line_coords(self, i, lineNum, mode):
        match mode:
            case 'HOR':
                return (
                    i * self.w / lineNum, 0,
                    i * self.w / lineNum, self.w
                )
            case 'VER':
                return (
                    0, i * self.h / lineNum,
                    self.h, i * self.h / lineNum
                )

    def confirm_window(self, message: str):
        self.confirmed = False
        self.done = False

        def choice(confirmed: bool):
            self.confirmed = confirmed
            self.done = True
            confirm_win.destroy()

        size, x_raw, y_raw = self.geometry().split('+')
        w_raw, h_raw = size.split('x')
        w, h, x, y = tuple(map(int, (w_raw, h_raw, x_raw, y_raw)))

        bg, fg = 'black', 'white'
        confirm_win = Tk()
        confirm_win.config(bg=bg)
        confirm_win.geometry(f'200x100+{x + w // 2 - 100}+{y + h // 2 - 50}')
        confirm_win.overrideredirect(True)
        message_label = Label(confirm_win, bg=bg, fg=fg, text=message)
        message_label.pack()
        yes_btn = Button(
            confirm_win, text="Yes", bg="dark blue",
            fg=fg, command=lambda: choice(True), width=10)
        yes_btn.pack(padx=10, pady=10, side=LEFT)
        no_btn = Button(
            confirm_win, text="No", bg="dark blue",
            fg=fg, command=lambda: choice(False), width=10)
        no_btn.pack(padx=10, pady=10, side=LEFT)
        while not self.done:
            confirm_win.lift()
            self.update()
        return self.confirmed


cw = CrosswordGenerator()

print('modified')
rejtveny.save('rejtveny.png')
print('saved')
