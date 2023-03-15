# -*- coding: utf-8 -*-
from Tkinter import *

mid1 = True
mid2 = True
stop = True

ctrl = Tk()
ctrl.title("The RCCloud's Manual")

def ell():
    if mid1 == True and mid2 == True and stop == True:
        StAllLab['text'] = "Levitating"
    elif (mid2 == False or mid1 == False) and stop == True:
        StAllLab['text'] = "Calibrating"
    elif stop == False:
        StAllLab['text'] = "MOVING"
        
def GoUp():
    global mid2, mid1
    Mivan2["text"] = "Going UP"
    mid2=False
    ell();
    
def GoLeft():
    global mid2, mid1
    Mivan["text"] = "Going LEFT"
    mid1=False
    ell();
    
def GoRight():
    global mid2, mid1
    Mivan["text"] = "Going RIGHT"
    mid1=False
    ell();
    
def GoDown():
    global mid2, mid1
    Mivan2["text"] = "Going DOWN"
    mid2=False
    ell();

def Levi():
    global mid1, mid2, stop
    mid1=mid2=stop=True
    Mivan["text"] = "MID"
    Mivan2['text'] = "MID"
    StAllLab['text'] = "Levitating"
    EngLab['text'] = 'STANDBY'

def Hormid():
    global mid2, mid1
    Mivan2['text'] = 'MID'
    mid2 = True
    ell();
    
def Vermid():
    global mid2, mid1
    Mivan['text'] = 'MID'
    mid1 = True
    ell();

def StartEng():
    global stop
    EngLab['text'] = 'MOVING'
    stop = False
    ell();

def StopEng():
    global stop
    EngLab['text']= 'STANDBY'
    stop = True
    ell();

def SwitchChange():
    Left.grid_forget()
    Right.grid_forget()
    Change.grid_forget()
    Mivan.grid_forget()
    Up.grid_forget()
    Down.grid_forget()
    eleg.grid_forget()
    StAllLab.grid_forget()
    Mivan2.grid_forget()
    StHor.grid_forget()
    StVer.grid_forget()
    ctrl.title("The RCCloud's Auto")
    Change['text'] = "Switch to MANUAL"
    Change['command'] = Switch2
    Change.grid()
    

def Switch2():
    Change.grid_forget()
    ctrl.title("The RCCloud's Manual")
    Change['text'] = "Switch to AUTO"
    Change['command'] = SwitchChange
    Change.grid(row=0,column=0)
    Mivan.grid(row = 2,column=1)
    Left.grid(row=2,column=0)
    Right.grid(row=2,column=2)
    Up.grid(row=3,column=0)
    Down.grid(row=3,column=2)
    eleg.grid(row=1,column=0)
    StAllLab.grid(row=1,column=1)
    Mivan2.grid(row = 3,column=1)
    StVer.grid(row=3, column=3)
    StHor.grid(row=2, column=3)

EngLab = Label(ctrl, text="STANDBY", height =7 , width = 11)
EngLab.grid(row=4, column=1)

EngStart = Button (ctrl, text= 'FORWARD', command = StartEng, height = 7, width = 11)
EngStart.grid(row = 4, column = 0)

EngStop = Button (ctrl, text= 'STOP', command = StopEng, height = 7, width = 11)
EngStop.grid(row = 4, column = 2)

StAllLab = Label(ctrl, text = 'Levitating', width = 10)
StAllLab.grid(row=1,column=1)

Mivan2 = Label(ctrl, text = "MID", width = 10)
Mivan2.grid(row = 3,column=1)

Mivan = Label(ctrl, text = "MID", width = 10)
Mivan.grid(row = 2,column=1)

Change = Button(ctrl, text='Switch to AUTO', command=SwitchChange, height = 4, width = 11)
Change.grid(row=0,column=0)

Left = Button(ctrl, text='LEFT', command = GoLeft, height = 7, width = 11)
Left.grid(row=2,column=0)

Right = Button(ctrl, text='RIGHT', command = GoRight, height = 7, width = 11)
Right.grid(row=2,column=2)

Down = Button(ctrl, text='DOWN', command = GoDown, height = 7, width = 11)
Down.grid(row=3,column=2)

Up = Button(ctrl, text='UP', command = GoUp, height = 7, width = 11)
Up.grid(row=3,column=0)

eleg = Button(ctrl, text='STOP!', command = Levi, height = 7, width = 11)
eleg.grid(row=1,column=0)

StHor = Button(ctrl, text='MID', command = Hormid, height = 7, width = 11)
StHor.grid(row=3, column=3)

StVer = Button(ctrl, text='MID', command = Vermid, height = 7, width = 11)
StVer.grid(row=2, column=3)

ctrl.mainloop()














