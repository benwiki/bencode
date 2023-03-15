# -*- coding: utf-8 -*-
import os
##os.system('sudo systemctl start pigpiod')
import socket
##import RPi.GPIO as GPIO
##import pigpio
##pi = pigpio.pi()

from time import time

##import picamera
##cam = picamera.PiCamera()

SER = 6
SER2 = 12

##pi.set_mode(SER, pigpio.OUTPUT)
##pi.set_mode(SER2, pigpio.OUTPUT)

myip = ([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0])

UDP_IP = str(myip)
UDP_PORT = int(open('port.txt', 'r').read())

import subprocess
subprocess.Popen('python kuld.py')
subprocess.Popen('python Interface.py')
#irany.py megnyitasa volt itt

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
 
sock.bind((UDP_IP, UDP_PORT))

ANA = 23
ANA2 = 13
I5 = 19
I6 = 26
I3 = 24
I4 = 25
elore = True
run = True
val1 = 0
val2 = 0

##GPIO.setmode(GPIO.BCM)
##
##GPIO.setup(ANA, GPIO.OUT)
##GPIO.setup(I4, GPIO.OUT)
##GPIO.setup(I3, GPIO.OUT)
##pwm = GPIO.PWM(ANA, 1000)
##
##GPIO.setup(ANA2, GPIO.OUT)
##GPIO.setup(I5, GPIO.OUT)
##GPIO.setup(I6, GPIO.OUT)
##pwm2 = GPIO.PWM(ANA2, 1000)
##
##GPIO.output(I4, 0)
##GPIO.output(I3, 0)
##GPIO.output(I5, 0)
##GPIO.output(I6, 0)
##pwm.start(0)
##pwm2.start(0)
##szam = 0
##pi.set_servo_pulsewidth(SER, 1560)
##pi.set_servo_pulsewidth(SER2, 1412)

def running():
    return run

print (myip)
data = ''
szam = 0
c = 0
##c = open('comm.txt', 'r')
while data!='close':
    #f = open('udpdata.txt', 'w')
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    #f.write('haaaaa')
    #f.close()
    i = 0
    e = 0
    com = ''
    if data[0] == 'P':
        ############################################
        i = 1
        while data[i].isdigit() or data[i] == '-':
            i += 1
        com = ''
        for n in range(1, i):
            com = com + data[n]
        szam = int(com)
        print(szam)
        #############################################
        i += 1
        e = i
        while data[i].isdigit() or data[i] == '-':
            i += 1
        com = ''
        for n in range(e, i):
            com = com + data[n]
        #--------------------------------------------
        if True:
            veg1 = szam-int(com)
            veg2 = szam+int(com)
            
            if veg1 > 100: veg1 = 100;
            if veg2 > 100: veg2 = 100;
            if veg1 < -100: veg1 = -100;
            if veg2 < -100: veg2 = -100;
            
            if veg1 > 0: val1 = 1;
            elif veg1 < 0:
                val1 = 2
                veg1 *= -1
            if veg2 > 0: val2 = 1;
            elif veg2 < 0:
                val2 = 2
                veg2 *= -1
            
##            if val1 == 1:
##                GPIO.output(I4, 0)
##                GPIO.output(I3, 1)
##            elif val1 == 2:
##                GPIO.output(I4, 1)
##                GPIO.output(I3, 0)
##            if val2 == 1:
##                GPIO.output(I5, 0)
##                GPIO.output(I6, 1)
##            elif val2 == 2:
##                GPIO.output(I5, 1)
##                GPIO.output(I6, 0)
                
            cszam1 = float(veg1)/2.0+50.0
            cszam2 = float(veg2)/2.0+50.0
            if veg1 == 0: cszam1 = 0;
            if veg2 == 0: cszam2 = 0;
            print ('--------\n'+str(cszam1)+'\n'+str(cszam2))
##            pwm.start(cszam1)
##            pwm2.start(cszam2)
        ######################################################
        i += 1
        e = i
        while data[i].isdigit() or data[i] == '-':
            i += 1
        com = ''
        for n in range(e, i):
            com = com + data[n]
        c = int(com)
        ser = 1560+(890*c)/100
        ser2 = 1412.5-(890*c)/100
        print ser, ser2
##        pi.set_servo_pulsewidth(SER, ser)
##        pi.set_servo_pulsewidth(SER2, ser2)

    if data[0] == 'F':
        pass
##        cam.rotation = 180
##        datum = time.strftime("%Y%m%d-%H%M%S")
##        kep = '/home/pi/Pictures/RCC2.0/pic_'+datum+'.jpg'
##        cam.capture(kep)
    if data[0] == 'G':
        i = 1
        while data[i].isdigit() or data[i] == '.':
            i += 1
        com = ''
        for n in range(1, i):
            com = com + data[n]
        print (com)
 
        i += 1
        e = i
        while data[i].isdigit() or data[i] == '.':
            i += 1
        com = ''
        for n in range(e, i):
            com = com + data[n]
        print (com)
    if data[0] == 'S':
        print ('STOPPING EVERYTHING')
##        GPIO.output(I4, 0)
##        GPIO.output(I3, 0)
##        GPIO.output(I5, 0)
##        GPIO.output(I6, 0)
##        pwm.start(0)
##        pwm2.start(0)
##        szam = 0
##        pi.set_servo_pulsewidth(SER, 1560)
##        pi.set_servo_pulsewidth(SER2, 1412)
##f = open('port.txt', 'w')
##f.write(port+1)
##f.close()
run = False
sock.close()
#GPIO.cleanup()
