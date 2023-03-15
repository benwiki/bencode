"""
Ez egy left-truncatable prímeket kereső program. meg is találja a legnagyobbat.
és milyen gyorsan!
"""

import random
maxi=0

def miller_rabin(n, k):
    if n == 2:
        return True

    if n % 2 == 0:
        return False

    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

count=sokjegy=0
def iteral(sz, num=10):
    global maxi, count, sokjegy
    found_some_more = False
    for i in range(1, 10): # 1-től 9-ig végigmegyünk a lehetőségeken...
        p = sz+num*i # ...változik az eggyel magasabb helyiérték.
        if miller_rabin(p, 40): # ha a szám prím,
            if maxi<p: maxi=p # elmentjük a legnagyobbat,
            iteral(p, num*10) # és mehet egy új ág!
            found_some_more = True # (találtunk új ágat)
            
    if not found_some_more: # ha nincs tovább, elérkeztünk az adott szám végéhez...
        count+=1 # ...akkor van egy találatunk.
        if len(str(sz)) > 21: # Amennyiben ez 15 számjegynél hosszabb...
            sokjegy += 1
            print (sz) # ...kiíratjuk!

def fugg(sz):
    x = 5
    
    while (x < sz):
        x+=1
        #print miller_rabin(x, 40), x
        if miller_rabin(x, 40):
            outf = open("out.txt", "a")  
            outf.write(str(x)+'\n')
            outf.close()
            
      

for i in [3, 7]:
    iteral(i)
    #fugg(input())
    print ('\nready!')
    print (maxi,'\n')

print (count, sokjegy)
