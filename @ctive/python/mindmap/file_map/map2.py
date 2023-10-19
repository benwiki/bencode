#!/usr/bin/python
# -*- coding: utf-8 -*-

import ctypes
import re
import tkinter as tk
from bisect import insort_right
from dataclasses import dataclass, field
from enum import Enum, auto
from math import cos, pi, sin
from tkinter import font
from typing import Callable, Optional

# Activate DPI awareness for better GUI rendering on Windows.
ctypes.windll.shcore.SetProcessDpiAwareness(1)

# ------------------------------ PARAMETERS ------------------------------
MAP_PATH = r"C:\Users\b.hargitai\Documents\Programme\MindMap\onedrive_folder_tree.md"
PLATFORM = "desktop"  # "mobile" / "desktop"
FONT_STYLE = "Segoe UI"
CONN_LEN = 1.5
RAD_SCALE = 0.2
TXT_SCALE = 15
TXT_SHRINK = 0.4
ZOOMSCALE = 2
TAB_AS_SPACES = " " * 4
SHOW_PERCENTAGE = True

# ------------------------------ THEMES ------------------------------


@dataclass
class Theme:
    """Defines the appearance of the MindMap."""

    bg: str  # background
    altbg: str  # alternative background
    fg: str  # foreground
    bd: str  # border
    pr: str  # progress
    focus: str  # focused color


DARK_THEME = Theme(
    bg="#101045",
    altbg="#88AAAA",
    fg="white",
    bd="gray",
    pr="green",
    focus="yellow",
)

LIGHT_THEME = Theme(
    bg="white",
    altbg="lightgrey",
    fg="black",
    bd="grey",
    pr="lightgreen",
    focus="#ff4444",
)

# ------------------------------ PROGRESS STYLES ------------------------------


class StyleMode(Enum):
    ARC = auto()
    SECTOR = auto()


class ProgressStyle:
    """Defines the appearance of progress arcs."""

    def __init__(self, theme: Theme, mode: StyleMode):
        self.theme = theme
        self.mode = mode

        if self.mode == StyleMode.ARC:
            self.setup_arc_style()
        elif self.mode == StyleMode.SECTOR:
            self.setup_sector_style()
        else:
            raise ValueError(f"Unsupported style mode: {mode}")

    def setup_arc_style(self):
        self.arcOutline = self.theme.pr
        self.arcFill = ""
        self.arcWidth = 5
        self.style = "arc"

    def setup_sector_style(self):
        self.arcOutline = self.theme.bd
        self.arcFill = self.theme.pr
        self.arcWidth = 1
        self.style = ""


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
        return Coord(int(self.x * amount), int(self.y * amount))

    def stretch_to(self, pos: "Coord", amount: float):
        return self + (pos - self) * amount


# Node class with explicit attributes:
@dataclass
class Node:
    text: str
    progress: float
    parent: Optional["Node"]
    children: list["Node"]
    indent: int
    coord: Optional[Coord] = None
    rotation: Optional[float] = None
    params: dict = field(default_factory=dict)


class MindMapDrawer:
    def __init__(self, canvas, theme, pr_style, font_style):
        self.canvas = canvas
        self.theme = theme
        self.pr_style = pr_style
        self.font_style = font_style

    def draw_node(self, node: Node, pos: Coord, radius: float):
        """Draw a node with the given attributes."""
        self.canvas.create_oval(
            self._oval_coords(pos, radius),
            outline=self.theme.bd,
            fill=self._circle_fill(node),
        )
        self.canvas.create_arc(
            self._oval_coords(pos, radius),
            extent=node.progress / 100 * 359.999,
            style=self.pr_style.style,
            outline=self._arc_outline(node.progress),
            fill=self._arc_fill(node.progress),
            width=self.pr_style.arcWidth,
        )

    def draw_text(self, node: Node, pos: Coord, radius: float) -> dict[str, int]:
        """Draw text on a node."""
        node_txt = node.text + (
            f"\n{round(node.progress)} %" if SHOW_PERCENTAGE else ""
        )
        text_size = self._calculate_text_size(radius)
        return {
            "radius": radius,
            "obj": self.canvas.create_text(
                pos.x,
                pos.y,
                text=node_txt,
                fill=self.theme.fg,
                font=(self.font_style, text_size),
                justify="center",
            ),
        }

    def draw_connection(self, start: Coord, end: Coord):
        """Draw a connection between two nodes."""
        self.canvas.create_line(start.x, start.y, end.x, end.y, fill=self.theme.bd)

    def calculate_position(self, pos: Coord, radius: float, rotation: float) -> Coord:
        """Calculate position based on rotation."""
        rotation_rad = 2 * pi * rotation
        return Coord(
            pos.x + cos(rotation_rad) * radius, pos.y + sin(rotation_rad) * radius
        )

    # Helper methods

    def _oval_coords(self, pos: Coord, radius: float):
        """Calculate the bounding box coordinates for an oval."""
        return (pos.x - radius, pos.y - radius, pos.x + radius, pos.y + radius)

    def _circle_fill(self, node: Node):
        """Determine the fill color for a node."""
        if self.pr_style.mode == StyleMode.SECTOR and node.progress == 100:
            return self.theme.pr
        elif node.params.get("isfile", False):
            return "#202090"
        return self.theme.bg

    def _arc_fill(self, progress: float):
        """Determine the fill color for an arc."""
        if self.pr_style.mode == StyleMode.SECTOR and progress == 100:
            return ""
        return self.pr_style.arcFill

    def _arc_outline(self, progress: float):
        """Determine the outline color for an arc."""
        if self.pr_style.mode == StyleMode.SECTOR and not 0 < progress < 100:
            return ""
        return self.pr_style.arcOutline

    def _calculate_text_size(self, radius: float) -> int:
        """Calculate the appropriate text size based on the node's radius."""
        text_size = radius * TXT_SCALE
        return int(text_size**TXT_SHRINK)


class MindMapParser:
    def __init__(self, raw_text: str, tab_as_spaces: str = TAB_AS_SPACES):
        self.raw_text = raw_text
        self.tab_as_spaces = tab_as_spaces

    def convert_to_map(self) -> Node:
        """Converts the raw text to a structured mind map tree."""
        parsed_nodes = self._parse_text()
        return self._build_tree(parsed_nodes)

    def _parse_text(self):
        """Parse the raw text into a list of nodes with their indentation levels."""
        nodes = self.raw_text.strip().split("\n")
        parsed_nodes = []

        for node_text in nodes:
            indent, node = self._match_text(node_text)
            node.indent = indent  # Store the indentation level as a node parameter
            parsed_nodes.append(node)

        return parsed_nodes

    def _build_tree(self, parsed_nodes: list[Node]):
        """Builds the tree structure from the parsed nodes."""
        stack: list[Node] = []
        root = parsed_nodes[0]

        for node in parsed_nodes:
            while stack and stack[-1].indent >= node.indent:
                stack.pop()

            if stack and stack[-1].indent < node.indent:
                node.parent = stack[-1]
                stack[-1].children.append(node)

            stack.append(node)

        return root

    # This function has a bad name. It should be called something like "parse_node_text".
    # Even better: split it into two functions: one for parsing the text, and one for building the node.
    def _match_text(self, text: str) -> tuple[int, Node]:
        """Match the text to a regex and return the indentation level and the node."""
        match = re.fullmatch(r"(\s*)([^;]+);?\s*(\d*)", text)
        if not match:
            raise ValueError(f"Invalid node text: {text}")
        indent, name, percent = match.groups()
        return (
            indent.count("\t") + indent.count(self.tab_as_spaces),
            Node(name, self._zero_int(percent), None, []),
        )

    def _zero_int(self, text: str) -> int:
        """Convert a string to int, or return 0 if it's empty."""
        return 0 if text == "" else int(text)


class MindMap:
    def __init__(
        self,
        raw_text: str,
        theme: Theme,
        pr_style: ProgressStyle,
        font_style: str = FONT_STYLE,
    ):
        self.parser = MindMapParser(raw_text)
        self.drawer = MindMapDrawer(theme, pr_style, font_style)
        self.map = self.parser.convert_to_map()
        self.init_window()
        self.init_win_bindings()
        self.init_attributes()
        self.drawer.attach_to_canvas(self.draw)
        if PLATFORM == "mobile":
            self.init_zoom()

    # ... [Other methods remain largely unchanged, but drawing methods now delegate to the MindMapDrawer instance]

    def draw_map(self):
        self.drawer.draw_map(self.map)

    # ... [Other utility methods and event handlers remain largely unchanged]


if __name__ == "__main__":
    run_map()
