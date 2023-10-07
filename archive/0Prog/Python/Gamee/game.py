from tkinter import *
from math import *
from time import time
from random import *

##############################
#Defining too many variables

#!!!!!!!!!!!!!---Nenyúljhozzá részleg---!!!!!!!!!!!!!!!

#~~~~~~~~~~~Setup~~~~~~~~~~~
timeborder=0.04

x, y = 350, 350
change=90.0
point=[]

pressing=False
first=True
shootnow=0
direction=0
shoots=[]
getpts=[]

#~~~~~~~~~~Design~~~~~~~~~~~
r=3
cr=40
scr=25
br=5
d=br
kulso=500

gosmaller=90
gosmperiod=35
delay=60
acc=250

color='red'
simplecolor='black'
fullcolor='#ffffff'
outlinecolor='white'


#*****************************************
#@@@---Hozzányúlhatsz részleg---@@@

db=12# töltények száma
plus=7# lőtorony forgási sebesség

enenum=50 # enemyk száma
blackene=17 # fekete enemyk száma
enespeed=12 # enemyk sebessége
startdist=500 # első enemy milyen korán jön
between=40# enemyk közötti táv

#Ezekkel vicces játszani ;)
min=20# enemyk mininum mérete
max=40 # enemyk maximum mérete

##############################
eredb=db
enespeed/=10
##############################
#Defining messy functions

def cd(which, i):
	if db<=15: vmi=db
	else: vmi=15
	if not which: #tehát x coord
		return x+cos(radians(360*(i/vmi) -change))*cr
	else: #tehát y coord
		return y+sin(radians(360*(i/vmi) -change))*cr
		
def cdp(which, i, rad):
	if db<=15: vmi=db
	else: vmi=db-15
	if not shootnow: chan=change+360/(db-15)/2
	else: chan=change
	if not which: #tehát x coord
		return x+cos(radians(360*(i/vmi) -chan))*rad
	else: #tehát y coord
		return y+sin(radians(360*(i/vmi) -chan))*rad
		
#~~~~~~~~~~~~~~~~~~~~~~~~~~

def rotate(dir):
	global pressing, direction
	direction=dir
	pressing=True
		
def stop_rot():
	global pressing
	pressing=False
	
def eneinside(xy):
	if xy[0] >= 0-max and xy[0] <= 700+max and xy[1] >= 0-max and xy[1] <= 700+max:
		return True
	else: return False
	
def ng():
	global change, alive
	rajz.delete(ALL)
	change=90.0
	setnewgame()
	alive=True
	
#~~~~~~~~~~~~~~~~~~~~~~~~~~
	
def fire():
	global shoots, alive, enedied, lab, shootnow
	if db==1 or not alive:
		return 0
	shootnow=True
	shoots.append([rajz.create_line(cdp(0, 0, cr+d), cdp(1, 0, cr+d), cdp(0, 0, kulso), cdp(1, 0, kulso), fill='#ff0000', width=br), time()])
	shootnow=False
	
	for enemy in enearr:
		enexy=[350+cos(enemy[1]) *enemy[2], 350+sin(enemy[1])*enemy[2]]
		diff=radians(change*-1) - enemy[1]
		if abs(sin(diff)*enemy[2])< (min+max)/2 and eneinside(enexy) and cos(diff)>0 and enemy[3]==1:
			enemy[3]=0
			
	changepts(db-1)
	
#~~~~~~~~~~~~~~~~~~~~~~~~~~
	
def changepts(how):
	global point, db
	for pt in point:
		rajz.delete(pt)
	db=how
	if db<=15:
		point=[rajz.create_oval(cd(0, i)-r, cd(1, i)-r, cd(0, i)+r, cd(1, i)+r, width=r, outline=outlinecolor) for i in range(db)]
	else: 
		point=[rajz.create_oval(cd(0, i)-r, cd(1, i)-r, cd(0, i)+r, cd(1, i)+r, width=r, outline=outlinecolor) for i in range(15)]
		point+=[rajz.create_oval(cdp(0, i, scr)-r, cdp(1, i, scr)-r, cdp(0, i, scr)+r, cdp(1, i, scr)+r, width=r, outline=outlinecolor) for i in range(db-15)]
			
	rad=br
	rajz.coords(point[0], cd(0, 0)-rad, cd(1, 0)-rad, cd(0, 0)+rad, cd(1, 0)+rad)
	rajz.itemconfig(point[0], outline=color, width=br)
	
#~~~~~~~~~~~~~~~~~~~~~~~~~~
	
def randdeg():
	return uniform(0, 2*pi)

def help(i):
	global min, max
	r=radians(uniform(0, 90)+i*90)
	d=uniform(min, max)
	#alseg.append([r, d])
	enedeg=deg[ind]
	if first:
		enedist=dist[ind]
	else:
		enedist=enearr[ind][2]
	kx, ky= x+cos(enedeg)*enedist, y+sin(enedeg)* enedist
	a, b = cos(r)*d+kx, sin(r)*d+ky
	return [a, b]
	
def getshape(index):
	global ind
	ind=index
	return help(0)+help(1)+help(2)+help(3)
	
#~~~~~~~~~~~~~~~~~~~~~~~~~~

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
	try:
		c = (Ln[2]-Ln[0])/hypot(Ln[1]-Ln[3], Ln[0]-Ln[2])
		s = (Ln[3]-Ln[1])/hypot(Ln[1]-Ln[3], Ln[0]-Ln[2])
	except:
		c, s = 0, 0
	recovery=acos(c)*easy(s)-radians(start)
	dgc=acos(cos(recovery))
	elojel=sin(recovery)
	return dgc*easy(elojel)

#~~~~~~~~~~~~~~~~~~~~~~~~~~

def animation():
	for enemy in enearr:
		if enemy[3]<1 and len(rajz.coords(enemy[0]))>0:
			enexy=[350+cos(enemy[1]) *enemy[2], 350+sin(enemy[1])*enemy[2]]
			if (enemy[4]==simplecolor and enemy[3] > -gosmperiod) or (enemy[4]==fullcolor and enemy[3] > -gosmperiod/2):
				eneshape= [[rajz.coords(enemy[0])[2*j+i] for i in range(2)] for j in range(4)]
				enedegs=[calcDeg(0, enexy+eneshape[i]) for i in range(4)]
				eneptdists=[hypot(enexy[0]- eneshape[i][0], enexy[1]-eneshape[i][1])* gosmaller/100 for i in range(4)]
				def shape(i):
					return [enexy[0]+ cos(enedegs[i])* eneptdists[i], enexy[1]+ sin(enedegs[i])*eneptdists[i]]
				newshape=[]
				for i in range(4):
					newshape+=shape(i)
				rajz.coords(enemy[0], newshape)
				enemy[3]-=1
			else:
				rajz.coords(enemy[0], enexy+ enexy+enexy+enexy)
				enemy[3]=2
				if enemy[4]==fullcolor:
					for i in range(randint(2, 5)):
						getpts.append([ rajz.create_oval(enexy[0]-r, enexy[1]-r, enexy[0]+r, enexy[1]+r, width=r, outline=outlinecolor), -i*delay, time(), enemy[1]+pi, rajz.coords(enemy[0])[:2]])
		
		rem=[]
		if len(getpts)>0:
			for pt in getpts:
				t=pow(time()-pt[2], 2)
				npx, npy = pt[4][0]+ cos(pt[3])*acc*t, pt[4][1]+sin(pt[3])*acc*t
				pdist=hypot(350-npx, 350-npy)
				if pt[1]<0:
					pt[1]+=1
					pt[2]=time()
				elif pdist > cr:
					rajz.coords(pt[0], npx-r, npy-r, npx+r, npy+r)
				else:
					changepts(db+1)
					rem.append(pt)
					rajz.delete(pt[0])
			for item in rem:
				getpts.remove(item)

#~~~~~~~~~~~~~~~~~~~~~~~~~~
#For test purposes

def stop(arg):
	f=open('sth.txt', 'w')
	f.write(str(arg))
	f.close()
	while 1:
		pass
		
#~~~~~~~~~~~~~~~~~~~~~~~~~~
		
def setnewgame():
	global centralline, deg, dist, enearr, first
	first=True
	changepts(eredb)

	centralline=rajz.create_line(350, 350, 350, 350-cr, fill='red', width=4)

	deg=[randdeg() for i in range(enenum)]
	dist=[startdist+i*between for i in range(enenum)]
	shuffle(dist)
	enearr=[[rajz.create_polygon( getshape(i), fill=simplecolor, outline=outlinecolor), deg[i],dist[i], 1, simplecolor] for i in range(enenum)]
	for i in range(blackene):
		enearr[i][4]=fullcolor
		rajz.itemconfig(enearr[i][0], fill=fullcolor)
	first=False
				
"""hatar1=2
hatar2=2

def mozgat():
	global alak
	for i in range(4):
		r=alseg[i][0]+uniform(-hatar1, hatar1)
		d=alseg[i][1]+uniform(-hatar2, hatar2)
		if r>90+i*90:
			r=90+i*90
		elif r<i*90:
			r=i*90
		if d < min:
			d=min
		elif d > max:
			d=max
		a, b = cos(r)*d+x, sin(r)*d+y
		alak[i][0]=a
		alak[i][1]=b"""

##############################
#Getting program ready

ablak=Tk()

rajz=Canvas(width=700, height=700, bg=simplecolor)
rajz.grid(columnspan=2)

dir=["Balra", "Jobbra"]
dirbut=[]
for i in range(2):
	dirbut.append(Button(text=dir[i], width=14, height=3))
	dirbut[i].grid(column=i, row=1)
	dirbut[i].bind('<ButtonPress-1>', lambda event, i=i: rotate(i))
	dirbut[i].bind('<ButtonRelease-1>', lambda event: stop_rot())

firebut=Button(text='FIRE!!!!', command=fire, width=20, height=3)
firebut.grid(row=2, columnspan=2)

newgamebut=Button(text='New Game', command=ng, width=20, height=3)
newgamebut.grid(row=3, columnspan=2)

alive=True
rogzit=time()
lab=Label()
lab.grid(columnspan=2)

setnewgame()

#~~~~~~~~~Main loop~~~~~~~~~~~

# I know it's very ugly but... it works xd
"""
RÉGI STATISZTIKA: csinálj újat!
Alap várási idő: 0.02 sec
Iterációk 0.025 sec feletti idővel: 45%
Iterációk 0.03 sec feletti idővel: 14%
Iterációk 0.035 sec feletti idővel: 5%

Ebbe beleszámítandó az iterációnkénti
időellenőrzés
"""
while 1:
	while time()-rogzit < timeborder:
		pass
	rogzit=time()
	animation()
	ablak.update()
	if len(shoots)!=0:
		for sh in shoots:
			kul=time()-sh[1]
			if kul <= 1:
				ertek=str(hex(int(255- 255*kul)))[2:]
				if len(ertek)==1:
					ertek='0'+ertek
				#rajz.itemconfig(sh[0], fill='#ff'+ertek+ertek)
				rajz.itemconfig(sh[0], fill='#'+ertek+'0000')
			else:
				rajz.delete(sh[0])
				shoots.remove(sh)
	if pressing:
		if direction:
			plus=abs(plus)*-1
		else:
			plus=abs(plus)
		change+=plus
		for i in range(db):
			if i==0: rad=br
			else: rad=r
			if db<=15:
				rajz.coords(point[i], cd(0, i)-rad, cd(1, i)-rad, cd(0, i)+rad, cd(1, i)+rad)
			else:
				if i<=14:
					rajz.coords(point[i], cd(0, i)-rad, cd(1, i)-rad, cd(0, i)+rad, cd(1, i)+rad)
				else:
					rajz.coords(point[i], cdp(0, i, scr)-rad, cdp(1, i, scr)-rad, cdp(0, i, scr)+rad, cdp(1, i, scr)+rad)
		rajz.coords(centralline, 350, 350, cd(0, 0), cd(1, 0))
	
	h=0
	for enemy in enearr:
		if enemy[2]<cr:
			alive=False
			break
		elif enemy[3]==1:
			enemy[2] -= enespeed
			rajz.coords(enemy[0], getshape(h))
		h+=1
	if not alive:
		rajz.delete(ALL)
		rajz.create_text(350, 350, text='GAME OVER', fill=outlinecolor)
