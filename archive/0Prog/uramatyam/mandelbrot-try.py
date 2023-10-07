from tkinter.constants import HORIZONTAL
from PIL import Image
from typing import Tuple
from tkinter import Button, Canvas, Label, Entry, Scale, StringVar, Tk, Text
from os import path
import re
import colorsys


class Mandelbrot:

    def __init__(self) -> None:
        self.res = {"width": 90, "height": 60}
        self.interval = {"bottom_left": -2 - 1j, "top_right": 1 + 1j}
        self.complex_border = 2
        self.iteration = 40
        self.picpath = "mandelbrot.png"

        self.drawres = {"width": 450, "height": 300}
        self.draw_pos = {'x': 0, 'y': 0}
        self.modified_res = 1

        self.rendering = False
        self.break_rendering = False

        self.do_the_tkinter_stuff()

    # ----------------------------------------------------------------------------
    def mandelbrot(self, c: complex, m: int, complex_border: int = 2) -> int:
        num: complex = 0 + 0j
        for i in range(1, m + 1):
            num = num ** 2 + c
            if abs(num) > complex_border:
                return i
        return m

    # -----------------------------------------------------------------------------
    def sample(self, z: complex, w: complex,
               x: int, y: int,
               sx: int, sy: int) -> complex:
        return complex(z.real + (x / sx) * (w.real - z.real),  # mapping X coord
                       z.imag + (y / sy) * (w.imag - z.imag))  # mapping Y coord

    def coordinates(self, x, y, r):
        return (x-r, y-r, x+r, y+r)

    def rgb_to_hex(self, rgb: tuple) -> str:
        return '#%02x%02x%02x' % rgb
    
    def _from_rgb(self, rgb: tuple):
        """translates an rgb tuple of int to a tkinter friendly color code
        """
        # print(rgb)
        r, g, b = map(int, rgb)
        return f'#{r:02x}{g:02x}{b:02x}'

    # -----------------------------------------------------------------------------
    def render_mandelbrot(self, left_bottom: complex, right_top: complex,
                          width: int, height: int, render_iter: int, cborder: int,
                          pic: str = "", on_canvas: bool = False):
        if on_canvas:
            self.draw.delete("all")
            print("im here", self.res)
        else:
            img = Image.new('HSV', (width, height))
        for i in range(width):
            self.window.update()
            # print("Progress: ", round(i / width * 100, 2),
            #       "%", end="\r", sep='')  # print progress
            if not on_canvas:
                self.progress_label_var.set(
                    f"Progress: {round(i / width * 100, 2)}%")
            for j in range(height):
                coords = self.sample(left_bottom, right_top, i, j,
                                     width, height)  # find the coordinate
                # check if it's in the mandelbrot set
                border = self.mandelbrot(coords, render_iter, cborder)
                if on_canvas:
                    h, s, v = self.color(border, render_iter)
                    h, s = h/255, s/255
                    # print(self.color(border, render_iter))
                    """self.draw.create_rectangle(i/self.res["width"]*self.drawres["width"],
                                               j/self.res["height"]*self.drawres["height"],
                                               (i+1)/self.res["width"]*self.drawres["width"],
                                               (j+1)/self.res["height"]*self.drawres["height"],
                                          width=1, fill=self._from_rgb(colorsys.hsv_to_rgb(h, l, s)), outline="")"""
                    # print((255 - border//render_iter * 255,) * 3)
                    self.draw.create_rectangle(i/self.res["width"]*self.drawres["width"],
                                               j/self.res["height"]*self.drawres["height"],
                                               (i+1)/self.res["width"]*self.drawres["width"],
                                               (j+1)/self.res["height"]*self.drawres["height"],
                                               width=1, fill=self._from_rgb(colorsys.hsv_to_rgb(h, s, v)), outline="")
                                            # width=1, fill=self.rgb_to_hex((255 - int(border/render_iter * 255),)*3), outline="")
                                        #   width=1, fill='#'+''.join([str(hex(16-col//16))[-1] for col in self.color(border, m)]), outline="")
                else:
                    img.putpixel((i, j), self.color(border, render_iter))
                if self.break_rendering:  # XXXXXXXX We break the rendering here  XXXXXXXXXX
                    self.break_rendering = False
                    self.progress_label_var.set("Progress: 0%")
                    return
        if not on_canvas:
            self.progress_label_var.set(f"Progress: DONE")
            img.convert('RGB').save(pic, quality=95)
        print("hey ready")
        self.window.update()

    # -------------------------------------------------------------------------------
    def color(self, i: int, max_i: int) -> Tuple[int, int, int]:
        # Farbton in Abhängigkeit der benötigten Schleifendurchläufe.
        hue = int(255 * (i / max_i))
        # Volle Helligkeit 255, außer wenn c Teil der Mandelbrotmenge ist.
        # Dadurch wird das innere schwarz.
        value = 255 if i < max_i else 0
        # Volle Sättigung
        saturation = 255
        return (hue, saturation, value)

    # -------------------------------
    def raw(self, s: str) -> str:
        return repr(s)[1:-1]

    # -------------------------------
    def render(self, by_button=False):
        if by_button:
            if True:
                if self.update(by_button) ==  "PATHERROR":
                    self.progress_label_var.set("INVALID PATH")
                    return
                elif self.update(by_button) == "EXTENSIONERROR":
                    self.progress_label_var.set(
                        "EXTENSION MUST BE jp(e)g / png / gif!")
                    return
                elif self.update(by_button)== "BREAK_RENDERING":
                    return
                elif self.update(by_button)== "GOOD":
                    pass
            self.rendering = True
            self.start.config(text="STOP")
            self.render_mandelbrot(
                self.interval["bottom_left"], self.interval["top_right"],
                # Intervall auf der komplexen Ebene.
                # Auflösung des zu erzeugenden Bildes.
                self.res["width"], self.res["height"],
                self.iteration,  # Anzahl maximaler Schleifendurchläufe.
                self.complex_border,
                self.picpath)
            self.rendering = False
            self.start.config(text="Get picture!")
        else:
            self.update(False)
            self.render_mandelbrot(
                self.interval["bottom_left"], self.interval["top_right"],
                # Intervall auf der komplexen Ebene.
                # Auflösung des zu erzeugenden Bildes.
                self.res["width"], self.res["height"],
                self.iteration,  # Anzahl maximaler Schleifendurchläufe.
                self.complex_border,
                self.picpath,
                on_canvas=True)

    # ------------------------------------------------------------
    def update(self, by_button) -> str:
        if by_button:
            if self.rendering:
                self.break_rendering = True
                return "BREAK_RENDERING"

            getpicpath = self.path_entry.get("1.0", "end").strip()
            pathre = re.search(
                "([\w\s\:\\\/]+)[\\\/]+\w+\.(\w+)", self.raw(getpicpath))
            if pathre is None or not path.exists(pathre[1]):
                return "PATHERROR"
            elif (ext := re.match("jpe?g|png|gif", pathre[2])) is None or ext[0] != pathre[2]:
                return "EXTENSIONERROR"

            self.picpath = getpicpath

        """self.interval["bottom_left"] = eval(self.bottom_left_entry.get())
        self.interval["top_right"] = eval(self.top_right_entry.get())
        self.res = dict(zip(("width", "height"),
                            list(map(int, self.resolution_entry.get().split("x")))))
        self.iteration = int(self.iteration_entry.get())
        self.complex_border = int(self.bordernum_entry.get())
        self.picpath = getpicpath"""
        self.res = dict(zip(("width", "height"),
                            [int(size * self.resolution_scale.get()) for size in [90, 60]]))
        self.iteration = self.iteration_scale.get()
        self.complex_border = self.bordernum_scale.get()
        return "GOOD"

    # ---------------------------------------------------------------
    def do_the_tkinter_stuff(self):
        self.window = Tk()

        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()

        Label(self.window, text="Picture's full PATH with <name>.jpg").pack()
        self.path_entry = Text(self.window, width=(
            self.screen_width + self.screen_height)//50, height=3)
        self.path_entry.pack()

        self.progress_label_var = StringVar(
            self.window, value="Progress: No task")
        Label(self.window, textvariable=self.progress_label_var).pack()

        self.start = Button(
            self.window, text="Get picture!", command=lambda: self.render(True))
        self.start.pack()

        self.draw = Canvas(self.window, background="white",
                           width=self.drawres["width"],
                           height=self.drawres["height"])
        self.draw.pack()

        Label(self.window, text="Resolution").pack()
        self.resolution_scale = Scale(
            self.window, from_=0.1, to=30, orient=HORIZONTAL, resolution=0.01,length=400)
        self.resolution_scale.set(1)
        self.resolution_scale.pack()

        Label(self.window, text="Iteration").pack()
        self.iteration_scale = Scale(
            self.window, from_=1, to=1000, orient=HORIZONTAL, length=400)
        self.iteration_scale.set(self.iteration)
        self.iteration_scale.pack()

        Label(self.window, text="Complex Border Number").pack()
        self.bordernum_scale = Scale(
            self.window, from_=1, to=100, orient=HORIZONTAL, length=400)
        self.bordernum_scale.set(self.complex_border)
        self.bordernum_scale.pack()

        """self.draw.bind("<Button-1>", self.press)
        self.draw.bind("<Motion>", self.motion)"""
        self.draw.bind("<ButtonRelease-1>", self.release)
        self.window.bind("<Key>", self.key)

        self.draw.bind("<MouseWheel>", self.do_zoom)
        self.draw.bind('<ButtonPress-1>', self.press)
        self.draw.bind("<B1-Motion>", lambda event: self.draw.scan_dragto(event.x, event.y, gain=1))

        self.render()

        self.window.mainloop()

    def adjust_and_render(self):
        self.draw.scan_mark(*self.draw_pos.values())
        self.draw.scan_dragto(0, 0, gain=1)

        diff = self.interval["top_right"] - self.interval["bottom_left"]
        interval_w, interval_h = diff.real, diff.imag

        bl_add_x = interval_w * (-self.draw_pos['x'] / self.drawres['width']) + (interval_w * (1 - 1/self.modified_res))/2
        bl_add_y = interval_h * (-self.draw_pos['y'] / self.drawres['height']) + (interval_h * (1 - 1/self.modified_res))/2
        tr_add_x = interval_w * (-self.draw_pos['x'] / self.drawres['width']) - (interval_w * (1 - 1/self.modified_res))/2
        tr_add_y = interval_h * (-self.draw_pos['y'] / self.drawres['height']) - (interval_h * (1 - 1/self.modified_res))/2

        self.interval["bottom_left"] += complex(bl_add_x, bl_add_y)
        self.interval["top_right"] += complex(tr_add_x, tr_add_y)

        self.draw_pos.update(x=0, y=0)
        self.modified_res = 1
        self.render()

    def press(self, event):
        self.scan_mark_pos = (event.x, event.y)
        self.draw.scan_mark(event.x, event.y)

    def release(self, event):
        self.draw_pos['x'] += event.x - self.scan_mark_pos[0]
        self.draw_pos['y'] += event.y - self.scan_mark_pos[1]
        self.adjust_and_render()

    def do_zoom(self, event):
        
        # x = self.draw.canvasx(event.x)
        # y = self.draw.canvasy(event.y)
        factor = 1.001 ** event.delta
        self.modified_res *= factor
        self.draw.scale("all",
                        self.drawres["width"] /2 - self.draw_pos['x'],
                        self.drawres["height"]/2 - self.draw_pos['y'],
                        factor, factor)
        # self.iteration *= factor
        # self.iteration_scale.set(self.iteration)
        # print(self.iteration)
        
        # diff = self.interval["top_right"] - self.interval["bottom_left"]
        # interval_w, interval_h = diff.real, diff.imag
        # self.interval["bottom_left"] += complex((interval_w *  (1 - 1/factor))/8,
        #                                         (interval_h * (1 - 1/factor))/8)
        # self.interval["top_right"] -= complex((interval_w *  (1 - 1/factor))/8,
        #                                         (interval_h * (1 - 1/factor))/8)
        
    def key(self, event):
        if event.char == " ":
            self.adjust_and_render()

        elif event.char == "b":
            print(self.modified_res)

    ##################################################################

mbrot = Mandelbrot()
