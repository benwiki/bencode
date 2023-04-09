# -*- coding: cp1250 -*-
# -----remek lifehackek és easter eggek pythonban-----
# 1.: a listák generátorai
from random import randint
sorozat = [i*2 for i in range(10)]  # a lista elemei a "for" szócska előtti
# értéket veszik fel, a range-ben szereplő
# elemászámmal
print("sorozat:", sorozat)

# megfordítja a lista sorrendjét, és visszatér a megfordított listával...
forditott = reversed(sorozat)
print("forditott:", list(forditott))
print("sorozat:", sorozat)  # ...de azt nem változtatja meg.

# ez is, de ez arra hivatott, hogy magának a listának a sorrendjét változtassa meg.
sorozat.reverse()
print("sorozat:", sorozat)

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
multi_dim = [[[randint(0, 100) for k in range(4)]
              for j in range(3)] for i in range(2)]
# ez egy 3 dimenzi�s t�mb egyszer�en gener�lva, minden eleme v�letlenszer�
# l�tod, hogy egy olyan list�t veszel 2-szer (i), aminek 3 eleme van (j), �s minden eleme egy 4 elem� lista (k)
# k***** men�
print("multi_dim:", multi_dim)
flat = [multi_dim[i][j][k]
        for i in range(2) for j in range(2) for k in range(2)]
# �gy lap�tasz le egy t�bbdimenzi�s t�mb�t. �rdekes, hogy ford�tva van a ciklusok sorrendje: i, j, k

for elem in flat:  # list�n val� v�gigiter�l�sn�l az "elem" v�ltoz�...
    # print(elem)   # ...mindig a lista k�vetkez� elem�nek �rt�k�vel lesz egyenl�...
    pass
print("flat:", flat)

flat2 = []
# ...ha ez az �rt�k egy lista, akkor a v�ltoz� is egy lista lesz, amin...
for reteg in multi_dim:
    for sor in reteg:   # ugyancsak v�gig lehet iter�lni.
        for elem in sor:
            # �gy is k�sz�lhetett volna a lelap�tott lista.
            flat2.append(elem)
print("flat2:", flat2)

# vagy ak�r �gy. szemet gy�ny�rk�dtet�...
flat4 = [elem for reteg in multi_dim for sor in reteg for elem in sor]
print("flat4:", flat4)

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
felteteles = [1 for i in range(100) if i % 3 == 0]
# felt�teles listagener�tor, akkor sz�rja be az elemet, ha a felt�tel teljes�l
felt2 = [1 if i % 3 == 0 else 0 for i in range(100)]
# ha else is kell, a for ciklus el�ttre kell �rnod. A sorrend fontos.
"felt3 = [1 if i%3==0 for i in range(100)]"  # ez hib�s, pr�b�ld csak ki
"felt4 = [1 for i in range(100) if i%3==0 else 0]"  # ez is

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
i, j, k = 1, 2, 3  # a tuple-�k... j� cuccokat lehet vel�l csin�lni.
# ez itt �pp inicializ�l�s tuple-m�dra.
print("i, j, k:", i, j, k)

# a tuple-�ket a sima z�r�jel �s a vessz� jellemzi, �s nem lehet �ket indexel�ssel megv�ltoztatni.
# egy�bk�nt viszonr ugyan�gy viselkednek, mint a list�k.
tup = (1, 2, 3)
tup = 1, 2, 3  # mindegy hogy kiteszed-e a z�r�jelet

"tup[0] = 4"  # hib�s, "nem lehet �ket indexel�ssel megv�ltoztatni"...
print("tup[0]:", tup[0])  # lehet viszont indexelni

# ha nagyon meg akarod v�ltoztatni a tuple elemeit,
# csin�lj bel�le list�t, v�ltoztass rajta, azt�n alak�tsd vissza
lista = list(tup)
lista[0] = 4
tup = tuple(lista)  # ez �gy hely�nval�
print("tup[0]:", tup[0])

i, j, k = (i+1 for i in range(3))  # lehet �gy is... gener�torral, hihihi
print("i, j, k:", i, j, k)
# ide viszont kell a z�r�jel, ez hib�s sor.
"i, j, k = i+1 for i in range(3)"
# a gener�toroknak mindig kell valami, amibe elemeket sz�rogathatnak...
# ez jelen esetben egy tuple.

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
# a k�vetkez� az �n. dictionary, amiben te mondhatod meg, hogy mi legyen az index, pl.
szotar = {"cucc": 69, "bucc": 21}
print('szotar["cucc"]:', szotar["cucc"])  # igen, �gy indexeled. k*** j�


print("szotar.keys():", szotar.keys())  # a kulcsszavai az indexek,

print("szotar.values():", szotar.values())  # az �rt�kei... az �rt�kei.

# �s egyben is list�v� (akarom mondani tuple-�k list�j�v�) lehet alak�tani, �gy.
print("szotar.items():", szotar.items())
# rohadt �rdekes...

# egy�bk�nt egy mezei list() csak az indexeit szedi ki bel�le... na ja
print("list(szotar):", list(szotar))
