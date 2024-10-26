from imageio import imread
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

ipcim = input('Kerem az IP cimet: ')
portsz = int(input('Kerem a port szamat: '))

def to8bit(r, g, b):
    rb = int(int(r)*8/256)
    gb = int(int(g)*8/256)
    bb = int(int(b)*4/256)
    c = (rb << 5) | (gb << 2) | bb
    return c

def strtb64(a, b, c):
    # Az els‹ karakter el‹ llˇt sa: az els‹ sz m els‹ 6 bitje }
    id1 = a >> 2;
    #print('elso:'+str(id1))
    
    #{ A m sodik karakter: az els‹ sz m utols˘ 2 bitje }
    #{  ‚s a m sodik sz m els‹ 4 bitje }
    id2 = a << 6;
    id2 = id2 >> 2;
    id2 = id2 + ( b >> 4 );
    #print('masodik: '+str(id2))

    #{ A harmadik karakter: a m sodik sz m utols˘ 4 bitje }
    #{  ‚s a harmadik sz m els‹ k‚t bitje }
    id3 = b << 4;
    id3 = id3 >> 2;
    id3 = id3 + ( c >> 6 );
    #print('harmadik: '+str(id3))

    #{ A negyedik karakter: a harmadik sz m utols˘ 6 bitje }
    id4 = c << 2;
    id4 = id4 >> 2;
    #print('negyedik: '+str(id4))

    #{ A k˘dolt sztring ”ssze llˇt sa }
    kodolt = ''
    #{ 1. karakter }
    if id1 <= 25: kodolt = kodolt + chr(id1+65);
    if (id1>25) and (id1<=51): kodolt = kodolt + chr(id1-26+97)
    if (id1>51) and (id1<=61): kodolt = kodolt + chr(id1-52+48)
    if id1 == 62: kodolt = kodolt + '+'
    if id1 == 63: kodolt = kodolt + '/'
    #{ 2. karakter }
    if id2 <= 25: kodolt = kodolt + chr(id2+65);
    if (id2>25) and (id2<=51): kodolt = kodolt + chr(id2-26+97)
    if (id2>51) and (id2<=61): kodolt = kodolt + chr(id2-52+48)
    if id2 == 62: kodolt = kodolt + '+'
    if id2 == 63: kodolt = kodolt + '/'
    #{ 3. karakter }
    if id3 <= 25 : kodolt = kodolt + chr(id3+65);
    if (id3>25) and (id3<=51): kodolt = kodolt + chr(id3-26+97)
    if (id3>51) and (id3<=61): kodolt = kodolt + chr(id3-52+48)
    if id3 == 62: kodolt = kodolt + '+'
    if id3 == 63: kodolt = kodolt + '/'
    #{ 4. karakter }
    if id4 <= 25: kodolt = kodolt + chr(id4+65);
    if (id4>25) and (id4<=51): kodolt = kodolt + chr(id4-26+97)
    if (id4>51) and (id4<=61): kodolt = kodolt + chr(id4-52+48)
    if id4 == 62: kodolt = kodolt + '+'
    if id4 == 63: kodolt = kodolt + '/'
    return kodolt

pic = 'C:/Users/HBenkex/Pictures/newimagesave.png'
arr = imread(pic) # 640x480x3 array   
for l in range(0, 200):
    if l < 10: strung = '  ' + str(l) + '1';
    elif l < 100 and l > 9: strung += ' ' + str(l) + '1';
    else: strung += str(l) + '1';
    pixels = [0, 0, 0]
    cpix = [0, 0, 0]
    for i in range(0, 99, 3):
        for j in range(i, i+3):
            for k in range(0, 3):
                pixels[k] = arr[l, j, k]
            cpix[j-i] = to8bit(pixels[0], pixels[1], pixels[2])
        strung += str(strtb64(cpix[0], cpix[1], cpix[2]))
    sock.sendto(strung, (ipcim, portsz))
    if l < 10: strung = '  ' + str(l) + '2';
    elif l < 100 and l > 9: strung += ' ' + str(l) + '2';
    else: strung += str(l) + '2';
    pixels = [0, 0, 0]
    cpix = [0, 0, 0]
    for i in range(99, 198, 3):
        for j in range(i, i+3):
            for k in range(0, 3):
                pixels[k] = arr[l, j, k]
            cpix[j-i] = to8bit(pixels[0], pixels[1], pixels[2])
        strung += str(strtb64(cpix[0], cpix[1], cpix[2]))
    sock.sendto(strung, (ipcim, portsz))
    if l < 10: strung = '  ' + str(l) + '3';
    elif l < 100 and l > 9: strung += ' ' + str(l) + '3';
    else: strung += str(l) + '3';
    pixels = [0, 0, 0]
    cpix = [0, 0, 0]
    for i in range(198, 297, 3):
        for j in range(i, i+3):
            for k in range(0, 3):
                pixels[k] = arr[l, j, k]
            cpix[j-i] = to8bit(pixels[0], pixels[1], pixels[2])
        strung += str(strtb64(cpix[0], cpix[1], cpix[2]))
    sock.sendto(strung, (ipcim, portsz))
    if l < 10: strung = '  ' + str(l) + '4';
    elif l < 100 and l > 9: strung += ' ' + str(l) + '4';
    else: strung += str(l) + '4';
    pixels = [0, 0, 0]
    cpix = [0, 0, 0]
    for i in range(297, 318, 3):
        for j in range(i, i+3):
            for k in range(0, 3):
                pixels[k] = arr[l, j, k]
            cpix[j-i] = to8bit(pixels[0], pixels[1], pixels[2])
        strung += str(strtb64(cpix[0], cpix[1], cpix[2]))
    pixels = [0, 0, 0]
    cpix = [0, 0, 0]
    for i in range(318, 320):
        for k in range(0, 3):
            pixels[k] = arr[l, j, k]
        cpix[i-318] = to8bit(pixels[0], pixels[1], pixels[2])
    strung += str(strtb64(cpix[0], cpix[1], 255))
    sock.sendto(strung, (ipcim, portsz))
    '''strung2 = str(strtb64(arr[l, 319, 0], arr[l, 319, 1], arr[l, 319, 2]))+str(strtb64(arr[l, 320, 0], arr[l, 320, 1], arr[l, 320, 2]))
    sock.sendto(strung2.encode(), (ipcim, portsz))'''

