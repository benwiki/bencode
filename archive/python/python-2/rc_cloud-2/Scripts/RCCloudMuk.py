# -*- coding: utf-8 -*-
import os
os.system('sudo systemctl start pigpiod')
import socket
import pigpio
pi = pigpio.pi()

SER = 6
SER2 = 12

pi.set_mode(SER, pigpio.OUTPUT)
pi.set_mode(SER2, pigpio.OUTPUT)

myip = ([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0])

UDP_IP = str(myip)
UDP_PORT = 5007

import subprocess
#subprocess.Popen(["python2", "python /home/pi/Documents/Scripts/irany.py"], shell = True)
#subprocess.Popen(["python2", "python /home/pi/Documents/Scripts/kuld.py"], shell = True)

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
 
sock.bind((UDP_IP, UDP_PORT))

pi.set_servo_pulsewidth(SER, 1560)
pi.set_servo_pulsewidth(SER2, 1412)

print (myip)
data = ''
szam = 0
c = 0

while data!='close':
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    f = open('udpdata.txt', 'w')
    f.write(data)
    f.close()
    i = 0
    e = 0
    com = ''
    if data[0] == 'P':
        p = open('powa.txt', 'w')
        h = open('hori.txt', 'w')
        #############################################
        i = 1
        while data[i].isdigit() or data[i] == '-':
            i = i + 1
        com = ''
        for n in range(1, i):
            com = com + data[n]
        p.write(com)
        p.close()
        #############################################
        i = i + 1
        e = i
        while data[i].isdigit() or data[i] == '-':
            i = i + 1
        com = ''
        for n in range(e, i):
            com = com + data[n]
        h.write(com)
        h.close()
        #############################################
        i = i + 1
        e = i
        while data[i].isdigit() or data[i] == '-':
            i = i + 1
        com = ''
        for n in range(e, i):
            com = com + data[n]
        c = int(com)
        ser = 1560+(890*c)/100
        ser2 = 1412.5-(890*c)/100
        pi.set_servo_pulsewidth(SER, ser)
        pi.set_servo_pulsewidth(SER2, ser2)
   
    if data[0] == 'G':
        i = 1
        while data[i].isdigit() or data[i] == '.':
            i = i + 1
        com = ''
        for n in range(1, i):
            com = com + data[n]
        print (com)
 
        i = i+1
        e = i
        while data[i].isdigit() or data[i] == '.':
            i = i + 1
        com = ''
        for n in range(e, i):
            com = com + data[n]
        print (com)
    if data[0] == 'S':
        print ('STOPPING EVERYTHING')
        pi.set_servo_pulsewidth(SER, 1560)
        pi.set_servo_pulsewidth(SER2, 1412)
sock.close()

