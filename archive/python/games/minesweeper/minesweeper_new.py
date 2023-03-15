# -*- coding: cp1250 -*-
from keyboard import is_pressed
from random import randint, shuffle

def main():
    global w, h, arr, arr2, ell, x, y, bombak, kilep, megegy, bomb2
    w, h = 10, 10
    arr = [['.' for _ in range(w)] for _ in range(h)]
    arr2 = [[0 for _ in range(w)] for _ in range(h)]
    ell = [[0 for _ in range(w)] for _ in range(h)]

    x = 0
    y = 0
    kilep = False
    bombak = 0

    megegy = True

    while megegy:
        level = int(input('Nehezsegi szint (1/2/3): '))
        megegy = False
        if level == 1:
            bombak = 10
        elif level == 2:
            bombak = 15
        elif level == 3:
            bombak = 20
        else:
            print('Nem jol valasztottal.')
            megegy = True

    bomb2 = bombak
    for i in range(0, 10):
        for j in range(0, 10):
            if bomb2 > 0:
                arr2[i][j] = 'B'
                bomb2 -= 1

    arr2 = randomize(arr2)

    for i in range(10):
        for j in range(10):
            if arr2[i][j] != 'B':
                arr2[i][j] = kornyek(arr2, i, j)

    while not kilep:
        bighely()
        kiir()
        keyb()


def randomize(tomb):
    tomb2 = [[0 for c in range(10)] for d in range(10)]
    volt = [[0 for c in range(10)] for d in range(10)]
    megvolt = 0
    while (megvolt != 100):
        a = randint(0, 9)
        b = randint(0, 9)
        if volt[a][b] != 1:
            tomb2[a][b] = tomb[int((megvolt-megvolt % 10)/10)][megvolt % 10]
            megvolt += 1
            volt[a][b] = 1
    return tomb2


def kornyek(tomb, cur_x, cur_y):
    ossz = 0

    # Nezzuk, hogy valamelyik szelen vagy sarokban vagyunk-e!

    # Alapbeallitasok
    x_bal = -1
    x_jobb = 1
    if cur_y == 0:  # Ha a bal oldalan vagyunk...
        x_bal = 0   # a bal oldali hatart allitjuk 0-ra.
    elif cur_y == 9:  # Ha a jobb oldalan vagyunk...
        x_jobb = 0  # akkor a jobb oldali hatart.

    # Alapbeallitasok
    y_felso = -1
    y_also = 1
    if cur_x == 0:  # Ha a tetejen vagyunk...
        y_felso = 0  # a felso hatart allitjuk 0-ra.
    elif cur_x == 9:  # Ha az aljan vagyunk...
        y_also = 0  # akkor az also hatart.

    for n in range(y_felso, y_also+1):
        for m in range(x_bal, x_jobb+1):
            if tomb[cur_x + n][cur_y + m] == 'B':
                ossz += 1
    return ossz


def felderit(a, b):
    global arr, arr2, ell
    print(-int(a != 0), int(a != 9))
    for n in range(-int(a != 0), int(a != 9)+1):
        for m in range(-int(b != 0), int(b != 9)+1):
            e = a+n
            f = b+m
            if arr2[e][f] == 0 and ell[e][f] != 1:
                arr[e][f] = '0'
                ell[e][f] = 1
                felderit(e, f)
            elif arr2[e][f] != 'B':
                arr[e][f] = str(arr2[e][f])


def bighely():
    print('\n' * 40)


def kiir():
    global x, y
    for i in range(0, 10):
        cucc = ''
        for j in range(0, 10):
            if not (i == y and j == x):
                cucc += arr[i][j] + ' '
            else:
                cucc += 'X '
        print(cucc)


def kiir2():
    for i in range(0, 10):
        cucc = ''
        for j in range(0, 10):
            cucc += str(arr2[i][j]) + ' '
        print(cucc)


def kiir3():
    for i in range(0, 10):
        cucc = ''
        for j in range(0, 10):
            cucc += str(ell[i][j]) + ' '
        print(cucc)


def keyb():
    global x, y, kilep, arr, arr2
    while True:
        if is_pressed('w') and not y == 0:
            y -= 1
            while is_pressed('w'):
                cucc = 0
            break
        if is_pressed('s') and not y == 9:
            y += 1
            while is_pressed('s'):
                cucc = 0
            break
        if is_pressed('d') and not x == 9:
            x += 1
            while is_pressed('d'):
                cucc = 0
            break
        if is_pressed('a') and not x == 0:
            x -= 1
            while is_pressed('a'):
                cucc = 0
            break
        if is_pressed('q'):
            while is_pressed('q'):
                cucc = 0
            kilep = True
            print(
                '\n\n\n\n\n'
                '//////////////////////////////////////\n'
                'Kileptel a jatekbol!\n'
                '//////////////////////////////////////\n')
            break
        if is_pressed('e'):
            while is_pressed('e'):
                cucc = 0
            if arr2[y][x] == 'B':
                bighely()
                i = y-1
                while i != -1:
                    arr2[i][x] = '|'
                    i -= 1
                i = y+1
                while i != 10:
                    arr2[i][x] = '|'
                    i += 1
                i = x-1
                while i != -1:
                    arr2[y][i] = '-'
                    i -= 1
                i = x+1
                while i != 10:
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
            for i in range(10):
                for j in range(10):
                    if arr[i][j] == '/' and arr2[i][j] == 'B':
                        ossz += 1
            if ossz == bombak:
                print(
                    '\n\n\n\n'
                    '//////////////////////\n'
                    'MEGNYERTED A JATEKOT! :)\n'
                    '//////////////////////\n')
                kilep = True
                break


if __name__ == "__main__":
    main()
