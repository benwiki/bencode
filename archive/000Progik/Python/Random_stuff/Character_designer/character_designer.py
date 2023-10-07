from tkinter import *
from math import *
from time import time, sleep
from random import uniform

#~~~~~~~~~~~~~~~~~~~~~~~~-
#Defining variables

lastcoord=[-1, -1]
drawing_coord=[]
drawing_object=[]
valid_lines=[]

grabbed=False
the_same_line=False

virt_but_r=150
cur_index=-1
hold_press=0
delete_line_time=0.5

main_color= "#00ff99"

#~~~~~~~~~~~~~~~~~~~~~~~~~~
#Defining functions

def calcDeg(Ln, start=0):
	def easy(x):
		if x >= 0:
			return 1
		elif x < 0:
			return -1
	c = (Ln[2]-Ln[0])/hypot(Ln[1]-Ln[3], Ln[0]-Ln[2])
	s = (Ln[3]-Ln[1])/hypot(Ln[1]-Ln[3], Ln[0]-Ln[2])
	recovery=acos(c)*easy(s)-radians(start)
	dgc=acos(cos(recovery))
	elojel=sin(recovery)
	return degrees(dgc*easy(elojel))
	
def pressed_menu_button(x, y):
	if hypot(x, height-y)<=virt_but_r:
		return 1, True
	elif hypot(width/2-x, height-y)<=virt_but_r:
		angle = calcDeg([width/2,height,x,y])
		if angle<-90:
			return 2, True
		elif angle>=-90:
			return 3, True
	return 0, False
	
def new_line():
	global lastcoord, cur_index, the_same_line
	lastcoord=[-1, -1]
	cur_index=-1
	drawing_coord.append([])
	drawing_object.append([])
	rajz.itemconfig(lampa, state=NORMAL)
	the_same_line=False
	
def undo():
	global drawing_object, cur_index, hold_press, valid_lines, the_same_line
	time_diff=time()-hold_press
	if time_diff<=delete_line_time and drawing_object!=[[]]:
		cur_index=last_valid_line()
		cur_lines=drawing_object[cur_index]
		if abs(cur_index) <= len(drawing_object) and cur_lines!=[]:
			rajz.delete(cur_lines[-1])
			cur_lines.pop()
			if cur_lines==[]:
				valid_lines[cur_index]=0
				cur_index=last_valid_line()
			the_same_line=False
	hold_press=0

def redo():
	#global
	time_diff=time()-hold_press
	if time_diff<=delete_line_time and drawing_object!=[[]]:
		pass

def coord(arg1=None, arg2=None, r=0):
	if isinstance(arg1, tuple) or isinstance(arg1, list):
		x1, y1, x2, y2 = arg1
		r=arg2
		return x1+r, y1+r
	else:
		x, y = arg1, arg2
		return x-r, y-r, x+r, y+r
	
def click(event):
	pass

def motion(event):
	global lastcoord, hold_press
	x, y = event.x, event.y
	n, pressed=pressed_menu_button(x,y)
	buttonToModify=all_buttons[n-1]
	for button in all_buttons:
		rajz.itemconfig(button, fill="#777777")
	if not pressed:
		if lastcoord!=[-1, -1]:
			drawing_object[cur_index].append(rajz.create_line(lastcoord+[event.x, event.y], width=5, capstyle=ROUND, fill='white'))
			if not valid_lines[cur_index]:
				valid_lines[cur_index]=1
		elif not the_same_line:
			new_line()
			valid_lines.append(1)
		lastcoord=[x, y]
		drawing_coord[cur_index].append(lastcoord)
		rajz.itemconfig(lampa, state=HIDDEN)
		hold_press=0
	else:
		if hold_press==0 and (n==2 or n==3):
			hold_press=time()
		lastcoord=[-1, -1]
		rajz.itemconfig(buttonToModify, fill=main_color)
		
def release(event):
	x, y = event.x, event.y
	n, pressed=pressed_menu_button(x, y)
	if pressed:
		if n==1:
			new_line()
		elif n==2:
			undo()
		elif n==3:
			redo()
	for button in all_buttons:
		rajz.itemconfig(button, fill='#777777')
		
def erase(array):
	for item in array:
		rajz.delete(item)
	array.clear()
		
def hold_buttons():
	hold_undo()
	
def hold_undo():
	global drawing_object, cur_index, valid_lines, hold_press, the_same_line
	if time()-hold_press>delete_line_time and drawing_object!=[[]] and hold_press>0:
		if abs(cur_index) <= len(drawing_object):
			cur_index=last_valid_line()
			erase(drawing_object[cur_index])
			valid_lines[cur_index]=0
			cur_index=-1
			the_same_line=True
		hold_press=0
		
def last_valid_line():
	index=cur_index
	while abs(index)<= len(valid_lines) and valid_lines[index]!=1:
		index-=1
	if abs(index)<= len(drawing_object):
		return index
	else: return -1
		
#~~~~~~~~~~~~~~~~~~~~~~~~~~
#Setting up interface
		
ablak=Tk()
ablak.config(bg='white')

width = ablak.winfo_screenwidth()
height = ablak.winfo_screenheight()
rajz=Canvas(width=width, height=height, bg='black', highlightthickness=0)

releaseVirtualButton = rajz.create_oval(coord(0, height, virt_but_r), outline=main_color, fill='#777777', width=10)
releaseText=rajz.create_text(50, height-50, text="NEW\nLINE", fill='white')

undoVirtualButton = rajz.create_arc( coord(width/2, height+5, virt_but_r), start=90, extent=90, fill="#777777", width=10, outline=main_color)
undoText=rajz.create_text(width/2-70, height-40, text="UNDO", fill='white', font="Courier 10")

redoVirtualButton = rajz.create_arc( coord(width/2, height+5, virt_but_r), start=0, extent=90, fill="#777777", width=10, outline=main_color)
redoText=rajz.create_text(width/2+70, height-40, text="REDO", fill='white', font="Courier 10")

all_buttons=[releaseVirtualButton, undoVirtualButton, redoVirtualButton]

lampa=rajz.create_oval(0, height/2-20, 40, height/2+20, fill=main_color, state=HIDDEN)

text=rajz.create_text(width/2, 50, fill='white')

#rajz.bind("<Button-1>", click)
rajz.bind("<Motion>", motion)
rajz.bind("<ButtonRelease-1>", release)

rajz.pack()

while 1:
	ablak.update()
	hold_buttons()
	#rajz.itemconfig(text, text=str(valid_lines)+' '+str(cur_index)+" "+str(drawing_object))