# -*- coding: cp1250 -*-
from keyboard import is_pressed
from random import randint, shuffle
w, h = 15, 15;
arr = [[0 for c in range(w)] for d in range(h)]
arr2 = [[0 for c in range(w)] for d in range(h)]
ell = [[0 for c in range(w)] for d in range(h)]
 
x = 0
y = 0
kilep = False
bombak = 0

megegy = True

while megegy:
    level = input('Nehézségi szint (1/2/3): ')
    megegy = False
    if level == 1:
        bombak = 10
    elif level == 2:
        bombak = 25
    elif level == 3:
        bombak = 40
    else:
        print 'Nem jól választottál.'
        megegy = True
    

for i in range(0, w):
    for j in range(0, h):
        arr[i][j] = '.'
        ell[i][j] = 0

bomb2 = bombak
for i in range(0, w):
    for j in range(0, h):
        if bomb2 > 0:
            arr2[i][j] = 'B'
            bomb2 -= 1

def randomize(tomb):
    tomb2 = [[0 for c in range(w)] for d in range(h)]
    volt = [[0 for c in range(w)] for d in range(h)]
    megvolt = 0
    while (megvolt != 100):
        a = randint(0, w)
        b = randint(0, h)
        if volt[a][b] != 1:
            tomb2[a][b] = tomb[(megvolt-megvolt%w)/h][megvolt%w]
            megvolt += 1
            volt[a][b] = 1
    return tomb2

arr2 = randomize(arr2)

def kornyek(tomb, f, g):
    ossz = 0

    x = -1
    y = 1
    if f==0:
        x = 0
    elif f==h-1:
        y = 0

    z = -1
    w2 = 1
    if g==0:
        z = 0
    elif g==w-1:
        w2 = 0
        
    
    for n in range(x, y+1):
        for m in range(z, w2+1):
            if tomb[f+n][g+m] == 'B':
                ossz += 1
    return ossz

def felderit(a, b):
    global arr, arr2, ell
    
    I = -1
    J = 1
    if a==0:
        I = 0
    elif a==h-1:
        J = 0

    K = -1
    L = 1
    if b==0:
        K = 0
    elif b==w-1:
        L = 0
    
    for n in range(I, J+1):
        for m in range(K, L+1):
            e = a+n
            f = b+m
            if arr2[e][f] == 0 and ell[e][f] != 1:
                arr[e][f] = '0'
                ell[e][f] = 1
                felderit(e, f)
            elif arr2[e][f] != 'B':
                arr[e][f] = str(arr2[e][f])
                
def bighely():
    print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')

def kiir():
    global x, y
    for i in range(0, w):
        cucc = ''
        for j in range(0, h):
            if not (i==y and j==x):
                cucc += arr[i][j] + ' '
            else:
                cucc += 'X '
        print (cucc)
 
def kiir2():
    for i in range(0, w):
        cucc = ''
        for j in range(0, h):
            cucc += str(arr2[i][j]) + ' '
        print (cucc)

def kiir3():
    for i in range(0, w):
        cucc = ''
        for j in range(0, h):
            cucc += str(ell[i][j]) + ' '
        print (cucc)
        
def keyb():
    global x , y, kilep, arr, arr2
    while True:
        if is_pressed('w') and not y==0:
            y -= 1
            while is_pressed('w'):
                cucc = 0
            break
        if is_pressed('s') and not y==h-1:
            y += 1
            while is_pressed('s'):
                cucc = 0
            break
        if is_pressed('d') and not x==w-1:
            x += 1
            while is_pressed('d'):
                cucc = 0
            break
        if is_pressed('a') and not x==0:
            x -= 1
            while is_pressed('a'):
                cucc = 0
            break
        if is_pressed('q'):
            while is_pressed('q'):
                cucc = 0
            kilep = True
            print '\n\n\n\n'
            print '//////////////////////////////////////'
            print 'Kiléptél a játékból!'
            print '//////////////////////////////////////'
            break
        if is_pressed('e'):
            while is_pressed('e'):
                cucc = 0
            if arr2[y][x] == 'B':
                bighely()
                i = y-1
                while i!=-1:
                    arr2[i][x] = '|'
                    i -= 1
                i = y+1
                while i!=w:
                    arr2[i][x] = '|'
                    i += 1
                i = x-1
                while i!=-1:
                    arr2[y][i] = '-'
                    i -= 1
                i = x+1
                while i!=w:
                    arr2[y][i] = '-'
                    i += 1
                kiir2()
                print('\nVesztettel sajnos, bomba volt!')
                kilep = True
                break
            else:
                if arr[y][x] == '.':
                    felderit(y, x)
                break
        if is_pressed('b'):
            while is_pressed('b'):
                cucc = 0
            if arr[y][x] == '.':
                arr[y][x] = '/'
            elif arr[y][x] == '/':
                arr[y][x] = '.'
                
            ossz = 0
            for i in range(w):
                for j in range(h):
                    if arr[i][j] == '/' and arr2[i][j] == 'B':
                        ossz += 1
            if ossz == bombak:
                print '\n\n\n'
                print '//////////////////////'
                print 'MEGNYERTED A JATEKOT! :)'
                print '//////////////////////'
                kilep = True
                break
            
for i in range(w):
    for j in range(h):
        if arr2[i][j] != 'B':
            arr2[i][j] = kornyek(arr2, i, j)

while not kilep:
    bighely()
    kiir()
    keyb()
