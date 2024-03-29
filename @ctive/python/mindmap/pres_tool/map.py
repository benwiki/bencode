#!/usr/bin/python
# -*- coding: utf-8 -*-

from bisect import insort_right
import tkinter as tk
from mdMapTools import extract_mindmap
from dataclasses import dataclass
from math import cos, pi, sin
from typing import Optional
import re

# ################################ #
# ###--------Parameters--------### #
# ################################ #

projectName = "Buddhismus"

platform = "desktop"  # "mobile" / "desktop"
conn_len = 1.5
rad_scale = 0.2
txtScale = 15
txtShrink = 0.4
zoomScale = 2
tab = ' '*4
showPercentage = False


def run_map(text: str, name: str):
    block = convert_to_map(text, name)
    # ~~~~~~~~~~~~~~~~~~~~~~~~
    theme = darkTheme  # darkTheme / lightTheme
    prStyle = ProgressStyle(theme, "sector")  # "sector" / "arc"
    # ~~~~~~~~~~~~~~~~~~~~~~~~
    MindMap(block, theme, prStyle).start()


class Theme:
    bg: str  # background
    altbg: str  # alternative background
    fg: str  # foreground
    bd: str  # border
    pr: str  # progress

    def __init__(self, properties: dict):
        assert (set(properties.keys()) ==
                {'bg', 'altbg', 'fg', 'bd', 'pr'}),\
                "False attributes for Theme object!"
        self.__dict__ = properties


darkTheme = Theme({
    "bg": "#101045",
    "altbg": "#88AAAA",
    "fg": "white",
    "bd": "gray",
    "pr": "green"
})

lightTheme = Theme({
    "bg": "white",
    "altbg": "lightgrey",
    "fg": "black",
    "bd": "grey",
    "pr": "lightgreen"
})

##################################
##################################
##################################


class ProgressStyle:
    def __init__(self, theme: Theme, mode: str):
        if mode == "arc":
            self.arcOutline = theme.pr
            self.arcFill = ""
            self.arcWidth = 4
            self.style = "arc"
        elif mode == "sector":
            self.arcOutline = theme.bd
            self.arcFill = theme.pr
            self.arcWidth = 1
            self.style = ""
        else:
            raise ValueError("ProgressStyle mode " +
                             f'"{mode}" incompatible!')
        self.mode = mode


@dataclass
class Block:
    text: str
    progress: float
    parent: Optional["Block"]
    children: list["Block"]


def zero_int(text):
    return 0 if text == "" else int(text)


def match_text(text: str) -> Optional[tuple[int, Block]]:
    m = re.fullmatch(r'(\s*)([^;]+);?\s*(\d*)', text)
    if not m:
        return None
    intend, name, percent = m.groups()
    return (intend.count('\t') + intend.count(tab),
            Block(name, zero_int(percent), None, []))


def convert_to_map(string: str, name: str) -> Block:
    start: Block = Block(name, 0, None, [])
    cur_block = Block("", 0, start, [])
    blocks = string.strip().split('\n')
    prev_intend = 0
    for i, block in enumerate(blocks):
        block_match = match_text(block)
        if block_match is None:
            raise RuntimeError(f'"{block}" doesn\'t match (line ~{i})!')
        intendation, new_block = block_match
        if intendation > prev_intend + 1 or cur_block is None:  # bc of mypy
            raise RuntimeError(f"Too high intendation "
                               f"({intendation}) on text \"{block}\"!")
        elif intendation == prev_intend + 1:
            new_block.parent = cur_block
        elif intendation == prev_intend:
            new_block.parent = cur_block.parent
        else:
            back = prev_intend - intendation
            while back > 0:
                if cur_block.parent is None:
                    raise RuntimeError("You can't use "
                                       "negative intendations!")
                cur_block = cur_block.parent
                back -= 1
            new_block.parent = cur_block.parent
        if new_block.parent is None:
            raise RuntimeError("You can't use negative intendations!")
        cur_block = new_block
        new_block.parent.children.append(cur_block)
        prev_intend = intendation
    return start


@dataclass
class Coord:
    x: int
    y: int


class MindMap:
    def start(self):
        self.draw_map(self.map)
        tk.mainloop()

    def __init__(self, block: Block, theme: Theme, prStyle: ProgressStyle):
        self.map = block
        self.theme = theme
        self.prStyle = prStyle
        self.init_win()
        self.init_attributes()
        self.init_draw()
        if platform == "mobile":
            self.init_zoom()

    def init_win(self):
        self.win = tk.Tk()
        self.win["bg"] = self.theme.bg
        self.win.bind("<ButtonRelease-1>", self.winrelease)
        self.w = float(self.win.winfo_screenwidth())
        self.h = float(self.win.winfo_screenheight())
        self.draw_w, self.draw_h = self.w, self.h
        if platform == "mobile":
            self.draw_h *= 0.85

    def init_attributes(self):
        self.draw_pos = Coord(0, 0)
        self.texts: list[dict[str, int]] = []
        self.resolution = 1
        self.scalepos = 0
        self.start_radius = self.draw_w/12
        self.txtshowres = (self.draw_w+self.draw_h)/70

    def init_draw(self):
        self.draw = tk.Canvas(
            self.win,
            width=self.draw_w,
            height=self.draw_h,
            background=self.theme.bg,
            highlightthickness=0
        )
        self.draw.bind("<MouseWheel>", self.scrollzoom)
        self.draw.bind("<ButtonRelease-1>", self.release)
        self.draw.bind('<ButtonPress-1>', self.press)
        self.draw.bind("<B1-Motion>", lambda event:
                       self.draw.scan_dragto(event.x, event.y, gain=1))
        self.draw.pack()

    def init_zoom(self):
        self.zoom = tk.Scale(
            self.win,
            from_=-100, to=100,
            orient=tk.HORIZONTAL,
            length=self.w*0.9, width=self.h*0.04,
            sliderlength=100,
            command=self.scalezoom,
            bg=self.theme.bg,
            highlightthickness=0,
            activebackground=self.theme.bg,
            troughcolor=self.theme.altbg,
            fg=self.theme.fg
        )
        self.zoom.set(0)
        self.zoom.pack()

    def oval_coords(self, x, y, r):  # r ~ radius
        return (x-r, y-r, x+r, y+r)

    def rot_coord(self, x, y, r, rot):  # r ~ radius, rot ~ rotation
        rot *= 2*pi
        return (x + cos(rot)*r, y + sin(rot)*r)

    def line_rotate(self, x, y, s, e, rot):  # s ~ start radius, e ~ end rad.
        return (*self.rot_coord(x, y, s, rot), *self.rot_coord(x, y, e, rot))

    def draw_map(self, block: Block, x=None, y=None, r=None, rot=0.0):
        if x is None:
            x = self.draw_w/2
        if y is None:
            y = self.draw_h/2
        if r is None:
            r = self.start_radius

        child_num = len(block.children)
        plus_rot = (child_num % 2 == 0 and block.parent is not None)
        progress = 0
        for i in range(child_num):
            rotation = (i / child_num + rot
                        + (0.5/child_num if plus_rot else 0))
            self.draw.create_line(
                self.line_rotate(x, y, r, r*conn_len, rotation),
                fill=self.theme.bd
            )
            linerot = self.rot_coord(
                x, y, r*conn_len + r*rad_scale, rotation
            )
            if block.progress > 0:
                block.children[i].progress = block.progress
            progress += self.draw_map(
                block.children[i],
                linerot[0], linerot[1],
                r*rad_scale, rotation
            )

        if child_num != 0:
            avg_progress = progress / child_num
            block.progress = avg_progress

        if block.progress < 1:
            block.progress = 0

        self.draw_block(block, x, y, r)
        self.draw_text(block, x, y, r)
        return block.progress

    def draw_block(self, block: Block, x: float, y: float, r: float):
        self.draw.create_oval(
            self.oval_coords(x, y, r),
            outline=self.theme.bd,
            fill=self.circle_fill(block.progress))
        self.draw.create_arc(
            self.oval_coords(x, y, r),
            extent=block.progress/100*359.999,
            style=self.prStyle.style,
            outline=self.arc_outline(block.progress),
            fill=self.arc_fill(block.progress),
            width=self.prStyle.arcWidth)

    def draw_text(self, block: Block, x, y, r):
        block_txt = block.text
        if showPercentage:
            block_txt += f"\n{round(block.progress)} %"
        textSize = self.resolution * r * txtScale
        textSize = int(textSize ** txtShrink)
        self.texts += [{'r': r, 'obj': self.draw.create_text(
            x, y, text=block_txt,
            fill=(self.theme.fg if r >= self.txtshowres else ""),
            font=('Consolas', textSize),
            justify="center"
        )}]

    def circle_fill(self, progress):
        return (self.theme.pr
                if self.prStyle.mode == "sector" and progress == 100
                else self.theme.bg)

    def arc_fill(self, progress):
        return (""
                if self.prStyle.mode == "sector" and progress == 100
                else self.prStyle.arcFill)

    def arc_outline(self, progress):
        return (""
                if self.prStyle.mode == "sector" and not 0 < progress < 100
                else self.prStyle.arcOutline)

    def press(self, event):
        self.scan_mark_pos = (event.x, event.y)
        self.draw.scan_mark(event.x, event.y)

    def release(self, event):
        self.draw_pos.x += event.x - self.scan_mark_pos[0]
        self.draw_pos.y += event.y - self.scan_mark_pos[1]

    def winrelease(self, event):
        if platform == "mobile":
            self.zoom.set(0)
        self.scalepos = 0

    def scalezoom(self, pos):
        pos = int(pos)
        if pos == 0 or self.scalepos == pos:
            return
        factor = (pos-self.scalepos)*zoomScale/100 + 1
        self.scalepos = pos
        self.do_zoom(factor, Coord(int(self.draw_w/2), int(self.draw_h/2)))

    def scrollzoom(self, event):
        factor = 1.001 ** event.delta
        self.do_zoom(factor, Coord(event.x, event.y))

    def do_zoom(self, factor, pos: Coord):
        self.resolution *= factor
        self.draw.scale("all",
                        pos.x - self.draw_pos.x,
                        pos.y - self.draw_pos.y,
                        factor, factor)
        for text in self.texts:
            textSize = self.resolution * text['r'] * txtScale
            textSize = int(textSize ** txtShrink)
            self.draw.itemconfig(text['obj'], font=('Consolas', textSize))
            if text['r'] * self.resolution < self.txtshowres:
                self.draw.itemconfig(text['obj'], fill="")
            else:
                self.draw.itemconfig(text['obj'], fill=self.theme.fg)


if __name__ == "__main__":
    mindmap_txt = extract_mindmap(r'C:\Users\Admin\prog\bencode\in_progress\python\mindmap\pres_tool\\'+projectName + ".md")
    run_map(mindmap_txt, projectName)
