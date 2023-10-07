import tkinter as tk
from math import sqrt, sin, cos, pi

root = tk.Tk()
sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
draw = tk.Canvas(width=sw, height=sh, bg="white")
draw.pack()