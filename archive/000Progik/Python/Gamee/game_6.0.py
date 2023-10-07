from tkinter import *
from math import *
from time import time
from random import *
#from keyboard import is_pressed

#############################
#Defining too many variables

#!!!!!!!!!!!!!---Nenyúljhozzá részleg---!!!!!!!!!!!!!!!

#~~~~~~~~~~~Setup~~~~~~~~~~~
timeborder=0.04

width = 700
height = 700
x, y = width/2, height/2
change=-90.0
point=[]

pressing=False
first=True
firewhenrelease=False
shield_active=False
eneadded=False
gotammo=False
shootnow=0
direction=0
score=0
multikill= [-1, 0]
shoots=[]
getpts=[]

try:
	best_score=int(open('best_score.txt', 'r').read())
except:
	best_score=0
	f=open('best_score.txt', 'w')
	f.write('0')
	f.close()
	
mode=2

#~~~~~~~~~~Design~~~~~~~~~~~
r=3 # töltények sugara
cr=40 # torony sugara
scr=25 # torony belső sugara
br=5 # piros bogyó sugara
d=br # lézer és célzóvonal vastagsága
kulso=500 # lézer külső sugara

gosmaller=90 # %ra csökk. az ene. p-ként
gosmperiod=35 # hányszor csökk.
delay=20 # lőtények esése közötti szünet
acc=250 # esés gyorsulása

rotate_shield=1.5 # pajzs forgása
reduce_shield=3 # pajzs csökkenése
shield_r=60 # pajzs sugara
width_shield=5 # pajzs vastagsága

color='red'
simplecolor='black'
ammo_ene_color='#ffffff'
def_ene_color='#00deff'
shield_basic_color='#005677'
outlinecolor='white'

multi=['double', 'triple', 'quadra', 'penta','hexa', 'hepta', 'octa', 'nona', 'deka']

#*****************************************
#@@@---Hozzányúlhatsz részleg---@@@

db=13# töltények száma
plus=7# lőtorony forgási sebesség

speed=3
fordindex=20
ford=0.1
enenum=40 # enemyk száma
point_pcs=10
enemy_pcs=0
ammoene=10 # golyós enemyk száma
defene=3 # pajzsos enemyk száma
enespeed=13# enemyk sebessége
spin=0.013# enemy körüljárási sebessége
startdist=500 # első enemy milyen korán jön
between=35 # enemyk közötti táv

#Ezekkel vicces játszani ;)
min_size=20 # enemyk mininum mérete
max_size=40 # enemyk maximum mérete

#############################
eredb=db
enespeed/=10
#############################
#Defining messy functions

def cd(which, i):  # cd = coord
	if db<=15: vmi=db
	else: vmi=15
	if not which: #tehát x coord
		return x+cos(radians(360*(i/vmi) -change))*cr
	else: #tehát y coord
		return y-sin(radians(360*(i/vmi) -change))*cr
		
def cdp(which, i, rad): # coord plus
	if db<=15: vmi=db
	
	else: vmi=db-15
	if not shootnow: chan=change+360/(db-15)/2
	else: chan=change
	if not which: #tehát x coord
		return x+cos(radians(360*(i/vmi) -chan))*rad
	else: #tehát y coord
		return y-sin(radians(360*(i/vmi) -chan))*rad
		
#~~~~~~~~~~~~~~~~~~~~~~~~~~
	
def rotate(dir):
	for d in dirbut:
		d.config(activeforeground='black')
	global pressing, direction
	direction=not dir
	pressing=True
		
def stop_rot():
	for d in dirbut:
		d.config(activeforeground='white')
	global pressing
	pressing=False
	
def eneinside(xy):
	if xy[0] >= 0-max_size and xy[0] <= width+max_size and xy[1] >= 0-max_size and xy[1] <= height+max_size:
		return True
	else: return False
	
def ng():
	global change, alive
	rajz.delete(ALL)
	newgamebut.grid_forget()
	change=-90.0
	setnewgame()
	alive=True
	
#~~~~~~~~~~~~~~~~~~~~~~~~~~
	
def fire():
	global shoots, alive, enedied, lab, shootnow, gotammo, score, multikill
	if db==1 or not alive:
		return 0
	shootnow=True
	shoots.append([rajz.create_line(cdp(0, 0, cr+d), cdp(1, 0, cr+d), cdp(0, 0, kulso), cdp(1, 0, kulso), fill='#ff0000', width=br), time()])
	shootnow=False
	
	dead=0
	for enemy in enemies:
		enexy=[x+cos(enemy[1]) *enemy[2], y-sin(enemy[1])*enemy[2]]
		diff=radians(change*-1) - enemy[1]
		if abs(sin(diff)*enemy[2]) < max_size and eneinside(enexy) and cos(diff)>0 and enemy[3]==1:
			enemy[3]=0
			if enemy[4]==simplecolor:
				score+=5
			elif enemy[4]==ammo_ene_color:
				score+=2
			else:
				score+=12
			gotammo=False
			dead+=1
	
	if dead>1:
		if multikill[0] != -1:
			rajz.delete(multikill[0])
		multikill = [rajz.create_text(x, 70, text=str(multi[dead-2]).upper()+'KILL', fill='yellow'), shoots[-1][1]]
		score+=dead*5
	rajz.itemconfig(scoreText, text=str(score))
	changepts(db-1)
	
#~~~~~~~~~~~~~~~~~~~~~~~~~~
	
def changepts(how):
	global point, db
	for pt in point:
		rajz.delete(pt)
	db=how
	if db<=15:
		point=[rajz.create_oval(coord(cd(0,i), cd(1,i), r), width=r*2, outline=outlinecolor) for i in range(db)]
	else: 
		point=[rajz.create_oval(coord(cd(0,i), cd(1,i), r), width=r*2, outline=outlinecolor) for i in range(15)]
		point+=[rajz.create_oval(coord(cdp(0,i,scr), cdp(1,i,scr), r), width=r*2, outline=outlinecolor) for i in range(db-15)]
			
	rad=br
	rajz.coords(point[0], coord(cd(0,0), cd(1,0), rad))
	rajz.itemconfig(point[0], outline=color, width=br*2)
	
#~~~~~~~~~~~~~~~~~~~~~~~~~~
	
def randdeg():
	return uniform(0, 2*pi)

"""def help(i, deg, enemy=None, min=min_size, max=max_size):
	r=radians(uniform(0, 90)+i*90)
	d=uniform(min, max)
	#alseg.append([r, d])
	if first:
		enedist=startdist
	else:
		enedist=enemy[2]
	enedeg=deg
	kx, ky= x+cos(enedeg)*enedist, y-sin(enedeg)* enedist
	a, b = cos(r)*d+kx, sin(r)*d+ky
	return [a, b]
	
def getshape(ind, d, min=min_size, max=max_size):
	product=[]
	if first:
		for i in range(4):
			product+=help(i, d, min, max)
	else:
		for i in range(4):
			product+=help(i, d, enemies[ind], min, max)
	return product"""
	
#~~~~~~~~~~~~~~~~~~~~~~~~~~
	
def get_point(x, y, i):
	r=uniform(0, pi*2/point_pcs)+i*pi*2/point_pcs
	d=uniform(min_size, max_size)
	a, b = cos(r)*d+x, sin(r)*d+y
	return [a, b]
	
def get_shape(x, y):
	return [get_point(x, y, i) for i in range(point_pcs)]
	
#~~~~~~~~~~~~~~~~~~~~~~~~~~

def calcDeg(Ln, start=0):
	def easy(x):
		if x >= 0: return 1
		elif x < 0: return -1
	def correct(x):
		if x<0: return 2*pi+x 
		else: return x
	try:
		c = (Ln[2]-Ln[0])/hypot(Ln[1]-Ln[3], Ln[0]-Ln[2])
		s = (Ln[3]-Ln[1])/hypot(Ln[1]-Ln[3], Ln[0]-Ln[2])
	except:
		c, s = 0, 0
	recovery=acos(c)*easy(s)-radians(start)
	dgc=acos(cos(recovery))
	elojel=sin(recovery)
	return correct(dgc*easy(elojel))
	
#~~~~~~~~~~~~~~~~~~~~~~~~~~

def out_of_range(x, y, i):
	if mode==1:
		return x<0 or x>width or y<0 or y>height
	elif mode==2:
		min_border= i/point_pcs*2*pi
		max_border=(i+1)/point_pcs*2*pi
		angle=calcDeg([kx, ky, x, y])
		return hypot(x-kx, y-ky)>=max_size or angle<=min_border or angle>=max_border

#~~~~~~~~~~~~~~~~~~~~~~~~~~

def move_enemy(enemy):
	rajz.tag_raise(enemy[0])
	rajz.coords(enemy[6], coord(width/2+cos(enemy[1])*enemy[2], height/2+sin(enemy[1])*enemy[2], max_size))
	points = [[rajz.coords(enemy[0])[i*2+j] for j in range(2)] for i in range(point_pcs)]
	new_points=[]
	directions=enemy[5]
	for i in range(point_pcs):
		x, y = points[i]
		x, y = x-cos(enemy[1])*enespeed, y-sin(enemy[1])*enespeed
		angle = directions[i]
		if out_of_range(x, y, i):
			directions[i]+=pi/2
			angle+=pi/2
		x, y = x+cos(angle)*speed, y+sin(angle)*speed
		new_points+=[x,y]
		if randint(0, 100)<fordindex:
			directions[i] += uniform(-ford, ford)
	rajz.coords(enemy[0], new_points)

#~~~~~~~~~~~~~~~~~~~~~~~~~~

def drawshield(arr):
	size, rot = arr
	rajz.itemconfig(shield[0], start=rot, extent=size)
	
#~~~~~~~~~~~~~~~~~~~~~~~~~~

def animation():
	global shield, lightshield, shield_active, multikill
	eneremove=[]
	rajz.itemconfig(textt, text=str(between))
	for enemy in enemies:
		if enemy[3]<1 and len(rajz.coords(enemy[0]))>0:
			enexy=[x+cos(enemy[1])*enemy[2], y-sin(enemy[1])*enemy[2]]
			if ((enemy[4]==simplecolor or enemy[4]==def_ene_color) and enemy[3] > -gosmperiod) or (enemy[4]==ammo_ene_color and enemy[3] > -gosmperiod/2):
				eneshape= [[rajz.coords(enemy[0])[2*j+i] for i in range(2)] for j in range(4)]
				enedegs=[calcDeg(enexy+eneshape[i]) for i in range(4)]
				eneptdists=[hypot(enexy[0]- eneshape[i][0], enexy[1]-eneshape[i][1])* gosmaller/100 for i in range(4)]
				def shape(i):
					return [enexy[0]+ cos(enedegs[i])* eneptdists[i], enexy[1]+ sin(enedegs[i])*eneptdists[i]]
				newshape=[]
				for i in range(4):
					newshape+=shape(i)
				rajz.coords(enemy[0], newshape)
				
				if enemy[3]==0 and enemy[4]==def_ene_color and shield[1] < 359:
					if not shield_active:
						lightshield=rajz.create_oval(coord(x, y, shield_r), width=width_shield, outline=shield_basic_color)
						rajz.tag_lower(lightshield)
					shield[1] = 359
					shield[2]=degrees(enemy[1])
					shield_active=True
				enemy[3]-=1
			else:
				enemy[3]=2
				if enemy[4]==ammo_ene_color:
					for i in range(randint(2, 5)):
						getpts.append([rajz.create_oval(enexy[0]-r, enexy[1]-r, enexy[0]+r, enexy[1]+r, width=r*2, outline=outlinecolor), -i*delay, time(), enemy[1]+pi, rajz.coords(enemy[0])[:2]])
				rajz.delete(enemy[0])
				eneremove.append(enemy)
				
		rem=[]
		for pt in getpts:
			t=pow(time()-pt[2], 2)
			npx, npy = pt[4][0]+ cos(pt[3])*acc*t, pt[4][1]-sin(pt[3])*acc*t
			pdist=hypot(x-npx, y-npy)
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
			
	for sh in shoots:
		kul=time()-sh[1]
		if kul <= 1:
			ertek=str(hex(int(255- 255*kul)))[2:]
			if len(ertek)==1:
				ertek='0'+ertek
			#rajz.itemconfig(sh[0], fill='#ff'+ertek+ertek)
			color='#'+ertek+'0000'
			color2="#"+2*ertek+'00'
			rajz.itemconfig(sh[0], fill=color)
			firebut.config(bg=color, activebackground=color)
			if multikill[1]==sh[1]:
				rajz.itemconfig(multikill[0], fill=color2)
		else:
			rajz.delete(sh[0])
			shoots.remove(sh)
			if multikill[0] != -1:
				rajz.delete(multikill[0])
				multikill[0] = -1

	if shield[1]>0:
		shield[1]-=reduce_shield
		shield[2]+=rotate_shield
		drawshield(shield[1:3])
	elif shield_active:
		shield[1]=0
		rajz.delete(lightshield)
		drawshield(shield[1:3])
		shield_active=False
		
	for ene in eneremove:
		enemies.remove(ene)

#~~~~~~~~~~~~~~~~~~~~~~~~~~
#For test purposes

def stop(arg):
	f=open('sth.txt', 'w')
	f.write(str(arg))
	f.close()
	while 1:
		pass
		
def coord(x, y, r):
	return [x-r, y-r, x+r, y+r]
		
#~~~~~~~~~~~~~~~~~~~~~~~~~~
		
def setnewgame():
	global centralline, deg, dist, enemies, first, shield, scoreText, score, change, alive, textt
	rajz.delete(ALL)
	newgamebut.grid_forget()
	change=-90.0
	alive=True
	first=True
	changepts(eredb)

	centralline=rajz.create_line(x, y, x, y-cr, fill='red', width=br-1)
	score=0
	scoreText=rajz.create_text(width/2, 15, text=str(score), fill=outlinecolor)
	textt=rajz.create_text(width/2, 50, fill=outlinecolor)

	#deg=[randdeg() for i in range(enenum)]
	#dist=[startdist+i*between for i in range(enenum)]
	#shuffle(dist)
	enemies=[]
	
	shield = [rajz.create_arc(coord(x, y, shield_r), extent=0, width=width_shield, outline=def_ene_color, style='arc'), 0, 0]

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def control():
	global change, firewhenrelease, alive
	if not alive:
		return 0
	if is_pressed('space'):
		firewhenrelease = True
	if not is_pressed('space') and firewhenrelease:
		fire()
		firewhenrelease=False
	if is_pressed('left_arrow'):
		change+=abs(plus)
		changepts(db)
		rajz.coords(centralline, x, y, cd(0, 0), cd(1, 0))
	if is_pressed('right_arrow'):
		change+=abs(plus)*-1
		changepts(db)
		rajz.coords(centralline, x, y, cd(0, 0), cd(1, 0))
	if is_pressed('n'):
		rajz.delete(ALL)
		change=90.0
		setnewgame()
		alive=True
		
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

#############################
#Getting program ready

ablak=Tk()
ablak.config(bg='black')

rajz=Canvas(width=width, height=height, bg=simplecolor, highlightthickness=0)
rajz.grid(columnspan=2)

dir=["Balra", "Jobbra"]
dirbut=[]
for i in range(2):
	dirbut.append(Button(text=dir[i], width=14, height=3, bg='black', fg='white', activebackground="black"))
	dirbut[i].grid(column=i, row=1)
	dirbut[i].bind('<ButtonPress-1>', lambda event, i=i: rotate(i))
	dirbut[i].bind('<ButtonRelease-1>', lambda event: stop_rot())

firebut=Button(text='FIRE!!!!', command=fire, width=20, height=3, bg='black', fg='white', activebackground='black', activeforeground="white")
firebut.grid(row=2, columnspan=2)

newgamebut=Button(text='New Game', command=setnewgame, width=20, height=3, bg='black', fg='white', activebackground='black', activeforeground='white')

alive=True
rogzit=time()

setnewgame()

#~~~~~~~~~Main loop~~~~~~~~~~~

# I know it's kinda ugly but... it works xd
# Actually now it looks better
"""
RÉGI STATISZTIKA: csinálj újat!
Alap várási idő: 0.02 sec
Iterációk 0.025 sec feletti idővel: 45%
Iterációk 0.03 sec feletti idővel: 14%
Iterációk 0.035 sec feletti idővel: 5%

Ebbe beleszámítandó az iterációnkénti
időellenőrzés
"""
circles=[]

while 1:
	while time()-rogzit < timeborder:
		pass
	rogzit=time()
	animation()
	ablak.update()
	
	if db<5 and not gotammo:
		randene=randint(0, len(enemies)-1)
		while enemies[randene][4] == def_ene_color or enemies[randene][3]<1:
			randene=randint(0, len(enemies)-1)
		enemies[randene][4]= ammo_ene_color
		rajz.itemconfig(enemies[randene][0], fill=ammo_ene_color)
		gotammo=True
		
	if between==0:
		first=True
		between=35
		if randint(0, 25)==0:
			enecolor=def_ene_color
		else:
			enecolor=simplecolor
		random_degrees=randdeg()
		kx, ky = x+cos(random_degrees)*startdist, y+sin(random_degrees)*startdist
		#circles.append(rajz.create_oval(coord(kx, ky, max_size), outline='red', fill='black'))
		enemies.append([rajz.create_polygon(get_shape(kx, ky), fill=enecolor, outline=outlinecolor), random_degrees, startdist, 1, enecolor, [uniform(0, 2*pi) for i in range(point_pcs)], rajz.create_oval(coord(kx, ky, max_size), outline='red', fill='black')])
		
		first=False
	between-=1
	
	if pressing:
		if direction:
			plus=abs(plus)*-1
		else:
			plus=abs(plus)
		change+=plus
		changepts(db)
		rajz.coords(centralline, 350, 350, cd(0, 0), cd(1, 0))
		
	h=0
	for enemy in enemies:
		if enemy[2]-max_size/2<shield_r and shield_active and enemy[3]==1:
			enemy[3]=0
		elif enemy[2]<cr:
			alive=False
			break
		elif enemy[3]==1:
			enemy[2] -= enespeed
			if enemy[4]==ammo_ene_color:
				enemy[1]+=spin
			elif enemy[4]==def_ene_color:
				enemy[1] += spin*2
			kx, ky = x+cos(enemy[1])*enemy[2],y+sin(enemy[1])*enemy[2]
			move_enemy(enemy)
			#rajz.coords(enemy[0], get_shape())
			#rajz.coords(enemy[0], getshape(h, enemy[1]))
		h+=1
	
	if not alive:
		rajz.delete(ALL)
		rajz.create_text(x, y, text='GAME OVER', fill=outlinecolor)
		if score <= best_score:
			rajz.create_text(x, y+80, text='Score: '+str(score)+'\nBest score: '+str(best_score), fill=outlinecolor)
		else:
			rajz.create_text(x, y+80, text='NEW BEST SCORE!!!!!', fill=outlinecolor)
			rajz.create_text(x, y+130, text=str(score), fill=outlinecolor)
			f=open('best_score.txt', 'w')
			f.write(str(score))
			f.close()
		newgamebut.grid(row=3, columnspan=2)
		getpts=[]