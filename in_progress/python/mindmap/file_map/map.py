#!/usr/bin/python
# -*- coding: utf-8 -*-

from bisect import insort_right
import tkinter as tk
from tkinter import font
from mdMapTools import extract_mindmap
from dataclasses import dataclass, field
from math import cos, pi, sin
from typing import Callable, Optional
import re
import ctypes
 
ctypes.windll.shcore.SetProcessDpiAwareness(1)

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
SHOW_PERCENTAGE = True


def run_map(mindmap_text=None):
    if mindmap_text is None:
        mindmap_text = extract_mindmap(MAP_PATH)

    # ~~~~~~~~~~~~~~~~~~~~~~~~
    node = convert_to_map(mindmap_text)
    # ~~~~~~~~~~~~~~~~~~~~~~~~
    theme = DARK_THEME  # DARK_THEME / LIGHT_THEME
    progressStyle = ProgressStyle(theme, "sector")  # "sector" / "arc"
    # ~~~~~~~~~~~~~~~~~~~~~~~~
    MindMap(node, theme, progressStyle).start()


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
            self.arcWidth = 5
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
class Node:
    text: str
    progress: float
    parent: Optional["Node"]
    children: list["Node"]
    params: dict = field(default_factory=dict)
    textparams: dict = field(default_factory=dict)

    def __getitem__(self, key):
        return self.params[key]


def convert_to_map(string: str) -> Node:
    nodes = string.strip().split('\n')
    prev_intend = -1
    start = None
    cur_node = None
    for i, node in enumerate(nodes):
        node_match = match_text(node)
        if node_match is None:
            raise RuntimeError(
                f"\n\nThe following line doesn't match:"
                + '\n' + '-' * len(node)
                + f'\n{node}'
                + '\n' + '-' * len(node)
                + '\nStructure is: [intendation][content];[percentage]'
                '\nExamples:\n    nice shorts;65\nor'
                '\n            right?\nor'
                '\n        Hey there! ;   89')
        intendation, new_node = node_match
        if intendation == 0 and i != 0:
            raise RuntimeError(
                f'\n\n"{node}" has intendation 0, but there can only be one '
                'top-level node: the title!')
        elif intendation > prev_intend + 1:
            raise RuntimeError(
                f'\n\nToo high intendation ({intendation}) on text "{node}"!')
        elif intendation == prev_intend + 1:
            new_node.parent = cur_node
            if intendation == 0 and i == 0:
                start = new_node  # HERE DOES THE MAGIC HAPPEN. I know I know
        elif intendation == prev_intend:
            new_node.parent = cur_node.parent
        else:
            back = prev_intend - intendation
            while back > 0:
                if cur_node.parent is None:
                    raise RuntimeError(
                        "You mustn't use negative intendations!")
                cur_node = cur_node.parent
                back -= 1
            new_node.parent = cur_node.parent
        if new_node.parent is None and i != 0:
            raise RuntimeError("You mustn't use negative intendations!")
        cur_node = new_node
        if i != 0:
            new_node.parent.children.append(cur_node)
        prev_intend = intendation
    return start


def match_text(text: str) -> Optional[tuple[int, Node]]:
    m = re.fullmatch(r'(\s*)([^;]+);?\s*(\d*)', text)
    if not m:
        return None
    intend, name, percent = m.groups()
    return (intend.count('\t') + intend.count(TAB_AS_SPACES),
            Node(name, zero_int(percent), None, []))


def zero_int(text):
    return 0 if text == "" else int(text)


##############################################################################


@dataclass
class Coord:
    x: int
    y: int

    def __iter__(self):
        return iter((self.x, self.y))
        
    def __sub__(self, other: "Coord"):
        return Coord(self.x - other.x, self.y - other.y)
        
    def __add__(self, other: "Coord"):
        return Coord(self.x + other.x, self.y + other.y)
    
    def __mul__(self, amount: float):
        return Coord(self.x * amount, self.y * amount)
    
    def stretch_to(self, pos: "Coord", amount: float):
        return self + (pos - self) * amount


class MindMap:
    def __init__(
            self, node: Node,
            theme: Theme, pr_style: ProgressStyle,
            font_style: str=FONT_STYLE):
        self.map = node
        self.theme = theme
        self.pr_style = pr_style
        self.font_style = font_style
        self.init_window()
        self.init_win_bindings()
        self.init_attributes()
        self.init_draw()
        if PLATFORM == "mobile":
            self.init_zoom()

    # -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
    def init_window(self):
        self.win = tk.Tk()
        self.win["bg"] = self.theme.bg
        self.win.bind("<ButtonRelease-1>", self.reset_zoom_scale)
        self.w = float(self.win.winfo_screenwidth())
        self.h = float(self.win.winfo_screenheight())
        self.draw_w, self.draw_h = self.w, self.h
        if PLATFORM == "mobile":
            self.draw_h *= 0.85

    def reset_zoom_scale(self, _):
        if PLATFORM == "mobile":
            self.zoom.set(0)
        self.scalepos = 0

    # -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
    def init_win_bindings(self):
        self.win.bind("<Key>", self.handle_key)

    def handle_key(self, key: tk.Event):
        len_children = len(self.focused.children)
        match key.keysym:
            case 'Down' if len_children != 0:
                self.focused = self.focused.children[self.selected[self.layer]]
                self.zoom_to_focused()
                self.layer += 1
            case 'Up' if self.focused.parent is not None:
                self.focused = self.focused.parent
                self.zoom_to_focused(reverse=True)
                self.layer -= 1
            case 'Left' if len_children != 0:
                self.selected[self.layer] -= 1
                self.correct_selected_with(len_children)
            case 'Right' if len_children != 0:
                self.selected[self.layer] += 1
                self.correct_selected_with(len_children)
            case 'f' | 'F':
                self.toggle_fullscreen()
            case 't':
                self.change_font('forwards')
            case 'T':
                self.change_font('backwards')
            case _:
                self.key_command(key, self.focused, self.selected[self.layer])
                return
        self.reset_position()
        self.draw.delete('all')
        self.draw_map(self.focused, rotation=self.focused.params['rotation'])#self.get_ideal_rotation())
        self.create_font_label()

    def zoom_to_focused(self, reverse=False):
        iterations = 20
        stretched_pos = self.focused.params['coord'].stretch_to(
            Coord(self.draw_w/2, self.draw_h/2), -0.25)  # TODO: magic number
        for i in range(iterations):
            rate = pow(1.175, 1-abs(iterations/2-i)/iterations*2)  # TODO: magic number
            self.do_zoom(1/rate if reverse else rate, stretched_pos)
            self.win.update()

    def correct_selected_with(self, len_children):
        self.selected[self.layer] %= len_children
        self.selected[self.layer + 1:] = (
            [0] * (self.depth - self.layer - 1) )

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
        
    def create_font_label(self):
        self.font_label = self.draw.create_text(
            *self.font_label_pos,
            text=self.font_style,
            anchor=tk.NW,
            fill=self.theme.fg,
            font=(self.font_style, self.font_label_size)
        )
        
    def toggle_fullscreen(self):
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

    # -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
    def init_attributes(self):
        self.draw_pos = Coord(0, 0)
        # self.texts: list[dict[str, int]] = []
        self.resolution = 1
        self.scalepos = 0
        self.START_RADIUS = self.draw_w / 8
        self.txtshowres = (self.draw_w+self.draw_h)/70
        self.focused = self.map
        self.depth = self.get_depth()
        self.selected = [0 for _ in range(self.depth)]
        self.layer = 0
        self.fullscreen = False
        self.font_index = -1
        self.font_label_size = 15
        self.font_label_pos = Coord(10, 10)
        self.key_command = lambda a, b, c: None

    def get_depth(self, map=None):
        if map is None:
            map = self.map
        if len(map.children) == 0:
            return 0
        return 1 + sum(self.get_depth(child) for child in map.children)

    # -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
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
        self.draw.bind("<MouseWheel>", self.scrollzoom)

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

    def scrollzoom(self, event):
        factor = 1.001 ** event.delta
        event_pos = Coord(event.x, event.y)
        self.do_zoom(factor, event_pos)

    def do_zoom(self, factor, pos: Coord):
        self.resolution *= factor
        self.draw.scale("all", *(pos - self.draw_pos), factor, factor)
        self.configure_text(self.focused)
        new_label_pos = self.font_label_pos - self.draw_pos
        self.draw.moveto(self.font_label, *new_label_pos)
            
    def configure_text(self, node: Node, stop=False):
        text = node.textparams
        textSize = self.resolution * text['r'] * TXT_SCALE
        textSize = int(textSize ** TXT_SHRINK)
        self.draw.itemconfig(text['obj'], font=(self.font_style, textSize))
        if text['r'] * self.resolution < self.txtshowres:
            self.draw.itemconfig(text['obj'], fill="")
        else:
            self.draw.itemconfig(text['obj'], fill=self.theme.fg)
        if stop: return
        for child in node.children:
            self.configure_text(child, stop=True)

    # -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
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

    # ====================================================================== #
    def start(self):
        self.draw_map(self.map, recalc_progress=True)
        self.create_font_label()
        tk.mainloop()
    # ====================================================================== #

    def draw_map(
            self, node: Node, pos=None, radius=None,
            rotation: float=0.75, recalc_progress: bool=False
            ) -> float:
        if pos is None:
            pos = Coord(self.draw_w/2, self.draw_h/2)
        if radius is None:
            radius = self.START_RADIUS

        worth_drawing = (node is self.focused or
            node in self.focused.children or
            any(node in child.children for child in self.focused.children))
        
        # initializing node params: position, rotation
        node.params['coord'] = pos
        node.params['rotation'] = rotation

        child_num = len(node.children)
        plus_rot = (child_num % 2 == 0 and node.parent is not None)
        progress = 0
        for i in range(child_num):
            new_rotation = (i / child_num + rotation
                            + (0.5/child_num if plus_rot else 0))
            if worth_drawing:
                self.draw.create_line(
                    self.line_rotate(pos, radius, radius*CONN_LEN, new_rotation),
                    fill=self.theme.bd
                )
            rotated_new_pos = self.circle_coord(
                pos, radius*CONN_LEN + radius*RAD_SCALE, new_rotation
            )
            if recalc_progress and node.progress > 0:
                node.children[i].progress = node.progress

            progress += self.draw_map(  # RECURSION HERE
                node.children[i],
                pos=rotated_new_pos,
                radius=radius*RAD_SCALE,
                rotation=new_rotation,
                recalc_progress=recalc_progress
            )

        if recalc_progress and child_num != 0:
            avg_progress = progress / child_num
            node.progress = avg_progress

        if node.progress < 1:
            node.progress = 0

        if worth_drawing:
            self.draw_node(node, pos, radius)
            node.textparams = self.draw_text(node, pos, radius)
        
        return node.progress

    def line_rotate(self, pos: Coord, start, end, rotation):
        return (
            *self.circle_coord(pos, start, rotation),
            *self.circle_coord(pos, end, rotation))

    def circle_coord(self, pos: Coord, radius, rotation) -> Coord:
        rotation *= 2*pi
        return Coord(pos.x + cos(rotation)*radius, pos.y + sin(rotation)*radius)

    def draw_node(self, node: Node, pos: Coord, r: float):
        self.draw.create_oval(
            self.oval_coords(pos, r),
            outline=self.theme.bd,
            fill=self.circle_fill(node))
        self.draw.create_arc(
            self.oval_coords(pos, r),
            extent=node.progress/100*359.999,
            style=self.pr_style.style,
            outline=self.arc_outline(node.progress),
            fill=self.arc_fill(node.progress),
            width=self.pr_style.arcWidth)

    def oval_coords(self, pos: Coord, r):  # r ~ radius
        return (pos.x - r, pos.y - r, pos.x + r, pos.y + r)

    def draw_text(self, node: Node, pos: Coord, r) -> dict[str, int]:
        node_txt = node.text + (f"\n{round(node.progress)} %"
                                  if SHOW_PERCENTAGE else "")
        textSize = self.resolution * r * TXT_SCALE
        textSize = int(textSize ** TXT_SHRINK)
        return {'r': r, 'obj': self.draw.create_text(
            pos.x, pos.y, text=node_txt,
            fill=(
                self.theme.focus if node is self.focused or
                node in self.focused.children and
                node.parent is not None and
                node.parent.children.index(node) == self.selected[self.layer]
                else self.theme.fg if r >= self.txtshowres else ""),
            font=(self.font_style, textSize),
            justify="center"
        )}

    def circle_fill(self, node: Node):
        return (self.theme.pr
                if self.pr_style.mode == "sector" and node.progress == 100
                else '#202090'
                if node.params.get('isfile', False)
                else self.theme.bg)

    def arc_fill(self, progress):
        return (""
                if self.pr_style.mode == "sector" and progress == 100
                else self.pr_style.arcFill)

    def arc_outline(self, progress):
        return (""
                if self.pr_style.mode == "sector" and not 0 < progress < 100
                else self.pr_style.arcOutline)

    def set_key_command(self, command: Callable[[str, Node], None]):
        self.key_command = command


if __name__ == "__main__":
    run_map()
