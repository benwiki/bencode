from PIL import Image
from typing import Tuple
from tkinter import Button, Label, Entry, StringVar, Tk, Text
from os import path
import re


class Mandelbrot:

    def __init__(self) -> None:
        self.res = {"width": 900, "height": 600}
        self.interval = {"bottom_left": -2 - 1j, "top_right": 1 + 1j}
        self.complex_border = 2
        self.iteration = 100
        self.picpath = "mandelbrot.png"

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

    # -----------------------------------------------------------------------------
    def render_mandelbrot(self, left_bottom: complex, right_top: complex,
                          width: int, height: int, m: int, cborder: int,
                          pic: str):
        img = Image.new('HSV', (width, height))
        for i in range(width):
            self.window.update()
            # print("Progress: ", round(i / width * 100, 2),
            #       "%", end="\r", sep='')  # print progress
            self.progress_label_var.set(
                f"Progress: {round(i / width * 100, 2)}%")
            for j in range(height):
                coords = self.sample(left_bottom, right_top, i, j,
                                     width, height)  # find the coordinate
                # check if it's in the mandelbrot set
                border = self.mandelbrot(coords, m, cborder)
                img.putpixel((i, j), self.color(border, m))
                if self.break_rendering:  # XXXXXXXX We break the rendering here  XXXXXXXXXX
                    self.break_rendering = False
                    self.progress_label_var.set("Progress: 0%")
                    return
        self.progress_label_var.set(f"Progress: DONE")
        img.convert('RGB').save(pic, quality=95)

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
    def render(self):
        match self.update():
            case "PATHERROR":
                self.progress_label_var.set("INVALID PATH")
                return
            case "EXTENSIONERROR":
                self.progress_label_var.set("EXTENSION MUST BE jp(e)g / png / gif!")
                return
            case "BREAK_RENDERING":
                return
            case "GOOD":
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

    #------------------------------------------------------------
    def update(self) -> str:
        if self.rendering:
            self.break_rendering = True
            return "BREAK_RENDERING"

        getpicpath = self.path_entry.get("1.0", "end").strip()
        pathre = re.search("([\w\s\:\\\/]+)[\\\/]+\w+\.(\w+)", self.raw(getpicpath))
        if pathre is None or not path.exists(pathre[1]):
            return "PATHERROR"
        elif (ext := re.match("jpe?g|png|gif", pathre[2])) is None or ext[0] != pathre[2]:
            return "EXTENSIONERROR"
        
        self.interval["bottom_left"] = eval(self.bottom_left_entry.get())
        self.interval["top_right"] = eval(self.top_right_entry.get())
        self.res = dict(zip(("width", "height"),
                            list(map(int, self.resolution_entry.get().split("x")))))
        self.iteration = int(self.iteration_entry.get())
        self.complex_border = int(self.bordernum_entry.get())
        self.picpath = getpicpath
        return "GOOD"

    # ---------------------------------------------------------------
    def do_the_tkinter_stuff(self):
        self.window = Tk()

        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()

        Label(self.window, text="Interval: Bottom_Left. Format: (-) <x> +/- <y>j").pack()
        self.bottom_left_entry = Entry(self.window)
        self.bottom_left_entry.insert(
            "end", str(self.interval["bottom_left"])[1:-1])
        self.bottom_left_entry.pack()

        Label(self.window, text="Interval: Top_Right. Format: (-) <x> +/- <y>j").pack()
        self.top_right_entry = Entry(self.window)
        self.top_right_entry.insert(
            "end", str(self.interval["top_right"])[1:-1])
        self.top_right_entry.pack()

        Label(self.window, text="Resolution. Format: <width> x <height>").pack()
        self.resolution_entry = Entry(self.window)
        self.resolution_entry.insert("end", str(
            self.res["width"])+" x "+str(self.res["height"]))
        self.resolution_entry.pack()

        Label(self.window, text="Iteration").pack()
        self.iteration_entry = Entry(self.window)
        self.iteration_entry.insert("end", str(self.iteration))
        self.iteration_entry.pack()

        Label(self.window, text="Complex Border Number").pack()
        self.bordernum_entry = Entry(self.window)
        self.bordernum_entry.insert("end", str(self.complex_border))
        self.bordernum_entry.pack()

        Label(self.window, text="Picture's full PATH with <name>.jpg").pack()
        self.path_entry = Text(self.window, width=(
            self.screen_width + self.screen_height)//50, height=3)
        self.path_entry.pack()

        self.progress_label_var = StringVar(
            self.window, value="Progress: No task")
        Label(self.window, textvariable=self.progress_label_var).pack()

        self.start = Button(
            self.window, text="Get picture!", command=self.render)
        self.start.pack()

        self.window.mainloop()
    ##################################################################

mbrot = Mandelbrot()
