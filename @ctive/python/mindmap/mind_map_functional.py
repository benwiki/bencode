
import tkinter as tk
from dataclasses import dataclass, field
from math import cos, pi, sin
from typing import Optional, List

# Constants and Parameters (Modify these as needed)
FONT_STYLE = 'Segoe UI'

@dataclass
class Coord:
    x: int
    y: int

@dataclass
class Theme:
    bg: str
    fg: str
    bd: str
    pr: str

@dataclass
class Node:
    text: str
    progress: float
    children: List["Node"]
    coord: Coord = None
    rotation: float = 0

class MindMapDrawer:
    def __init__(self, canvas, theme: Theme):
        self.canvas = canvas
        self.theme = theme

    def draw_map(self, node: Node, pos: Coord = None, radius: float = 200, rotation: float = 0):
        if pos is None:
            pos = Coord(self.canvas.winfo_reqwidth() // 2, self.canvas.winfo_reqheight() // 2)
        node.coord = pos
        node.rotation = rotation
        self.draw_node(node, pos, radius)
        angle_step = 2 * pi / max(len(node.children), 1)
        for i, child in enumerate(node.children):
            child_rotation = rotation + i * angle_step
            child_pos = Coord(pos.x + cos(child_rotation) * radius, pos.y + sin(child_rotation) * radius)
            self.canvas.create_line(pos.x, pos.y, child_pos.x, child_pos.y, fill=self.theme.bd)
            self.draw_map(child, child_pos, radius=radius*0.7, rotation=child_rotation)

    def draw_node(self, node: Node, pos: Coord, radius: float):
        self.canvas.create_oval(pos.x - radius, pos.y - radius, pos.x + radius, pos.y + radius, fill=self.theme.bg)
        self.canvas.create_text(pos.x, pos.y, text=node.text, fill=self.theme.fg)

class MindMap:
    def __init__(self, root_node: Node, theme: Theme):
        self.root_node = root_node
        self.theme = theme
        self.window = tk.Tk()
        self.canvas = tk.Canvas(self.window, bg=self.theme.bg, width=800, height=600)
        self.canvas.pack()
        self.drawer = MindMapDrawer(self.canvas, self.theme)

    def draw(self):
        self.drawer.draw_map(self.root_node)

    def run(self):
        self.draw()
        self.window.mainloop()

if __name__ == "__main__":
    # Example usage:
    root = Node("Mind Map", 0, [
        Node("Child 1", 50, []),
        Node("Child 2", 75, [
            Node("Grandchild", 30, [])
        ])
    ])
    theme = Theme(bg="white", fg="black", bd="black", pr="green")
    mind_map = MindMap(root, theme)
    mind_map.run()
