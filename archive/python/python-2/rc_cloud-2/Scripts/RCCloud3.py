import os
os.system('sudo systemctl start pigpiod')
import socket
import RPi.GPIO as GPIO
import pigpio
pi = pigpio.pi()

SER = 6

pi.set_mode(SER, pigpio.OUTPUT)

myip = ([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0])
UDP_IP = str(myip)
UDP_PORT = 5006
import subprocess
#os.system('cd | cd /home/pi/Documents/Scripts | python fogad.py')
#execfile(fogad.py [, '/home/pi/Documents/Scripts' [,]])
subprocess.Popen("python /home/pi/Documents/Scripts/kuld.py", shell = True)

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
 
sock.bind((UDP_IP, UDP_PORT))

ANA = 23
I3 = 22
I4 = 24
I4I = 0
I3I = 1

GPIO.setmode(GPIO.BCM)

GPIO.setup(ANA, GPIO.OUT)
GPIO.setup(I4, GPIO.OUT)
GPIO.setup(I3, GPIO.OUT)
pwm = GPIO.PWM(ANA, 1000)



print myip
data = ''
szam = 0
c = 0
while data!='S':
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    i = 0
    e = 0
    com = ''
    if data[0] == 'P':
        if data[1] == 'E':
            I4I = 0
            I3I = 1
        if data[1] == 'H':
            I4I = 1
            I3I = 0
        i = 2
        while data[i].isdigit():
            i = i + 1
        com = ''
        for n in range(2, i):
            com = com + data[n]
        if int(com)==0 or com == '':
            GPIO.output(I4, 0)
            GPIO.output(I3, 0)
            pwm.start(0)
        else:
            print (float(com)/2.0+50.0)
            szam = float(com)/2.0+50.0
            GPIO.output(I4, I4I)
            GPIO.output(I3, I3I)
            pwm.start(szam)
 
        i = i + 1
        e = i
        while data[i].isdigit() or data[i] == '-':
            i = i + 1
        com = ''
        for n in range(e, i):
            com = com + data[n]
        print com
 
        i = i + 1
        e = i
        while data[i].isdigit() or data[i] == '-':
            i = i + 1
        com = ''
        for n in range(e, i):
            com = com + data[n]
        c = int(com)
        ser = 1412.5+(887.5*c)/100
        pi.set_servo_pulsewidth(SER, ser)
   
    if data[0] == 'G':
        i = 1
        while data[i].isdigit() or data[i] == '.':
            i = i + 1
        com = ''
        for n in range(1, i):
            com = com + data[n]
        print com
 
        i = i+1
        e = i
        while data[i].isdigit() or data[i] == '.':
            i = i + 1
        com = ''
        for n in range(e, i):
            com = com + data[n]
        print com
    if data[0] == 'S':
        print 'STOPPING EVERITHING'
sock.close()
GPIO.cleanup()
