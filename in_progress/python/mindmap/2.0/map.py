#!/usr/bin/python
# -*- coding: utf-8 -*-

from bisect import insort_right
import tkinter as tk
from tkinter import font
from mdMapTools import extract_mindmap
from dataclasses import dataclass
from math import cos, pi, sin
from typing import Callable, Optional
import re

##############################################################################
# ---------------------------------Parameters------------------------------- #
##############################################################################

MAP_PATH = r"C:\Users\b.hargitai\Documents\Programme\MindMap\onedrive_folder_tree.md"

PLATFORM = "desktop"  # "mobile" / "desktop"
FONT_STYLE = 'Segoe UI'
CONN_LEN = 1.5
RAD_SCALE = 0.2
TXT_SCALE = 15
TXT_SHRINK = 0.4
ZOOMSCALE = 2
TAB_AS_SPACES = ' '*4
SHOW_PERCENTAGE = False


def run_map(mindmap_text=None):
    if mindmap_text is None:
        mindmap_text = extract_mindmap(MAP_PATH)

    # ~~~~~~~~~~~~~~~~~~~~~~~~
    block = convert_to_map(mindmap_text)
    # ~~~~~~~~~~~~~~~~~~~~~~~~
    theme = DARK_THEME  # DARK_THEME / LIGHT_THEME
    progressStyle = ProgressStyle(theme, "sector")  # "sector" / "arc"
    # ~~~~~~~~~~~~~~~~~~~~~~~~
    MindMap(block, theme, progressStyle).start()


class Theme:
    bg: str  # background
    altbg: str  # alternative background
    fg: str  # foreground
    bd: str  # border
    pr: str  # progress
    focus: str  # focused color

    def __init__(self, properties: dict):
        assert (set(properties.keys()) ==
                {'bg', 'altbg', 'fg', 'bd', 'pr', 'focus'}),\
                "False attributes for Theme object!"
        self.__dict__ = properties


DARK_THEME = Theme({
    "bg": "#101045",
    "altbg": "#88AAAA",
    "fg": "white",
    "bd": "gray",
    "pr": "green",
    "focus": "yellow"
})

LIGHT_THEME = Theme({
    "bg": "white",
    "altbg": "lightgrey",
    "fg": "black",
    "bd": "grey",
    "pr": "lightgreen",
    "focus": "#ff4444"
})

##############################################################################
##############################################################################
##############################################################################


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


def convert_to_map(string: str) -> Block:
    blocks = string.strip().split('\n')
    prev_intend = -1
    start = None
    cur_block = None
    for i, block in enumerate(blocks):
        block_match = match_text(block)
        if block_match is None:
            raise RuntimeError(
                f"\n\nThe following line doesn't match:"
                + '\n' + '-' * len(block)
                + f'\n{block}'
                + '\n' + '-' * len(block)
                + '\nStructure is: [intendation][content];[percentage]'
                '\nExamples:\n    nice shorts;65\nor'
                '\n            right?\nor'
                '\n        Hey there! ;   89')
        intendation, new_block = block_match
        if intendation == 0 and i != 0:
            raise RuntimeError(
                f'\n\n"{block}" has intendation 0, but there can only be one '
                'top-level node: the title!')
        elif intendation > prev_intend + 1:
            raise RuntimeError(
                f'\n\nToo high intendation ({intendation}) on text "{block}"!')
        elif intendation == prev_intend + 1:
            new_block.parent = cur_block
            if intendation == 0 and i == 0:
                start = new_block  # HERE DOES THE MAGIC HAPPEN. I know I know
        elif intendation == prev_intend:
            new_block.parent = cur_block.parent
        else:
            back = prev_intend - intendation
            while back > 0:
                if cur_block.parent is None:
                    raise RuntimeError(
                        "You mustn't use negative intendations!")
                cur_block = cur_block.parent
                back -= 1
            new_block.parent = cur_block.parent
        if new_block.parent is None and i != 0:
            raise RuntimeError("You mustn't use negative intendations!")
        cur_block = new_block
        if i != 0:
            new_block.parent.children.append(cur_block)
        prev_intend = intendation
    return start


def match_text(text: str) -> Optional[tuple[int, Block]]:
    m = re.fullmatch(r'(\s*)([^;]+);?\s*(\d*)', text)
    if not m:
        return None
    intend, name, percent = m.groups()
    return (intend.count('\t') + intend.count(TAB_AS_SPACES),
            Block(name, zero_int(percent), None, []))


def zero_int(text):
    return 0 if text == "" else int(text)


##############################################################################


@dataclass
class Coord:
    x: int
    y: int

    def __iter__(self):
        return iter((self.x, self.y))
        
    def __sub__(self, other):
        return Coord(self.x - other.x, self.y - other.y)
        
    def __add__(self, other):
        return Coord(self.x + other.x, self.y + other.y)


class MindMap:
    def __init__(
            self, block: Block,
            theme: Theme, prStyle: ProgressStyle,
            font_style: str=FONT_STYLE):
        self.map = block
        self.theme = theme
        self.prStyle = prStyle
        self.font_style = font_style
        self.initWindow()
        self.init_attributes()
        self.init_draw()
        if PLATFORM == "mobile":
            self.init_zoom()

    def initWindow(self):
        self.win = tk.Tk()
        self.win["bg"] = self.theme.bg
        self.win.bind("<ButtonRelease-1>", self.reset_zoom_scale)
        self.w = float(self.win.winfo_screenwidth())
        self.h = float(self.win.winfo_screenheight())
        self.draw_w, self.draw_h = self.w, self.h
        if PLATFORM == "mobile":
            self.draw_h *= 0.85
        

    def reset_zoom_scale(self, event):
        if PLATFORM == "mobile":
            self.zoom.set(0)
        self.scalepos = 0

    def init_attributes(self):
        self.draw_pos = Coord(0, 0)
        self.texts: list[dict[str, int]] = []
        self.resolution = 1
        self.scalepos = 0
        self.start_radius = self.draw_w/8
        self.txtshowres = (self.draw_w+self.draw_h)/70
        self.focused = self.map
        self.selected = [0 for _ in range(self.get_depth())]
        self.depth = 0
        self.fullscreen = False
        self.font_index = -1
        self.font_label_size = 15
        self.font_label_pos = Coord(10, 10)

    def get_depth(self, map=None):
        if map is None:
            map = self.map
        if len(map.children) == 0:
            return 0
        return 1 + sum(self.get_depth(child) for child in map.children)

    def init_draw(self):
        self.draw = tk.Canvas(
            self.win,
            width=self.draw_w,
            height=self.draw_h,
            background=self.theme.bg,
            highlightthickness=0
        )
        self.draw.pack()
        self.draw.bind('<ButtonPress-1>', self.press)
        self.draw.bind("<ButtonRelease-1>", self.release)
        self.draw.bind("<B1-Motion>", self.motion)
        for key in ["<Left>", "<Right>", "<Up>", "<Down>"]:
            self.win.bind(key, self.get_key_handler(key))
        for f_key in ["<f>", "<F>"]:
            self.win.bind(f_key, self.toggle_fullscreen)
        self.win.bind("<t>", lambda _: self.change_font('forwards'))
        self.win.bind("<T>", lambda _: self.change_font('backwards'))
        self.draw.bind("<MouseWheel>", self.scrollzoom)
        
    def create_font_label(self):
        self.font_label = self.draw.create_text(
            *self.font_label_pos,
            text=self.font_style,
            anchor=tk.NW,
            fill=self.theme.fg,
            font=(self.font_style, self.font_label_size)
        )

    def press(self, event):
        self.scan_mark_pos = Coord(event.x, event.y)
        self.draw.scan_mark(event.x, event.y)

    def release(self, event):
        self.draw_pos.x += event.x - self.scan_mark_pos.x
        self.draw_pos.y += event.y - self.scan_mark_pos.y
        new_label_pos = self.font_label_pos - self.draw_pos
        self.draw.moveto(self.font_label, *new_label_pos)
        self.draw.itemconfig(self.font_label, fill=self.theme.fg)

    def motion(self, event):
        self.draw.scan_dragto(event.x, event.y, gain=1)
        self.draw.itemconfig(self.font_label, fill="")

    def get_key_handler(self, key) -> Callable:
        return lambda event, key=key: self.handle_key(key)

    def handle_key(self, key):
        len_children = len(self.focused.children)
        match key:
            case "<Down>" if len_children != 0:
                self.focused = self.focused.children[self.selected[self.depth]]
                self.depth += 1
            case "<Up>" if self.focused.parent is not None:
                self.focused = self.focused.parent
                self.selected[self.depth] = 0
                self.depth -= 1
            case "<Left>" if len_children != 0:
                self.selected[self.depth] -= 1
                self.selected[self.depth] %= len_children
            case "<Right>" if len_children != 0:
                self.selected[self.depth] += 1
                self.selected[self.depth] %= len_children
            case _: return

        self.reset_position()
        self.draw.delete('all')
        self.draw_map(self.focused, rotation=self.get_ideal_rotation())
        self.create_font_label()

    def reset_position(self):
        self.draw.scan_mark(*self.draw_pos)
        self.draw.scan_dragto(0, 0, gain=1)
        self.draw_pos = Coord(0, 0)
        self.resolution = 1

    def get_ideal_rotation(self) -> float:
        rotation = (-1/4 if len(self.focused.children) == 2 else
                    -1/2 if self.focused.text == "Der Vogel" else 0)
        correction = 0.75
        return rotation + correction

    def is_power_of_2(self, n) -> bool:
        return n & (n-1) == 0
        
    def toggle_fullscreen(self, _):
        self.fullscreen = not self.fullscreen
        self.win.attributes("-fullscreen", self.fullscreen)
        
    def change_font(self, direction: str):
        
        match direction:
            case 'forwards' if self.font_index < len(font.families()) - 1:
                self.font_index += 1
            case 'backwards' if self.font_index > 0:
                self.font_index -= 1
            case _:
                return
        self.font_style = font.families()[self.font_index]
        self.draw.itemconfig(
            self.font_label, text=self.font_style,
            font=(self.font_style, self.font_label_size))
        self.configure_text()

    def scrollzoom(self, event):
        factor = 1.001 ** event.delta
        event_pos = Coord(event.x, event.y)
        self.do_zoom(factor, event_pos)

    def do_zoom(self, factor, pos: Coord):
        self.resolution *= factor
        self.draw.scale("all", *(pos - self.draw_pos), factor, factor)
        self.configure_text()
        new_label_pos = self.font_label_pos - self.draw_pos
        self.draw.moveto(self.font_label, *new_label_pos)
            
    def configure_text(self):
        for text in self.texts:
            textSize = self.resolution * text['r'] * TXT_SCALE
            textSize = int(textSize ** TXT_SHRINK)
            self.draw.itemconfig(text['obj'], font=(self.font_style, textSize))
            if text['r'] * self.resolution < self.txtshowres:
                self.draw.itemconfig(text['obj'], fill="")
            else:
                self.draw.itemconfig(text['obj'], fill=self.theme.fg)

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

    def scalezoom(self, pos):
        pos = int(pos)
        if pos == 0 or self.scalepos == pos:
            return
        factor = (pos-self.scalepos)*ZOOMSCALE/100 + 1
        self.scalepos = pos
        self.do_zoom(factor, Coord(int(self.draw_w/2), int(self.draw_h/2)))

    def start(self):
        self.draw_map(self.map, recalc_progress=True)
        self.create_font_label()
        tk.mainloop()

    def draw_map(
            self, block: Block, pos=None, radius=None,
            rotation: float=0.75, recalc_progress: bool=False
            ) -> float:
        if pos is None:
            pos = Coord(self.draw_w/2, self.draw_h/2)
        if radius is None:
            radius = self.start_radius

        child_num = len(block.children)
        plus_rot = (child_num % 2 == 0 and block.parent is not None)
        progress = 0
        for i in range(child_num):
            new_rotation = (i / child_num + rotation
                            + (0.5/child_num if plus_rot else 0))
            self.draw.create_line(
                self.line_rotate(pos, radius, radius*CONN_LEN, new_rotation),
                fill=self.theme.bd
            )
            rotated_new_pos = self.circle_coord(
                pos, radius*CONN_LEN + radius*RAD_SCALE, new_rotation
            )
            if recalc_progress and block.progress > 0:
                block.children[i].progress = block.progress

            progress += self.draw_map(  # RECURSION HERE
                block.children[i],
                pos=rotated_new_pos,
                radius=radius*RAD_SCALE,
                rotation=new_rotation,
                recalc_progress=recalc_progress
            )

        if recalc_progress and child_num != 0:
            avg_progress = progress / child_num
            block.progress = avg_progress

        if block.progress < 1:
            block.progress = 0

        self.draw_block(block, pos, radius)
        self.draw_text(block, pos, radius)
        return block.progress

    def line_rotate(self, pos: Coord, start, end, rotation):
        return (
            *self.circle_coord(pos, start, rotation),
            *self.circle_coord(pos, end, rotation))

    def circle_coord(self, pos: Coord, radius, rotation) -> Coord:
        rotation *= 2*pi
        return Coord(pos.x + cos(rotation)*radius, pos.y + sin(rotation)*radius)

    def draw_block(self, block: Block, pos: Coord, r: float):
        self.draw.create_oval(
            self.oval_coords(pos, r),
            outline=self.theme.bd,
            fill=self.circle_fill(block.progress))
        self.draw.create_arc(
            self.oval_coords(pos, r),
            extent=block.progress/100*359.999,
            style=self.prStyle.style,
            outline=self.arc_outline(block.progress),
            fill=self.arc_fill(block.progress),
            width=self.prStyle.arcWidth)

    def oval_coords(self, pos: Coord, r):  # r ~ radius
        return (pos.x-r, pos.y-r, pos.x+r, pos.y+r)

    def draw_text(self, block: Block, pos: Coord, r):
        block_txt = block.text + (f"\n{round(block.progress)} %"
                                  if SHOW_PERCENTAGE else "")
        textSize = self.resolution * r * TXT_SCALE
        textSize = int(textSize ** TXT_SHRINK)
        self.texts += [{'r': r, 'obj': self.draw.create_text(
            pos.x, pos.y, text=block_txt,
            fill=(
                self.theme.focus if block is self.focused or
                block in self.focused.children and
                block.parent is not None and
                block.parent.children.index(block) == self.selected[self.depth]
                else self.theme.fg if r >= self.txtshowres else ""),
            font=(self.font_style, textSize),
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


if __name__ == "__main__":
    run_map()
