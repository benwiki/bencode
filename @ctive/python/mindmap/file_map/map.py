#!/usr/bin/python
# -*- coding: utf-8 -*-

import ctypes
import re
import tkinter as tk
from dataclasses import dataclass, field
from math import cos, pi, sin
from tkinter import font
from typing import Callable, Iterator, Optional

from mdMapTools import extract_mindmap

# Activate DPI awareness for better GUI rendering on Windows.
ctypes.windll.shcore.SetProcessDpiAwareness(1)

##############################################################################
# ------------------------------ PARAMETERS -------------------------------- #
# Feel free to change these parameters to your liking.                       #
# -------------------------------------------------------------------------- #

MAP_PATH = (
    r"C:\Users\b.hargitai\prog\bencode\@ctive\python\mindmap"
    r"\file_map\onedrive_folder_tree.md"
)

PLATFORM = "desktop"  # "mobile" / "desktop"
FONT_STYLE = "Segoe UI"
CONN_LEN = 1.5
RAD_SCALE = 0.2
TXT_SCALE = 15
TXT_SHRINK = 0.4
ZOOMSCALE = 2
TAB_AS_SPACES = " " * 4
SHOW_PERCENTAGE = True

##############################################################################


def run_map(mindmap_text=None):
    """Starts the MindMap."""
    if mindmap_text is None:
        mindmap_text = extract_mindmap(MAP_PATH)

    # ~~~~~~~~~~~~~~~~~~~~~~~~
    node = MindMapParser(mindmap_text).get_map()
    # ~~~~~~~~~~~~~~~~~~~~~~~~
    theme = THEMES["DARK"]
    progress_style = ProgressStyle(theme, "sector")  # "sector" / "arc"
    # ~~~~~~~~~~~~~~~~~~~~~~~~
    MindMap(node, theme, progress_style).start()


@dataclass
class Theme:
    """Defines the appearance of the MindMap."""

    bg: str  # background
    bg2: str  # alternative background
    fg: str  # foreground
    bd: str  # border
    pr: str  # progress
    focus: str  # focused color


THEMES = {
    "DARK": Theme(
        bg="#101045",
        bg2="#88AAAA",
        fg="white",
        bd="gray",
        pr="green",
        focus="yellow",
    ),
    "LIGHT": Theme(
        bg="white",
        bg2="lightgrey",
        fg="black",
        bd="grey",
        pr="lightgreen",
        focus="#ff4444",
    ),
}

##############################################################################
##############################################################################
##############################################################################


class ProgressStyle:
    def __init__(self, theme: Theme, mode: str):
        if mode == "arc":
            self.arc_outline = theme.pr
            self.arc_fill = ""
            self.arc_width = 5
            self.style = "arc"
        elif mode == "sector":
            self.arc_outline = theme.bd
            self.arc_fill = theme.pr
            self.arc_width = 1
            self.style = ""
        else:
            raise ValueError("ProgressStyle mode " + f'"{mode}" incompatible!')
        self.mode = mode


@dataclass
class Coord:
    x: float
    y: float

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


@dataclass
class Node:
    text: str
    progress: float = 0.0
    parent: Optional["Node"] = None
    children: list["Node"] = field(default_factory=list)
    indent: int = 0
    params: dict = field(default_factory=dict)
    coord: Optional[Coord] = None
    rotation: Optional[float] = None
    textparams: dict = field(default_factory=dict)

    def __getitem__(self, key):
        return self.params[key]


class MindMapParser:
    def __init__(self, raw_text: str, tab_as_spaces: str = TAB_AS_SPACES):
        self.raw_text = raw_text
        self.tab_as_spaces = tab_as_spaces
        self.line_regex = re.compile(r"(\s*)([^;]+);?\s*(\d*)")

    def get_map(self) -> Node:
        """Converts the raw text to a structured mind map tree."""
        parsed_nodes = self._text_to_nodes()
        return self._tree_from_nodes(parsed_nodes)

    def _text_to_nodes(self) -> Iterator[Node]:
        """Parse the raw text into a list of nodes with their indentation levels."""
        lines = self.raw_text.strip().split("\n")
        return (self._line_to_node(line) for line in lines)

    def _tree_from_nodes(self, parsed_nodes: Iterator[Node]):
        """Builds the tree structure from the parsed nodes."""
        root = next(parsed_nodes)
        stack: list[Node] = [root]

        for node in parsed_nodes:
            while stack and node.indent <= stack[-1].indent:
                stack.pop()

            if stack and node.indent == (stack[-1].indent + 1):
                node.parent = stack[-1]
                stack[-1].children.append(node)

            elif stack and node.indent > (stack[-1].indent + 1):
                raise ValueError(
                    f"{node.indent} is too high indentation level for node: "
                    f"{node.text}. Should be {stack[-1].indent + 1} or lower."
                )

            stack.append(node)

        return root

    def _line_to_node(self, line: str) -> Node:
        """Match the text to a regex and return the indentation level and the node."""
        match = self.line_regex.fullmatch(line)
        if not match:
            raise ValueError(f"Invalid node text: {line}")
        indent, name, percent = match.groups()

        indent_count = indent.count("\t") + indent.count(self.tab_as_spaces)
        return Node(name, self._zero_int(percent), None, [], indent=indent_count)

    def _zero_int(self, text: str) -> int:
        """Convert a string to int, or return 0 if it's empty."""
        return 0 if text == "" else int(text)


##############################################################################


class MindMap:
    def __init__(
        self,
        node: Node,
        theme: Theme,
        pr_style: ProgressStyle,
        font_style: str = FONT_STYLE,
    ) -> None:
        self.map = node
        self.theme = theme
        self.pr_style = pr_style
        self.font_style = font_style

        self.init_window()
        self.init_win_bindings()

        self.draw_pos = Coord(0, 0)
        self.resolution = 1
        self.scalepos = 0
        self.start_radius = self.draw_w / 8
        self.txtshowres = (self.draw_w + self.draw_h) / 70
        self.focused = self.map
        self.depth = self.get_depth()
        self.selected = [0 for _ in range(self.depth)]
        self.layer = 0
        self.fullscreen = False
        self.font_index = -1
        self.font_label_size = 15
        self.font_label_pos = Coord(10, 10)
        self.key_command = lambda a, b, c: None
        self.font_label = -1
        self.scan_mark_pos = Coord(-1, -1)

        self.init_draw()
        if PLATFORM == "mobile":
            self.init_zoom()

    def get_depth(self, mind_map=None) -> int:
        if mind_map is None:
            mind_map = self.map
        if not mind_map.children:
            return 0
        return 1 + sum(self.get_depth(child) for child in mind_map.children)

    def get_distance(self, node: Node, root: Node | None = None) -> int:
        """Returns the distance between the root and the node.
        root has to be an ancestor of node."""
        if root is None:
            root = self.map
        if node is root or node.parent is None:
            return 0
        return 1 + self.get_distance(node.parent, root)

    # -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
    def init_window(self) -> None:
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
    def init_win_bindings(self) -> None:
        self.win.bind("<Key>", self.handle_key)
        self.win.protocol("WM_DELETE_WINDOW", quit)

    def handle_key(self, key: tk.Event) -> None:
        len_children = len(self.focused.children)
        match key.keysym:
            case "Down" if len_children != 0:
                self.focused = self.focused.children[self.selected[self.layer]]
                self.zoom_to_focused()
                self.layer += 1
            case "Up" if self.focused.parent is not None:
                self.focused = self.focused.parent
                self.zoom_to_focused(reverse=True)
                self.layer -= 1
            case "Left" if len_children != 0:
                self.selected[self.layer] -= 1
                self.correct_selected_with(len_children)
            case "Right" if len_children != 0:
                self.selected[self.layer] += 1
                self.correct_selected_with(len_children)
            case "f" | "F":
                self.toggle_fullscreen()
            case "t":
                self.change_font("forwards")
            case "T":
                self.change_font("backwards")
            case _:
                self.key_command(key, self.focused, self.selected[self.layer])
                return
        self.reset_position()
        self.draw.delete("all")
        self.draw_map(
            self.focused, rotation=self.focused.params["rotation"]
        )  # self.get_ideal_rotation())
        self.create_font_label()

    def zoom_to_focused(self, reverse=False) -> None:
        iterations = 20
        stretched_pos = self.focused.params["coord"].stretch_to(
            Coord(self.draw_w / 2, self.draw_h / 2), -0.25
        )  # TODO: magic number
        for i in range(iterations):
            rate = pow(
                1.175, 1 - abs(iterations / 2 - i) / iterations * 2
            )  # TODO: magic number
            self.do_zoom(1 / rate if reverse else rate, stretched_pos)
            self.win.update()

    def correct_selected_with(self, len_children) -> None:
        self.selected[self.layer] %= len_children
        self.selected[self.layer + 1 :] = [0] * (self.depth - self.layer - 1)

    def reset_position(self) -> None:
        self.draw.scan_mark(*self.draw_pos)
        self.draw.scan_dragto(0, 0, gain=1)
        self.draw_pos = Coord(0, 0)
        self.resolution = 1

    def get_ideal_rotation(self) -> float:
        rotation = (
            -1 / 4
            if len(self.focused.children) == 2
            else -1 / 2 if self.focused.text == "Der Vogel" else 0
        )
        correction = 0.75
        return rotation + correction

    def create_font_label(self) -> None:
        self.font_label = self.draw.create_text(
            *self.font_label_pos,
            text=self.font_style,
            anchor=tk.NW,
            fill=self.theme.fg,
            font=(self.font_style, self.font_label_size),
        )

    def toggle_fullscreen(self) -> None:
        self.fullscreen = not self.fullscreen
        self.win.attributes("-fullscreen", self.fullscreen)

    def change_font(self, direction: str) -> None:
        match direction:
            case "forwards" if self.font_index < len(font.families()) - 1:
                self.font_index += 1
            case "backwards" if self.font_index > 0:
                self.font_index -= 1
            case _:
                return
        self.font_style = font.families()[self.font_index]
        self.draw.itemconfig(
            self.font_label,
            text=self.font_style,
            font=(self.font_style, self.font_label_size),
        )
        self.configure_text(self.map)

    # -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
    def init_draw(self) -> None:
        self.draw = tk.Canvas(
            self.win,
            width=self.draw_w,
            height=self.draw_h,
            background=self.theme.bg,
            highlightthickness=0,
        )
        self.draw.pack()
        self.draw.bind("<ButtonPress-1>", self.press)
        self.draw.bind("<ButtonRelease-1>", self.release)
        self.draw.bind("<B1-Motion>", self.motion)
        self.draw.bind("<MouseWheel>", self.scrollzoom)

    def press(self, event) -> None:
        self.scan_mark_pos = Coord(event.x, event.y)
        self.draw.scan_mark(event.x, event.y)

    def release(self, event) -> None:
        self.draw_pos.x += event.x - self.scan_mark_pos.x
        self.draw_pos.y += event.y - self.scan_mark_pos.y
        new_label_pos = self.font_label_pos - self.draw_pos
        self.draw.moveto(self.font_label, *new_label_pos)
        self.draw.itemconfig(self.font_label, fill=self.theme.fg)

    def motion(self, event) -> None:
        self.draw.scan_dragto(event.x, event.y, gain=1)
        self.draw.itemconfig(self.font_label, fill="")

    def scrollzoom(self, event) -> None:
        factor = 1.001**event.delta
        event_pos = Coord(event.x, event.y)
        self.do_zoom(factor, event_pos)

    def do_zoom(self, factor, pos: Coord) -> None:
        self.resolution *= factor
        self.draw.scale("all", *(pos - self.draw_pos), factor, factor)  # type: ignore
        self.configure_text(self.focused)
        new_label_pos = self.font_label_pos - self.draw_pos
        self.draw.moveto(self.font_label, *new_label_pos)

    def configure_text(self, node: Node, stop=False) -> None:
        text = node.textparams
        text_size = self.resolution * text["r"] * TXT_SCALE
        text_size = int(text_size**TXT_SHRINK)
        self.draw.itemconfig(text["obj"], font=(self.font_style, text_size))
        if text["r"] * self.resolution < self.txtshowres:
            self.draw.itemconfig(text["obj"], fill="")
        else:
            self.draw.itemconfig(text["obj"], fill=self.theme.fg)
        if stop:
            return
        for child in node.children:
            self.configure_text(child, stop=True)

    # -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
    def init_zoom(self) -> None:
        self.zoom = tk.Scale(
            self.win,
            from_=-100,
            to=100,
            orient=tk.HORIZONTAL,
            length=self.w * 0.9,
            width=self.h * 0.04,
            sliderlength=100,
            command=self.scalezoom,
            bg=self.theme.bg,
            highlightthickness=0,
            activebackground=self.theme.bg,
            troughcolor=self.theme.bg2,
            fg=self.theme.fg,
        )
        self.zoom.set(0)
        self.zoom.pack()

    def scalezoom(self, pos) -> None:
        pos = int(pos)
        if pos == 0 or self.scalepos == pos:
            return
        factor = (pos - self.scalepos) * ZOOMSCALE / 100 + 1
        self.scalepos = pos
        self.do_zoom(factor, Coord(int(self.draw_w / 2), int(self.draw_h / 2)))

    # ====================================================================== #
    def start(self) -> None:
        self.draw_map(self.map, recalc_progress=True)
        self.create_font_label()
        tk.mainloop()

    # ====================================================================== #

    def draw_map(
        self,
        node: Node,
        pos=None,
        radius=None,
        rotation: float = 0.75,
        recalc_progress: bool = False,
    ) -> float:
        if pos is None:
            pos = Coord(self.draw_w / 2, self.draw_h / 2)
        if radius is None:
            radius = self.start_radius

        worth_drawing = self.get_distance(node, self.focused) < 3

        node.params["coord"] = pos
        node.params["rotation"] = rotation

        child_num = len(node.children)
        plus_rot = child_num % 2 == 0 and node.parent is not None
        progress = 0.0
        for i in range(child_num):
            new_rotation = (
                i / child_num + rotation + (0.5 / child_num if plus_rot else 0)
            )
            if worth_drawing:
                self.draw.create_line(
                    *self.line_rotate(pos, radius, radius * CONN_LEN, new_rotation),
                    fill=self.theme.bd,
                )
            rotated_new_pos = self.circle_coord(
                pos, radius * CONN_LEN + radius * RAD_SCALE, new_rotation
            )
            if recalc_progress and node.progress > 0:
                node.children[i].progress = node.progress

            progress += self.draw_map(  # RECURSION HERE
                node.children[i],
                pos=rotated_new_pos,
                radius=radius * RAD_SCALE,
                rotation=new_rotation,
                recalc_progress=recalc_progress,
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

    def line_rotate(self, pos: Coord, start, end, rotation) -> tuple[float, ...]:
        return (
            *self.circle_coord(pos, start, rotation),
            *self.circle_coord(pos, end, rotation),
        )

    def circle_coord(self, pos: Coord, radius, rotation) -> Coord:
        rotation *= 2 * pi
        return Coord(pos.x + cos(rotation) * radius, pos.y + sin(rotation) * radius)

    def draw_node(self, node: Node, pos: Coord, r: float) -> None:
        self.draw.create_oval(
            self.oval_coords(pos, r), outline=self.theme.bd, fill=self.circle_fill(node)
        )
        self.draw.create_arc(
            self.oval_coords(pos, r),
            extent=node.progress / 100 * 359.999,
            style=self.pr_style.style,
            outline=self.arc_outline(node.progress),
            fill=self.arc_fill(node.progress),
            width=self.pr_style.arc_width,
        )

    def oval_coords(self, pos: Coord, r) -> tuple[int, int, int, int]:  # r ~ radius
        return (pos.x - r, pos.y - r, pos.x + r, pos.y + r)

    def draw_text(self, node: Node, pos: Coord, r) -> dict[str, int]:
        node_txt = node.text + (
            f"\n{round(node.progress)} %" if SHOW_PERCENTAGE else ""
        )
        text_size = self.resolution * r * TXT_SCALE
        text_size = int(text_size**TXT_SHRINK)
        return {
            "r": r,
            "obj": self.draw.create_text(
                pos.x,
                pos.y,
                text=node_txt,
                fill=(
                    self.theme.focus
                    if node is self.focused
                    or node in self.focused.children
                    and node.parent is not None
                    and node.parent.children.index(node) == self.selected[self.layer]
                    else self.theme.fg if r >= self.txtshowres else ""
                ),
                font=(self.font_style, text_size),
                justify="center",
            ),
        }

    def circle_fill(self, node: Node) -> str:
        return (
            self.theme.pr
            if self.pr_style.mode == "sector" and node.progress == 100
            else (
                ("#202090" if self.theme == THEMES["DARK"] else "#AACCCC")
                if node.params.get("isfile", False)
                else self.theme.bg
            )
        )

    def arc_fill(self, progress) -> str:
        return (
            ""
            if self.pr_style.mode == "sector" and progress == 100
            else self.pr_style.arc_fill
        )

    def arc_outline(self, progress) -> str:
        return (
            ""
            if self.pr_style.mode == "sector" and not 0 < progress < 100
            else self.pr_style.arc_outline
        )

    def set_key_command(self, command: Callable[[tk.Event, Node, int], None]) -> None:
        """key: tk.Event, current_node: Node, selected: int"""
        self.key_command = command


if __name__ == "__main__":
    run_map()
