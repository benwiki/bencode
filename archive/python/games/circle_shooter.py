from tkinter import *
from math import *
from time import time
from random import *
from keyboard import is_pressed

##############################
#Defining too many variables

#!!!!!!!!!!!!!---Nenyúljhozzá részleg---!!!!!!!!!!!!!!!

#~~~~~~~~~~~Setup~~~~~~~~~~~
timeborder=0.04

width = 1500
height = 650
x, y = width/2, height/2
change=90.0
point=[]

pressing=False
first=True
firewhenrelease=False
shootnow=0
direction=0
shoots=[]
getpts=[]

#~~~~~~~~~~Design~~~~~~~~~~~
r=1
cr=20
scr=10
br=2
d=br
kulso=5000

gosmaller=90
gosmperiod=35
delay=60
acc=250

reduce_shield=2
rotate_shield=3
shield_r=40
width_shield=3

color='red'
simplecolor='black'
ammo_ene_color='#ffffff'
def_ene_color='#00deff'
outlinecolor='white'


#*****************************************
#@@@@@@@@@---Hozzányúlhatsz részleg---@@@@@@@@@

db=13# töltények száma
plus=5.5# lőtorony forgási sebesség

enenum=40 # enemyk száma
ammoene=12 # golyós enemyk száma
defene=3 # pajzsadó enemyk száma
enespeed=40 # enemyk sebessége
startdist=700 # első enemy milyen korán jön
between=35# enemyk közötti táv

#Ezekkel vicces játszani ;)
ene_min_r=40# enemyk mininum mérete
ene_max_r=50 # enemyk maximum mérete

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

def coord(x, y, r):
    return [x-r, y-r, x+r, y+r]

def rotate(dir):
    global pressing, direction
    direction=dir
    pressing=True

def eneinside(xy):
    if xy[0] >= 0-ene_max_r and xy[0] <= width+ene_max_r and xy[1] >= 0-ene_max_r and xy[1] <= height+ene_max_r:
        return True
    else: return False

#~~~~~~~~~~~~~~~~~~~~~~~~~~

def fire():
    global shoots, alive, enedied, lab, shootnow
    if db==1 or not alive:
        return 0
    shootnow=True
    shoots.append([rajz.create_line(cdp(0, 0, cr+d), cdp(1, 0, cr+d), cdp(0, 0, kulso), cdp(1, 0, kulso), fill='#ff0000', width=br), time()])
    shootnow=False

    for enemy in enearr:
        enexy=[x+cos(enemy[1]) *enemy[2], y+sin(enemy[1])*enemy[2]]
        diff=radians(change*-1) - enemy[1]
        if abs(sin(diff)*enemy[2])< (ene_min_r+ene_max_r)/2 and eneinside(enexy) and cos(diff)>0 and enemy[3]==1:
            enemy[3]=0

    changepts(db-1)

#~~~~~~~~~~~~~~~~~~~~~~~~~~

def changepts(how):
    global point, db
    for pt in point:
        rajz.delete(pt)
    db=how
    if db<=15:
        point=[rajz.create_oval(cd(0, i)-r, cd(1, i)-r, cd(0, i)+r, cd(1, i)+r, width=r*2, outline=outlinecolor) for i in range(db)]
    else:
        point=[rajz.create_oval(cd(0, i)-r, cd(1, i)-r, cd(0, i)+r, cd(1, i)+r, width=r*2, outline=outlinecolor) for i in range(15)]
        point+=[rajz.create_oval(cdp(0, i, scr)-r, cdp(1, i, scr)-r, cdp(0, i, scr)+r*2, cdp(1, i, scr)+r, width=r*2, outline=outlinecolor) for i in range(db-15)]

    rad=br
    rajz.coords(point[0], cd(0, 0)-rad, cd(1, 0)-rad, cd(0, 0)+rad, cd(1, 0)+rad)
    rajz.itemconfig(point[0], outline=color, width=br*2)

#~~~~~~~~~~~~~~~~~~~~~~~~~~

def randdeg():
    return uniform(0, 2*pi)

def help(i):
    global ene_min_r, ene_max_r
    r=radians(uniform(0, 90)+i*90)
    d=uniform(ene_min_r, ene_max_r)
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

def drawshield(arr):
    size, rot = arr
    rajz.itemconfig(shield[0], start=rot, extent=size)
##    a, b = cos(radians(rot)), -sin(radians(rot))
##    c, d = cos(radians(rot+size)), -sin(radians(rot+size))
##    rajz.coords(helpline1, x+a*shield_r, y+b*shield_r, x+a*shield_r*2, y+b*shield_r*2)
##    rajz.coords(helpline2, x+c*shield_r, y+d*shield_r, x+c*shield_r*2, y+d*shield_r*2)

#~~~~~~~~~~~~~~~~~~~~~~~~~~

def animation():
    global shield
    for enemy in enearr:
        if enemy[3]<1 and len(rajz.coords(enemy[0]))>0:
            enexy=[x+cos(enemy[1])*enemy[2], y+sin(enemy[1])*enemy[2]]
            if ((enemy[4]==simplecolor or enemy[4]==def_ene_color) and enemy[3] > -gosmperiod) or (enemy[4]==ammo_ene_color and enemy[3] > -gosmperiod/2):
                eneshape= [[rajz.coords(enemy[0])[2*j+i] for i in range(2)] for j in range(4)]
                enedegs=[calcDeg(0, enexy+eneshape[i]) for i in range(4)]
                eneptdists=[hypot(enexy[0]- eneshape[i][0], enexy[1]-eneshape[i][1])* gosmaller/100 for i in range(4)]
                def shape(i):
                    return [enexy[0]+ cos(enedegs[i])* eneptdists[i], enexy[1]+ sin(enedegs[i])*eneptdists[i]]
                newshape=[]
                for i in range(4):
                    newshape+=shape(i)
                rajz.coords(enemy[0], newshape)

                if enemy[4]==def_ene_color and enemy[3] == 0:
                    if shield[1] < 359:
                        shield[1] = 359
                enemy[3]-=1
            else:
                rajz.coords(enemy[0], enexy+enexy+enexy+enexy)
                enemy[3]=2
                if enemy[4]==ammo_ene_color:
                    for i in range(randint(2, 5)):
                        getpts.append([rajz.create_oval(enexy[0]-r, enexy[1]-r, enexy[0]+r, enexy[1]+r, width=r*2, outline=outlinecolor), -i*delay, time(), enemy[1]+pi, rajz.coords(enemy[0])[:2]])

        rem=[]
        for pt in getpts:
            t=pow(time()-pt[2], 2)
            npx, npy = pt[4][0]+ cos(pt[3])*acc*t, pt[4][1]+sin(pt[3])*acc*t
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
            rajz.itemconfig(sh[0], fill='#'+ertek+'0000')
        else:
            rajz.delete(sh[0])
            shoots.remove(sh)

    if shield[1]>0:
        shield[1]-=reduce_shield
        shield[2]+=rotate_shield
        drawshield(shield[1:3])

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
    global centralline, deg, dist, enearr, first, shield, helpline1, helpline2
    first=True
    changepts(eredb)

    centralline=rajz.create_line(x, y, x, y-cr, fill='red', width=br-1)

    deg=[randdeg() for i in range(enenum)]
    dist=[startdist+i*between for i in range(enenum)]
    shuffle(dist)
    enearr=[[rajz.create_polygon(getshape(i), fill=simplecolor, outline=outlinecolor), deg[i], dist[i], 1, simplecolor] for i in range(enenum)]
    for i in range(ammoene):
        enearr[i][4]=ammo_ene_color
        rajz.itemconfig(enearr[i][0], fill=ammo_ene_color)
    for i in range(ammoene, ammoene+defene):
        enearr[i][4]=def_ene_color
        rajz.itemconfig(enearr[i][0], fill=def_ene_color)
    first=False

##    helpline1 = rajz.create_line(0,0,0,0, fill=def_ene_color)
##    helpline2 = rajz.create_line(0,0,0,0, fill=def_ene_color)
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

def defended(deg):
    deg = degrees(deg)
    st, ex = shield[1:3]
    st = degrees(radians(st))
    if st+ex > 360:
        if deg > st or deg < st+ex-360:
            rajz.create_text(st+ex-360, 10, text=str(st+ex-360), fill='white')
            return 1
        else: return 0
    else:
        if deg > st and deg < st+ex:
            rajz.create_text(st+ex, 10, text=str(st+ex), fill='white')
            return 1
        else: return 0

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
        if d < ene_min_r:
            d=ene_min_r
        elif d > ene_max_r:
            d=ene_max_r
        a, b = cos(r)*d+x, sin(r)*d+y
        alak[i][0]=a
        alak[i][1]=b"""

##############################
#Getting program ready

ablak=Tk()

rajz=Canvas(width=width, height=height, bg=simplecolor)
rajz.pack()

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

while 1:
    while time()-rogzit < timeborder:
        pass
    rogzit=time()
    control()
    animation()
    #ablak.update_idletasks()
    ablak.update()
    h=0
    for enemy in enearr:
        if enemy[3]==1 and enemy[2]-ene_min_r/2 < shield_r and defended(enemy[2]):
            enemy[3]=0
        elif enemy[2]-ene_min_r/2 < cr:
            alive=False
            break
        elif enemy[3]==1:
            enemy[2] -= enespeed
            rajz.coords(enemy[0], getshape(h))
        h+=1
    if not alive:
        rajz.delete(ALL)
        rajz.create_text(x, y, text='GAME OVER', fill=outlinecolor)
