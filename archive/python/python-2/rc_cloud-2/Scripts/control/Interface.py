# -*- coding: cp1250 -*-
from tkinter import *
from random import *
from math import *
from time import time
import socket
from keyboard import is_pressed
from PIL import Image, ImageTk
import sys

import cv2
import zmq
import base64
import numpy as np

context = zmq.Context()
footage_socket = context.socket(zmq.SUB)
footage_socket.bind('tcp://*:5555')
footage_socket.setsockopt_string(zmq.SUBSCRIBE, np.unicode(''))

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

myip = '192.168.56.1'
port = int(open('port.txt', 'r').read())

sock2 = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock2.bind((myip, port+1))

#Változók~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

slidespeed = 1
horval, verval, powval= 0, 0, 0

#Függvények~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


#Setup~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
ablak = Tk()

horscale = Scale(label='Horizontal', from_= -100, to=100, length=500, width=20, orient=HORIZONTAL)
verscale = Scale(label='Vertical', from_= 100, to=-100, length=500, width=20, orient=VERTICAL)
powerscale = Scale(label='Power', from_= 100, to=-100, length=500, width=20, orient=VERTICAL)
horscale.pack()
powerscale.pack(side=LEFT)
verscale.pack(side=LEFT)

video = Label()
video.pack(side=LEFT)
timelab = Label()
timelab.pack(side=TOP)

def close():
    sock.sendto('close', (myip, port))
    ablak.destroy()

closebutton = Button(text='Close program', width=50, height=3, command=close)
closebutton.pack(side=LEFT)

horval, verval, powval= elozo = horscale.get(), verscale.get(), powerscale.get()

while 1:
    try:
        frame = footage_socket.recv_string()
        img = base64.b64decode(frame)
        npimg = np.fromstring(img, dtype=np.uint8)
        source = cv2.imdecode(npimg, 1)
        source = cv2.cvtColor(source, cv2.COLOR_BGR2RGB)
        render = ImageTk.PhotoImage(Image.fromarray(source))
        video.config(image=render)
        #cv2.imshow("Stream", source)
        #cv2.waitKey(1)
    except:
        pass
    #t, addr = sock2.recvfrom(1024)
    t = footage_socket.recv_string()
    timelab['text'] = time()-float(t)

    if is_pressed('6') and horval<100:
        horval += slidespeed
        horscale.set(horval)
    if is_pressed('4') and horval>-100:
        horval -= slidespeed
        horscale.set(horval)
    if is_pressed('8') and verval<100:
        verval += slidespeed
        verscale.set(verval)
    if is_pressed('2') and verval>-100:
        verval -= slidespeed
        verscale.set(verval)
    if is_pressed('7') and powval<100:
        powval += slidespeed
        powerscale.set(powval)
    if is_pressed('1') and powval>-100:
        powval -= slidespeed
        powerscale.set(powval)
    if is_pressed('5'):
        horval, verval, powval= 0, 0, 0
        horscale.set(horval)
        verscale.set(verval)
        powerscale.set(powval)

    if horscale.get()!= elozo[0] or verscale.get()!=elozo[1] or powerscale.get()!=elozo[2]:
        data = 'P'+str(powval)+'H'+str(horval)+'V'+str(verval)+'T'
        #print data
        sock.sendto(data, (myip, port))
    else:
        sock.sendto('N', (myip, port))

    horval, verval, powval= elozo = horscale.get(), verscale.get(), powerscale.get()
    
    ablak.update()
