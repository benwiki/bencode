import socket
import subprocess
from keyboard import is_pressed
from time import time
#import MF1.py

#subprocess.Popen('python C:\Python27\myscripts\Morze\MF1.py', shell = False)

IP = '192.168.' + input('IP cim: 192.168.')
#PORT = MF1.PORT
PORT = input('Port: ')

border = 0.2
transfer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
letter = False
word = False
space = time()
sep = time()
while 1:
    if is_pressed('space'):
        start = time()
        while is_pressed('space'):
            pass
        end = time()
        space = time()
        length = end-start
        if length<border:
            data = '.'
            transfer.sendto(data, (IP, PORT))
        else:
            data = '-'
            transfer.sendto(data, (IP, PORT))
        letter = True
        word = True

    current = time()
    if current-space > 0.4 and letter:
        data = 'l'
        transfer.sendto(data, (IP, PORT))
        letter = False

    if current-space > 1 and word:
        data = 's'
        transfer.sendto(data, (IP, PORT))
        word = False
