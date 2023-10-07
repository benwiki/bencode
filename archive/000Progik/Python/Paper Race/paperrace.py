from tkinter import *
from random import uniform, shuffle
from math import *
from datetime import datetime
dist = hypot

ablak=Tk()
ablak.configure(bg='black')

#EYYY IT ACTUALLY WORKS!!!!
#now I sleep a little.

##############################
# Defining too many variables

mennyi=35
koz=int(700/mennyi)
lightred='#ff7f7f'
red='#af0000'
gray='#777777'

ex, ey=0,340
kx, ky=0,0
tx, ty=koz*2, koz*2
r=6

trackbuild=False
submitted=False
ready=False
first=True
grayz=False
stline=False
over=False
start=False
hatrahagy=True
default=True
lines=[]
colors=[]
players=[]
crash=[]
myind=0

try:
	f=open('settings.txt', 'r')
	mode=int(f.readline())
	f.close()
except:
	f=open('settings.txt', 'w')
	f.write('2')
	f.close()
	mode=2

legit=0
myip=''
seltrack=''

##############################
#~~~~~~~~~~~~~~~~~~~~~~~~~~
#Functions

def lepes(a, b):
	global x, y, ex, ey, kx, ky, celok, navibuttons, track, lines, rajz, tx, ty, lastpoint, first, mycurln, mycurpt, hatrahagy, default, crash
	if trackbuild:
		if grayz:
			letter='G'
			color=gray
		elif stline:
			letter='S'
			color=lightred
		else:
			letter='N'
			color='black'
		rajz.itemconfig(point, outline=color)
		rajz.itemconfig(lastpoint, outline=color)
		if a==0 and b==0:
			rajz.create_line(tx, ty, x, y, width=4, fill=color)
			if not first:
				lines.append([letter, tx, ty, x, y])
			tx, ty=x, y
			rajz.delete(lastpoint)
			lastpoint=rajz.create_oval(tx-r, ty-r, tx+r, ty+r, width=r, outline=color)
			first=False
		else:
			x, y=x+a, y+b
			rajz.move(point, a, b)
			if first:
				rajz.move(lastpoint, a, b)
				tx, ty=x, y
	else:
		kx, ky=x+(x-ex)+a, y+(y-ey)+b
		if hatrahagy:
			ex, ey=x, y
			x, y=kx, ky
			check()
			if not crash[myind]==1:
				selgame.append([colors[myind], ex, ey, x, y, myind, players[myind][0]])
				players[myind][1]=ex
				players[myind][2]=ey
				players[myind][3]=x
				players[myind][4]=y
				rajz.create_line(ex, ey, x, y, width=3, fill=colors[myind])
				rajz.create_oval(x-r, y-r, x+r, y+r, width=r, outline=colors[myind])
			else:
				rajz.delete(mycurln)
				rajz.delete(mycurpt)
				mycurln=rajz.create_line(ex, ey, ex, ey, width=3, fill=colors[myind])
				mycurpt=rajz.create_oval(ex-r, ey-r, ex+r, ey+r, width=r, outline=colors[myind])
			hatrahagy=False
		else:
			default=False
			rajz.delete(mycurln)
			rajz.delete(mycurpt)
			mycurln=rajz.create_line(x, y, kx, ky, width=3, fill=colors[myind])
			mycurpt=rajz.create_oval(kx-r, ky-r, kx+r, ky+r, width=r, outline=colors[myind])
		
			
#~~~~~~~~~~~~~~~~~~~~~~~~~~

def balfenn():
	lepes(-koz, -koz)
def balkoz():
	lepes(-koz,0)
def ballenn():
	lepes(-koz,koz)
def kozfenn():
	lepes(0, -koz)
def kozkoz():
	lepes(0,0)
def kozlenn():
	lepes(0,koz)
def jobbfenn():
	lepes(koz,-koz)
def jobbkoz():
	lepes(koz,0)
def jobblenn():
	lepes(koz,koz)
	
def sub():
	global submitted
	submitted=True
	
def grayzonefunc():
	global grayz, stline, first, rajz
	rajz.itemconfig(point, outline=gray)
	rajz.itemconfig(lastpoint, outline=gray)
	grayz=True
	stline=False
	first=True

def startinglinefunc():
	global stline, grayz, first, rajz
	rajz.itemconfig(point, outline=lightred)
	rajz.itemconfig(lastpoint, outline=lightred)
	first=True
	grayz=False
	stline=True
	
def normfunc():
	global stline, grayz, first, rajz
	rajz.itemconfig(point, outline="black")
	rajz.itemconfig(lastpoint, outline="black")
	first=True
	grayz=stline=False
	
#~~~~~~~~~~~~~~~~~~~~~~~~~

def coloring(a, b):
	which = 255*5*(a/b)
	if which <256:
		color='#0000'
		if which<16:
			color+='0'
		color+= (str(hex(int(which)))[2:])
	elif which <511:
		color='#00'
		which -=255
		if which<16:
			color+='0'
		color+= (str(hex(int(which)))[2:])
		color+='ff'
	elif which <766:
		color='#00ff'
		which-=510
		which= 255-which
		if which<16:
			color+='0'
		color+= (str(hex(int(which)))[2:])
	elif which <1021:
		color='#'
		which-=765
		if which<16:
			color+='0'
		color+= (str(hex(int(which)))[2:])
		color+='ff00'
	elif which < 1276:
		color='#ff'
		which-=1020
		which= 255-which
		if which<16:
			color+='0'
		color+= (str(hex(int(which)))[2:])
		color+='00'
	return color
	
#~~~~~~~~~~~~~~~~~~~~~~~~~
	
def linecross(line1, line2):
	global legit, mode
	x1, y1, x2, y2= (line1[i] for i in range(1,5))
	x3, y3, x4, y4= (line2[i] for i in range(1,5))
	oszt1=((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1))
	oszt2=((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1))
	if oszt1!=0 and oszt2!=0:
		px = ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3)) / oszt1
		py = ((x2-x1)*(y1-y3) - (y2-y1)*(x1-x3)) / oszt2
	else:
		return False
		
	if mode==1 and px>0 and px<1 and py>0 and py<1:
		return True
		
	elif mode==2 and py>=0 and py<=1 and px>=0 and px<=1:
		
		if py==1:
			return True
		elif px>0 and px<1:
			return True
		elif px==0:
			legit.append(line1[3:5])
		elif px==1:
			legit.append(line1[1:3])
		
	elif mode==3 and px>=0 and px<=1 and py>=0 and py<=1:
		return True
	else:
		return False

#~~~~~~~~~~~~~~~~~~~~~~~~~

def st():
	global trackfile, lines, rajz, navibuttons, savetrack, cleartrack, trackbuild, grayzone, startingline, normal, seltrack
	trackfile=open(seltrack, 'w')
	trackfile.write(str(lines))
	trackfile.close()
	
	rajz.delete('all')
	rajz.grid_forget()
	normal.grid_forget()
	grayzone.grid_forget()
	startingline.grid_forget()
	savetrack.grid_forget()
	cleartrack.grid_forget()
	
	for i in range(3):
		for j in range(3):
			navibuttons[i][j].grid_forget()
	for i in range(3):
		startbuttons[i].grid(padx=120, pady=100)
	trackbuild=False

#~~~~~~~~~~~~~~~~~~~~~~~~~~

def ct():
	global point, lastpoint, x, y, ex, ey, tx, ty, first, lines
	rajz.delete('all')
	ex, ey=0,340
	tx, ty=koz*2, koz*2
	for i in range(mennyi):
		rajz.create_line(i*koz, 0, i*koz, 700, fill=gray)
	for i in range(mennyi):
		rajz.create_line(0, i*koz, 700, i*koz, fill=gray)
	
	x, y=koz*2, koz*2
	point=rajz.create_oval(x-r, y-r, x+r, y+r, width=r, outline='black')
	lastpoint=rajz.create_oval(x-r, y-r, x+r, y+r, width=r, outline='black')

	first=True
	lines=[]
	
#~~~~~~~~~~~~~~~~~~~~~~~~~~

def newtrack():
	global lines, startbuttons, point, x, y, rajz, trackbuild, lastpoint, first, submitted, seltrack, start
	for i in range(3):
		startbuttons[i].grid_forget()
	
	instruction.config(text='Select or add new track')
	instruction.grid(padx=150, pady=50)
	list.grid(padx=150, pady=20)
	f=open('alltracks.txt', 'r')
	trackslist=[line for line in f]
	f.close()
	for track in trackslist:
		list.insert(END, track[:-5])
	startbutton['text']='Select track'
	startbutton.grid(padx=150, pady=20)
	name.grid(padx=150, pady=10)
	name.delete(0, END)
	submit['text']='Add new track'
	submit.grid(padx=150)
	
	submitted=False
	start=False
	while not start:
		ablak.update()
		if submitted:
			list.insert(END, name.get())
			trackslist.append(name.get()+ '.txt\n')
			f=open('alltracks.txt', 'a')
			f.write(name.get()+'.txt\n')
			f.close()
			open(name.get()+'.txt', 'w').close()
			submitted = False
			name.delete(0, END)
	seltrack= trackslist[list.curselection()[0]][:-1]
	list.delete(0, END)
	
	instruction.grid_forget()
	name.grid_forget()
	submit.grid_forget()
	list.grid_forget()
	startbutton.grid_forget()
	
	x, y=koz*2, koz*2
	rajz.grid(columnspan=12)
	try:
		track=eval(open(seltrack, 'r').read())
		for line in track:
			if line[0]=='N':
				color="black"
			elif line[0]=='G':
				color=gray
			else:
				color=lightred
			rajz.create_line(line[1], line[2], line[3], line[4], width=4, fill=color)
	except:
		track=[]
	

	for i in range(3):
		for j in range(3):
			navibuttons[i][j].grid(row=i+1, column=j, pady=10)
	
	savetrack.grid(column=0,row=5, columnspan=10)
	cleartrack.grid(column=0, row=6, columnspan=10)
	normal.grid(row=1, column=3, columnspan=5)
	grayzone.grid(row=2, column=3, columnspan=5)
	startingline.grid(row=3, column=3, columnspan=5)
		
	for i in range(mennyi):
		rajz.create_line(i*koz, 0, i*koz, 700, fill=gray)
	for i in range(mennyi):
		rajz.create_line(0, i*koz, 700, i*koz, fill=gray)

	point=rajz.create_oval(x-r, y-r, x+r, y+r, width=r, outline='black')
	lastpoint=rajz.create_oval(x-r, y-r, x+r, y+r, width=r, outline='black')
	
	first=True
	lines=track
	trackbuild=True
	

#~~~~~~~~~~~~~~~~~~~~~~~~~~

def startfunc():
	global start
	start=True

#~~~~~~~~~~~~~~~~~~~~~~~~

def newgame():
	global submitted, players, seltrack, jelszo, playercount, selgame
	
	for i in range(3):
		startbuttons[i].grid_forget()
		
	global playercoords
	playercoords=[]
	jelszo.set("Players: ")
	jelszolab.grid(pady=20, padx=40)
	list.grid(padx=150, pady=20)
	name.grid(padx=150, pady=0)
	name.delete(0, END)
	submit['text']='Add player'
	submit.grid(padx=150)
	
	startbutton['text']='Start game'
	startbutton.grid(padx=150, pady=50)
	ablak.update()
	playercount=0
	global start
	start=False
	while 1:
		submitted=False
		while not (submitted and len(name.get())!=0):
			if submitted and len(name.get())==0:
				submitted=False
			ablak.update()
			if start and len(list.get(0, END))!=0:
				break
			else:
				start=0
		if start:
			break
		players.append([name.get()])
		list.insert(END, name.get())
		name.delete(0, END)
		ablak.update()
		playercount+=1
	name.grid_forget()
	shuffle(players)
	jelszolab.grid_forget()
	submit['text']='Choose track'
	startbutton.grid_forget()
	list.delete(0, END)
	f=open('alltracks.txt', 'r')
	trackslist=[line for line in f]
	f.close()
	for track in trackslist:
		list.insert(END, track[:-5])
	submitted=False
	while not submitted:
		ablak.update()
	seltrack= trackslist[list.curselection()[0]][:-1]
	
	list.delete(0, END)
	f=open('games.txt', 'r')
	games=[]
	exist=False
	for line in f:
		L=line.split('\t')
		if L[0]==seltrack:
			list.insert(END, str(L[1]))
			games.append(eval(L[2]))
			
	selgame=[]
	if len(games)!=0:
		players=[[]for i in range(playercount)]
		submit['text']='Choose game:'
		submitted=False
		while not submitted:
			ablak.update()
		selgame=games[list.curselection()[0]]
	
	list.grid_forget()
	submit.grid_forget()
	Startgame()

#~~~~~~~~~~~~~~~~~~~~~~~~

#ez egy csoda b+. mármint hogy működik
#ez matematikai bűvészet barátom
def calcDeg(start, Ln):
	def easy(x):
		if x >= 0:
			return 1
		elif x < 0:
			return -1
	"""def correct(x):
		if x<0:
			return 360+x 
		else:
			return x"""
	c = (Ln[2]-Ln[0])/dist(Ln[1]-Ln[3], Ln[0]-Ln[2])
	s = (Ln[3]-Ln[1])/dist(Ln[1]-Ln[3], Ln[0]-Ln[2])
	recovery=acos(c)*easy(s)-radians(start)
	dgc=acos(cos(recovery))
	elojel=sin(recovery)
	return degrees(dgc*easy(elojel))

def ok_sides(line, points):
	alapallas=calcDeg(0, line)
	left=right=0
	for pt in points:
		relDeg=calcDeg(alapallas, line[:2]+pt)
		if relDeg>0:
			left+=1
		elif relDeg<0:
			right+=1
		else:
			return False
	if left>0 and right>0:
		return False
	else:
		return True

#~~~~~~~~~~~~~~~~~~~~~~~~

def check():
	grayct=0
	global myind, track, ex, ey, x, y, crash, legit
	legit=[]
	for line in track:
		if linecross(line, ['', ex, ey, x, y]):
			if line[0]=='N':
				crash[myind]=1
			elif line[0]=='G':
				grayct+=1
			else:
				crash[myind]=2
	if len(legit)>1:
		if not ok_sides([ex, ey, x, y], legit):
			crash[myind]=1
	if grayct%2==1:
		crash[myind]=1
	for i in range(playercount):
		if myind != i and players[i][3:5]==players[myind][3:5]:
			crash[myind]=1

#~~~~~~~~~~~~~~~~~~~~~~~~~~

def setPlayer(p, line):
	global players, rajz, sock, colors, mycurln, mycurpt, selgame
	x=line[1]+koz
	if line[4]-line[2]>0:
		y=line[2]+koz+p*koz
	else:
		y=line[4]+koz+p*koz
	players[p].append(line[1])
	players[p].append(y)
	players[p].append(x)
	players[p].append(y)
	color=coloring(p+1, len(players))
	colors.append(color)
	selgame.append([color, line[1], y, x, y, p, players[p][0]])
	if p==myind:
		mycurln=rajz.create_line(line[1], y, x, y, width=4, fill=color)
		mycurpt=rajz.create_oval(x-r, y-r, x+r, y+r, width=r, outline=color)
	rajz.create_line(line[1], y, x, y, width=4, fill=color)
	rajz.create_oval(x-r, y-r, x+r, y+r, width=r, outline=color)
	return x, y

#~~~~~~~~~~~~~~~~~~~

def savegame():
	f=open('games.txt', 'a')
	t='\t'
	f.write(seltrack+t+str(datetime.now())+t+str(selgame)+'\n')
	f.close()

#~~~~~~~~~~~~~~

def Startgame():
	global seltrack, players, x, y, playercount, ex, ey, celok, myind, submitted, hatrahagy, kx, ky, track, crash, default, selgame, colors, mycurln, mycurpt
	rajz.grid(columnspan=12)
		
	for i in range(mennyi):
		rajz.create_line(i*koz, 0, i*koz, 700, fill=gray)
	for i in range(mennyi):
		rajz.create_line(0, i*koz, 700, i*koz, fill=gray)
		
	savedgame=len(selgame)!=0
	track=eval(open(seltrack, 'r').read())
	for line in track:
		if line[0]=='N':
			color="black"
		elif line[0]=='G':
			color=gray
		else:
			color=lightred
			for i in range(playercount):
				if savedgame:
					break
				if i==0:
					x, y=setPlayer(i, line)
					myind=i
				else:
					setPlayer(i, line)
		rajz.create_line(line[1], line[2], line[3], line[4], width=4, fill=color)

	
	if savedgame:
		max= selgame[0][5]
		for step in selgame:
			color=step[0]
			rajz.create_line(step[1], step[2], step[3], step[4], width=3, fill=color)
			rajz.create_oval(step[3]-r, step[4]-r, step[3]+r, step[4]+r, width=r, outline=color)
			if max<step[5]: max=step[5]
		playercount=max+1
		
		osszeszed=[]
		for step in reversed(selgame):
			if not step[5] in osszeszed:
				if playercount-len(osszeszed)==1:
					players[step[5]].append( [step[6], step[1], step[2], step[3], step[4]])
					cur=players[step[5]]
					break
				else:
					players[step[5]].append( [step[6], step[1], step[2], step[3], step[4]])
					osszeszed.append(step[5])
					
		mycurln=rajz.create_line(cur[1], cur[2], cur[3], cur[4], width=3, fill=color)
		mycurpt=rajz.create_oval(cur[3]-r, cur[4]-r, cur[3]+r, cur[4]+r, width=r, outline=color)
		x, y=cur[-2:]
		ex, ey=cur[1:3]
		#x, y=selgame[-playercount][-2:]
		#ex, ey = selgame[-playercount][1:3]
		"""if playercount>1:
			for i in range(playercount)
				for g in selgame[-playercount+]:
					p+= [g[1], g[2], g[3], g[4]]
		else:
			g = selgame[-1]
			players[0]+=[g[1], g[2], g[3], g[4]]
			color=coloring(i+1, len(players))
			colors.append(color)"""
			
	else:
		ex=x-koz
		ey=y
	a= x+(x-ex)
	b= y+(y-ey)
	celok=[[rajz.create_oval(a-r+(i*koz), b-r+(j*koz), a+r+(i*koz), b+r+(j*koz), outline=lightred) for j in range(-1, 2)] for i in range(-1, 2)]
	
	
	submit['text']='Take move'
	for i in range(3):
		for j in range(3):
			navibuttons[i][j].grid( row=i+1, column=j, pady=10)
	submit.grid(row=1, column=3, columnspan=7)
	savegamebut.grid(row=3, column=3, columnspan=7)
	instruction['text']='Crashed: '
	instruction.grid(columnspan=3)
	Label(text=str()).grid()
	crash=[0 for i in range(playercount)]
	while not over:
		for i in range(playercount):
			ablak.update()
			if True:
				instruction['text']='Crashed: '
				myind=i
				ex, ey, x, y=(players[i][k] for k in range(1,5))
				noone=True
				for k in range(playercount):
					if crash[k]==1:
						noone=False
						instruction['text'] +='\n'+players[k][0]
				if noone:
					instruction['text'] +='Nobody'
				if crash[i]==1:
					players[i][1]=x
					players[i][2]=y
					players[i][3]=x
					players[i][4]=y
					crash[myind]=0
					continue
				message['text']='Next player: \"'+players[i][0]+'\"'
				message['fg']=colors[i]
				message.grid(columnspan=3)
				for i in range(3):
					for j in range(3):
						rajz.delete(celok[i][j])
				a= x+(x-ex)
				b= y+(y-ey)
				celok= [[rajz.create_oval( a-r+(i*koz), b-r+(j*koz), a+r+(i*koz), b+r+(j*koz), outline=lightred) for j in range(-1, 2)] for i in range(-1, 2)]
				for i in range(3):
					for j in range(3):
						navibuttons[i][j]['activebackground'] = colors[myind]
				hatrahagy=False
				submitted=False
				default=True
				while not submitted:
					ablak.update()
				hatrahagy=True
				submit.grid_forget()
				for k in range(7000):
					ablak.update()
				submit.grid(row=1, column=3, columnspan=7)
				a, b=rajz.coords(mycurln)[2], rajz.coords(mycurln)[3]
				a, b=a-(x+(x-ex)), b-(y+(y-ey))
				if default:
					lepes(0,0)
				else:
					lepes(a, b)

#~~~~~~~~~~~~~~~~~~~~~~~~~

def setdifficulty(x):
	global mode
	for i in range(3):
		if i==x-1:
			col='#a5ff00'
		else:
			col='white'
		setbuttons[i].config(bg=col, activebackground=col)
	f=open('settings.txt', 'w')
	f.write(str(x))
	f.close()
	mode=x
	
def back():
	for i in range(3):
		setbuttons[i].grid_forget()
	backtomenu.grid_forget()
	for i in range(3):
		startbuttons[i].grid(padx=120, pady=100)

def settings():
	for i in range(3):
		startbuttons[i].grid_forget()
	backtomenu.grid()
	for i in range(3):
		setbuttons[i].grid(pady=100, column=i, row=1)
	
	setdifficulty(int(open('settings.txt', 'r').read()))
		

############################
#Defining widgets

instruction=Label(ablak, fg='white', bg='black')
name=Entry(ablak)
submit=Button(text="submit", command=sub, bg='white', activebackground='white')
startbutton=Button(command=startfunc, bg='white')
savegamebut=Button(text='Save Game', command=savegame, activebackground='white')

rajz=Canvas(width=700, height=700, bg='white')

functions=[[balfenn, balkoz, ballenn], [kozfenn, kozkoz, kozlenn], [jobbfenn, jobbkoz, jobblenn]]

savetrack=Button(text='Save track & return to menu', command=st, bg='white')

cleartrack=Button(text='Clear track', command=ct, bg='white')

normal=Button(text='Draw normal lines', command=normfunc, bg='white')
grayzone=Button(text='Draw gray zone', command=grayzonefunc, bg='white')
startingline=Button(text='Draw starting line', command=startinglinefunc, bg='white')

navibuttons=[[Button(ablak, text='o', command=functions[j][i], bg='white', activebackground=lightred)for j in range(3)] for i in range(3)]

startbuttons=[]
startbuttons.append(Button(text='Manage Tracks', width=20, height=5, command=newtrack, bg='white'))
startbuttons.append(Button(text='Start GAME', width=20, height=5, command=newgame, bg='white'))
startbuttons.append(Button(text="Settings", width=20, height=5, command=settings, bg='white'))

#list=Listbox(ablak, bg='#d0d0d0')
list=Listbox(bg=gray, fg='white', selectforeground=lightred)
jelszo=StringVar()
jelszolab=Label(ablak, textvariable=jelszo, fg='white', bg='black')

message=Label(ablak, fg='white', bg='black')

backtomenu=Button(text='<-- back', command=back, bg='white')

setbuttons=[]
setbuttons.append(Button(ablak, text='Ultra\nCheat ^-^', height=3, command=lambda:setdifficulty(1)))
setbuttons.append(Button(ablak, text='Normal', height=3, command=lambda: setdifficulty(2)))
setbuttons.append(Button(ablak, text='Super\nStrict!!!', height=3, command=lambda: setdifficulty(3)))

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#Start program 

for i in range(3):
	startbuttons[i].grid(padx=120, pady=100)
		
ablak.mainloop()
		
		

