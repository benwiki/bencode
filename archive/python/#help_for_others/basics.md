```py
Kommentek:
   # ez egy komment
   """ez igazából nem komment, hanem egy többsoros string,
   de gyakran használják többsoros kommentelésre.
   3 idézőjel kell hozzá, az elején és a végén."""

print("cucc", 123, False, sep=', ', end='\n')
   # Psszt, "sep" ~ s(z)eparátor ~ közöttük mi legyen
   #        "end" ~ Ende ~ a végén mi legyen
   pl. print(1, 'ööö', 3 sep='-', end='!') # 1-ööö-3!
   pl. print('hé', 'hello', 'szia', sep='... ', end='.') # hé... hello... szia.

Szám adattípusok:
   3 (int)
   3.14 (float)
   7+2j (complex)
   # Psszt, az int-et, float-ot és complex-et lehet átalakító függvénynek használni:
   #       pl. int(3.14) == 3, float(3) == 3.0, complex(3) == 3+0j 

Karaktersorozat / string (str) adattípus:
   "abc", 'abc'
   # Psszt, az str-t is lehet használni, mint függvényt:
   #       pl. str(3) == '3'

Logikai adattípus:
   True ″igaz″
   False ″hamis″

″Semmi″ adattípus:
   None

Operátorok:
   ==, !=, <, >, <=, >=
      # pl. (1 == 2) == False
      # pl. (1 < 2) == True
      # pl. (1 > 2) == False
      # pl. (2 != 2) == False

   not, and, or
      # pl. (not True) == False
      # pl. (True and False) == False
      # pl. (True or False) == True

   in, not in
      # pl. 1 in [1, 2] == True
      # pl. 1 not in [1, 2] == False

   is, is not
      pl. 1 is 1 == True, 1 is 2 == False, ...

Műveletek:
   +, -, *, /, //, %, **, ()
      pl. 3+2 == 5, 3-2 == 1, 3*2 == 6, 3/2 == 1.5, 3//2 == 1, 3%2 == 1, 3**2 == 9
      megj.: // -> lekerekítő osztás, % -> maradék (osztásnál), ** -> hatványozás

Változók:
   a = 1
   b = 2
   b = 312  # felülírja a b értékét
   c = a + b
   # Psszt, ha leírjuk a változó nevét, akkor a python behelyettesíti a változó értékét.
   #        pl. print(a) -> 1, print(b) -> 312, print(c) -> 313
   # Psszt, a változó neve nem kezdődhet számmal, és nem tartalmazhat szóközt.
   #        A változó neve nem lehet kulcsszó (pl. if, else, for, ...).

Léptethető adattípusok:
   [1, 2], list()
   (1, 2), tuple()
   {1, 2}, set()
   {"a": 1, "b": 2}, dict()
   # Psszt, a string pl. '12' ugyanúgy léptethető!

   max, min, sum
      pl. max([1, 2, 3]) == 3, min([1, 2, 3]) == 1, sum([1, 2, 3]) == 6

   any, all
      pl. any([True, False, True]) == True, all([True, False, True]) == False

   len, sorted
      pl. len([1, 2, 3]) == 3, sorted([3, 1, 2]) == [1, 2, 3]



   for item in iterator:
      pl. for i in ['a', 'b', 'c']: print(i) # a, b, c
      pl. for i in 'abc': print(i) # a, b, c
   
   for item in range(start, stop, step):
      pl. for i in range(1, 4, 1): print(i) # 1, 2, 3

   break, continue
      pl.
      for i in [1, 2, 3]:
         if i == 2: break
         else: print(i) # 1

      for i in [1, 2, 3]:
         if i == 2: continue
         else: print(i) # 1, 3

   range, zip, reversed
      pl. range(1, 4, 1) == [1, 2, 3]
      pl. reversed([1, 2, 3]) == [3, 2, 1]

   from math import pi

   (1 if condition else 0)
      pl. (1 if 2 < 3 else 0) == 1

   Objekte
      is, is not
         unterschied zwischen '==' und 'is':
            == -> value check: ([1, 2] == [1, 2]) == True
            is -> object check: ([1, 2] is [1, 2]) == False
      del
      class
   dict
      key in d # True, falls das Dictionary d den Schlüssel key enthält.
      bool(d) # True, falls das Dictionary nicht leer ist.
      len(d) # Liefert die Zahl der Elemente (Assoziationen) in d.
      d.get(key, value) # kein Fehler, wenn key nicht vorhanden -> returns "value" (None, wenn es weggelassen wurde).
      .keys(), .values(), .items()
```