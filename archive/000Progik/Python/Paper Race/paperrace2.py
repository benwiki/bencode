from tkinter import *
from random import uniform, shuffle
from math import *
import socket

ablak=Tk()

#EYYY IT ACTUALLY WORKS!!!!
#now I sleep a little.

##############################
# Defining variables

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
hatrahagy=True
lines=[]
colors=[]
players=[]
myind=0
myip=''
seltrack=''

sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


myip = ([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0])


##############################
#~~~~~~~~~~~~~~~~~~~~~~~~~~
#Functions

def lepes(a, b):
	global x, y, ex, ey, kx, ky, celok, navibuttons, track, lines, rajz, tx, ty, lastpoint, first, mycurln, mycurpt, hatrahagy
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
			rajz.create_line(ex, ey, x, y, width=3, fill=colors[myind])
			rajz.create_oval(x-r, y-r, x+r, y+r, width=r, outline=colors[myind])
			hatrahagy=False
		else:
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
	x1, y1, x2, y2= (line1[i] for i in range(4))
	x3, y3, x4, y4= (line2[i] for i in range(4))
	px = ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3)) / ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1))
	py = ((x2-x1)*(y1-y3) - (y2-y1)*(x1-x3)) / ((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1))
	print(px, py)
	if px>=0 and px<=1 and py>=0 and py<=1:
		return True
	else:
		return False
		
#~~~~~~~~~~~~~~~~~~~~~~~~~~

def setPlayer(p, line):
	global players, rajz, sock, colors, mycurln, mycurpt
	x=line[1]+koz
	if line[4]-line[2]>0:
		y=line[2]+koz+p*koz
	else:
		y=line[4]+koz+p*koz
	color=coloring(p+1, len(players))
	colors.append(color)
	if p==myind:
		mycurln=rajz.create_line(line[1], y, x, y, width=4, fill=color)
		mycurpt=rajz.create_oval(x-r, y-r, x+r, y+r, width=r, outline=color)
	rajz.create_line(line[1], y, x, y, width=4, fill=color)
	rajz.create_oval(x-r, y-r, x+r, y+r, width=r, outline=color)
	return x, y
	

#~~~~~~~~~~~~~~~~~~~~~~~~~

def st():
	global trackfile, lines, rajz, navibuttons, savetrack, cleartrack, trackbuild, grayzone, startingline, normal
	trackfile.write(str(lines))
	trackfile.close()
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
		startbuttons[i].grid(padx=120, pady=30)
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
	global lines, startbuttons, point, x, y, rajz, trackbuild, lastpoint, first, submitted, newtrackfile, cleartrack, savetrack
	for i in range(3):
		startbuttons[i].grid_forget()
	
	instruction.config(text='Name of the track?')
	instruction.grid(padx=150, pady=100)
	name.grid(padx=150, pady=30)
	submit['text']='submit'
	submit.grid(padx=150)
	
	submitted=False
	while not submitted:
		ablak.update()
	
	global trackfile, alltracksfile
	trackfile=open(name.get()+'.txt', 'w')
	if not (name.get()+'.txt\n') in open('alltracks.txt', 'r').readlines():
		alltracksfile=open('alltracks.txt', 'a')
		alltracksfile.write(name.get()+'.txt\n')
		alltracksfile.close()
	
	instruction.grid_forget()
	name.grid_forget()
	submit.grid_forget()
	
	x, y=koz*2, koz*2
	rajz.grid(columnspan=12)

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
	lines=[]
	trackbuild=True
	

#~~~~~~~~~~~~~~~~~~~~~~~~~~

def newgame():
	global submitted, players, seltrack, jelszo, playercount
	
	for i in range(3):
		startbuttons[i].grid_forget()
		
	instruction.config(text='Your name, sir/madam?')
	instruction.grid(padx=150, pady=100)
	name.grid(padx=150, pady=30)
	name.delete(0, END)
	submit['text']="submit"
	submit.grid(padx=150)
	submitted=False
	while not submitted:
		ablak.update()
	myname=name.get()
	
	instruction.config(text='How many more \nplayers will participate?')
	name.delete(0, END)
	submitted=False
	while not submitted:
		ablak.update()
	playercount=int(name.get())
	
	instruction.grid_forget()
	name.grid_forget()
	submit.grid_forget()
	port=int(open('portfile.txt', 'r').read())
	jelszo.set("Starting port:            "+str(port))
	jelszolab.grid(pady=20, padx=40)
	list.grid(padx=150, pady=50)
	submit['text']='Start game'
	submit.grid(padx=150)
	ablak.update()
	
	players.append([myname, -1])
	for i in range(playercount):
		sock.bind((myip, port+i))
		data, addr=sock.recvfrom(1024)
		data=data.decode('utf-8')
		players.append([data, port+i])
		list.insert(END, data)
		ablak.update()
	
	p=int(open('portfile.txt', 'r').read())
	f=open('portfile.txt', 'w')
	f.write(str(p+playercount))
	f.close()
	
	playercount+=1
		
	submitted=False
	while not submitted:
		ablak.update()
	
	shuffle(players)
	for i in range(playercount):
		sock.sendto( str(players).encode('utf-8'), (myip, port+i))
	
	
	jelszolab.grid_forget()
	submit['text']='Choose track'
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
	list.grid_forget()
	submit.grid_forget()
	
	"""for i in range(playercount):
		if players[i][1]!=-1:
			sock.sendto(open(seltrack, 'r').read().encode('utf-8'), (myip, players[i][1]))"""
	Startgame()

#~~~~~~~~~~~~~~~~~~~~~~~~~~

def joingame():
	global submitted, masterport
	for i in range(3):
		startbuttons[i].grid_forget()
		
	instruction.config(text='Your name, sir/madam?')
	instruction.grid(padx=150, pady=100)
	name.grid(padx=150, pady=30)
	name.delete(0, END)
	submit['text']="submit"
	submit.grid(padx=150)
	submitted=False
	while not submitted:
		ablak.update()
	myname=name.get()
	
	instruction.config(text='What\'s your port?')
	name.delete(0, END)
	submitted=False
	while not submitted:
		ablak.update()
	masterport=int(name.get())
	
	instruction.grid_forget()
	name.grid_forget()
	submit.grid_forget()

	
	sock.sendto(myname.encode('utf-8'), (myip, masterport))
	message['text']='Waiting for data'
	message.grid(padx=120, pady=100)
	ablak.update()
	sock.bind((myip, masterport))
	data, addr=sock.recvfrom(1024)
	data=data.decode('utf-8')
	players=eval(data)
	i=0
	for player in players:
		if player[0]==myname:
			myind=i
		if player[1]==-1:
			masterind=i
		i+=1
	player[ind][1], player[masterind][1]= player[masterind][1], player[ind][1]
	
	

#~~~~~~~~~~~~~~~~~~~~~~~~

def Startgame():
	global seltrack, players, x, y, playercount, ex, ey, celok, myind, submitted, hatrahagy, kx, ky
	rajz.grid(columnspan=12)
		
	for i in range(mennyi):
		rajz.create_line(i*koz, 0, i*koz, 700, fill=gray)
	for i in range(mennyi):
		rajz.create_line(0, i*koz, 700, i*koz, fill=gray)
	
	track=eval(open(seltrack, 'r').read())
	for line in track:
		if line[0]=='N':
			color="black"
		elif line[0]=='G':
			color=gray
		else:
			color=lightred
			for i in range(playercount):
				if players[i][1]==-1:
					x, y=setPlayer(i, line)
					myind=i
				else:
					setPlayer(i, line)
		rajz.create_line(line[1], line[2], line[3], line[4], width=4, fill=color)
		
	ex=x-koz
	ey=y
	a= x+(x-ex)
	b= y+(y-ey)
	celok=[[rajz.create_oval(a-r+(i*koz), b-r+(j*koz), a+r+(i*koz), b+r+(j*koz), outline=lightred) for j in range(-1, 2)] for i in range(-1, 2)]
	
	submit['text']='Take move'

	while not over:
		for i in range(playercount):
			ablak.update()
			if i==myind:
				for i in range(3):
					for j in range(3):
						navibuttons[i][j].grid( row=i+1, column=j, pady=10)
				submit.grid(row=1, column=3, columnspan=7)
				hatrahagy=False
				submitted=False
				while not submitted:
					ablak.update()
				hatrahagy=True
				a, b=rajz.coords(mycurln)[2], rajz.coords(mycurln)[3]
				a, b=a-(x+(x-ex)), b-(y+(y-ey))
				lepes(a, b)
				for i in range(3):
					for j in range(3):
						rajz.delete(celok[i][j])
				a= x+(x-ex)
				b= y+(y-ey)
				celok= [[rajz.create_oval( a-r+(i*koz), b-r+(j*koz), a+r+(i*koz), b+r+(j*koz), outline=lightred) for j in range(-1, 2)] for i in range(-1, 2)]
				for i in range(3):
					for j in range(3):
						navibuttons[i][j].grid_forget()
				submit.grid_forget()
			else:
				message['text']='Next player: \"'+players[i][0]+'\"'
				message.grid(padx=120, pady=40)
				ablak.update()
				sock.bind((myip, players[i][1]))
				data, addr=sock.recvfrom(1024)
				data=data.decode('utf-8')

############################
#Defining widgets

instruction=Label(ablak)
name=Entry(ablak)
submit=Button(text="submit", command=sub)

rajz=Canvas(width=700, height=700, bg='white')

functions=[[balfenn, balkoz, ballenn], [kozfenn, kozkoz, kozlenn], [jobbfenn, jobbkoz, jobblenn]]

savetrack=Button(text='Save track & return to menu', command=st)

cleartrack=Button(text='Clear track', command=ct)

normal=Button(text='Draw normal lines', command=normfunc)
grayzone=Button(text='Draw gray zone', command=grayzonefunc)
startingline=Button(text='Draw starting line', command=startinglinefunc)

navibuttons=[[Button(ablak, text='o', command=functions[j][i])for j in range(3)] for i in range(3)]

startbuttons=[]
startbuttons.append(Button(text='Create new TRACK', width=20, height=3, command=newtrack))
startbuttons.append(Button(text='Create new GAME', width=20, height=3, command=newgame))
startbuttons.append(Button(text='Join game', width=20, height=3, command=joingame))

list=Listbox(ablak)
jelszo=StringVar()
jelszolab=Label(ablak, textvariable=jelszo)

message=Label(ablak)

#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
#Start program 

for i in range(3):
	startbuttons[i].grid(padx=120, pady=30)
		
ablak.mainloop()
		
		
		
