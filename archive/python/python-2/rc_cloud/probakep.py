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
a = 0
while True:
    a = int(input('1.szám:' ))
    if a == 666: break
    b = int(input('2.szám: '))
    c = int(input('3.szám: '))
    print (strtb64(a, b, c))
