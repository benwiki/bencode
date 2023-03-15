from time import sleep
from subprocess import Popen
Popen('python C:\Python27\proba2.py', shell = False)

x = 5
while True:
    x = input('input x: ')
    f = open('x.txt', 'w')
    f.write(x)
    f.close()
