# -*- coding: utf-8 -*-
import socket

#from serial import Serial
import subprocess
#import Adafruit_BMP.BMP085 as BMP085

import base64
import cv2
import zmq
from time import time

context = zmq.Context()
footage_socket = context.socket(zmq.PUB)
footage_socket.connect('tcp://localhost:5555')

camera = cv2.VideoCapture(0)

addr = '192.168.56.1'
port = int(open('port.txt', 'r').read())+1

########################################
#ser = Serial('/dev/ttyUSB0',9600)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#ipcim = input('Add meg a kezelőfelület IP címét: ')
#from control import running

while 1:
    #sock.sendto(ser.readline(), ('192.168.0.112', 5000))
    grabbed, frame = camera.read()  # grab the current frame
    frame = cv2.resize(frame, (480, 360))  # resize the frame
    encoded, buffer = cv2.imencode('.jpg', frame)
    jpg_as_text = base64.b64encode(buffer)
    footage_socket.send(jpg_as_text)
    footage_socket.send(str(time()))
    #sock.sendto(str(time()), (addr, port))
    
    '''voltage = subprocess.check_output(['/opt/vc/bin/vcgencmd', 'measure_volts core'])
    out_number = ''
    for ele in voltage:
        if (ele == '.' and '.' not in out_number) or ele.isdigit():
            out_number += ele
        elif out_number:
            break
    truevolt = float(out_number)
    if truevolt < :
         sock.sendto('BA', (ipcim, 5002))'''
    
    
    
