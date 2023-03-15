#!/usr/bin/python
# -*- coding: utf-8 -*-

import tkinter as tk
from dataclasses import dataclass
from math import cos, pi, sin
from typing import Optional
import re

conn_len = 2
rad_scale = 0.4
tab = ' '*4


@dataclass
class Block:
	text: str
	progress: float
	parent: Optional["Block"]
	children: list["Block"]


zero_int = lambda text : 0 if text=="" else int(text)


def match_text(text: str) -> Optional[tuple[int, Block]]:
	m = re.fullmatch(r'(\s*)([^;]+);?(\d*)', text)
	if not m:
		return None
	intend, name, percent = m.groups()
	return(max(intend.count('\t'),intend.count(tab)),
			Block(name, zero_int(percent), None, []))


def convert_to_map(string: str) -> Block:
	start: Block = Block("main", 0, None, [])
	cur_block = Block("", 0, start, [])
	blocks = string.strip().split('\n')
	old_intend = 0
	for i, block in enumerate(blocks):
		block_match = match_text(block)
		if block_match is None:
			raise RuntimeError(f"{i+1}. line is not matching!")
		intendation, new_block = block_match
		if intendation > old_intend + 1 or cur_block is None:  # bc of mypy
			raise RuntimeError("Too high intendation!")
		elif intendation == old_intend + 1:
			new_block.parent = cur_block
		elif intendation == old_intend:
			new_block.parent = cur_block.parent
		else:
			back = old_intend - intendation
			while back > 0:
				if cur_block.parent is None:
					raise RuntimeError("You can't use negative "
									   "intendations!")
				cur_block = cur_block.parent
				back -= 1
			new_block.parent = cur_block.parent
		if new_block.parent is None:
			raise RuntimeError("You can't use negative intendations!")
		cur_block = new_block
		new_block.parent.children.append(cur_block)
		old_intend = intendation
	return start


def md_helper(text: str):
	block = convert_to_map(text)
	_ = MindMap(block)


def oval_coords(x, y, r):
	return (x-r, y-r, x+r, y+r)


def rot_coord(x, y, r, rot):
	rot *= 2*pi
	return (x + cos(rot)*r, y + sin(rot)*r)


def line_rotate(x, y, s, e, rot):
	return (*rot_coord(x, y, s, rot), *rot_coord(x, y, e, rot))


class MindMap:
	def __init__(self, block: Block):
		self.bgcolor="#151551"
		
		self.win = tk.Tk()
		self.win["bg"] = self.bgcolor;
		self.w = self.win.winfo_screenwidth()
		self.h = self.win.winfo_screenheight()
		self.draw_w, self.draw_h = self.w, self.h*0.85
		
		self.draw_pos = {'x': 0, 'y': 0}
		self.texts: list[tuple[float, int]] = []
		self.resolution = 1
		self.scalepos = 0
		self.start_radius = self.draw_w/12
		self.txtshowres = (self.draw_w+self.draw_h)/70
		
		self.draw = tk.Canvas(self.win,
			width=self.draw_w,
			height=self.draw_h,
			background="black",
			highlightthickness=0
		)
		self.draw.pack()

		self.draw.bind("<ButtonRelease-1>", self.release)
		self.draw.bind('<ButtonPress-1>', self.press)
		self.draw.bind("<B1-Motion>", lambda event:
					   self.draw.scan_dragto(event.x, event.y, gain=1))
		self.zoom = tk.Scale(self.win, from_=-100, to=100,orient=tk.HORIZONTAL, length=self.w*0.9, width=self.h*0.04,sliderlength=100, command=self.scalezoom, bg=self.bgcolor, highlightthickness=0,activebackground=self.bgcolor, troughcolor="#AACCFF", fg="white")
		self.zoom.set(0)
		self.zoom.pack()
		
		self.win.bind("<ButtonRelease-1>", self.winrelease)

		self.draw_map(block, self.draw)
		tk.mainloop()
		
	def draw_map(self,
			block: Block,
			draw: tk.Canvas,
			x=None, y=None,
			r=None, rot=0.0, layer=1.0):
		if x is None: x = self.draw_w/2
		if y is None: y = self.draw_h/2
		if r is None: r = self.start_radius
		child_num = len(block.children)
		plus_rot = (child_num % 2 == 0 and block.parent is not None)
		progress = 0
		for i in range(child_num):
			rotation = i / child_num + rot + (0.5/child_num if plus_rot else 0)
			draw.create_line(line_rotate(x, y, r, r*conn_len, rotation),
							 fill="grey")
			linerot = rot_coord(x, y, r*conn_len + r*rad_scale, rotation)
			if block.progress > 0:
				block.children[i].progress = block.progress
			progress += self.draw_map(block.children[i], draw,
									  linerot[0], linerot[1],
									  r*rad_scale, rotation, layer*1.2)

		draw.create_oval(oval_coords(x, y, r), outline="grey")
		if child_num != 0:
			avg_progress = progress / child_num
			block.progress = avg_progress
		if block.progress < 1:
			block.progress = 0
		if block.progress > 99:
			block.progress = 99.9
		draw.create_arc(oval_coords(x, y, r),
						extent=block.progress/100*360,
						style="arc", outline="green", width=4)
		fill = ("white" if r >= self.txtshowres else "")
		self.texts += [(r, draw.create_text(x, y,
											text=block.text +
											f"\n{round(block.progress)} %",
											fill=fill,
											justify="center"))]
		return block.progress

	def press(self, event):
		self.scan_mark_pos = (event.x, event.y)
		self.draw.scan_mark(event.x, event.y)

	def release(self, event):
		self.draw_pos['x'] += event.x - self.scan_mark_pos[0]
		self.draw_pos['y'] += event.y - self.scan_mark_pos[1]

	def winrelease(self, event):
		self.zoom.set(0)
		self.scalepos = 0
		
	def scalezoom(self, pos):
		pos = int(pos)
		if pos == 0 or self.scalepos == pos: return
		factor = (pos-self.scalepos)/50+1
		self.scalepos = pos
		self.resolution *= factor
		self.draw.scale("all",
						self.draw_w/2 - self.draw_pos['x'],
						self.draw_h/2 - self.draw_pos['y'],
						factor, factor)
		for text in self.texts:
			if text[0] * self.resolution < self.txtshowres:
				self.draw.itemconfig(text[1], fill="")
			else:
				self.draw.itemconfig(text[1], fill="white")
