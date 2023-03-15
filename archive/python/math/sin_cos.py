def torad(x):
    return 0.01745329251994*x

def hatv(m, n):
    i = 0
    o = 1
    if n == 0:
        return 1
    elif n == 1:
        return m
    else:
        for i in range(0, n):
            o = o * m
        return o

def fact(n):
    if(n == 1 or n == 0):
        return 1
    else:
        return n*fact(n-1)
    
x = torad(90)
sinuss = 0.0
coss = 0.0

for i in range(0, 15):
    if i%2==0:
        sinuss += hatv(x, (2*i+1))/float(fact(2*i+1))
    else:
        sinuss -= hatv(x, (2*i+1))/float(fact(2*i+1))
print(sinuss)

for i in range(0, 15):
    if i%2==0:
        coss += hatv(x, (2*i))/float(fact(2*i))
    else:
        coss -= hatv(x, (2*i))/float(fact(2*i))
print(coss)
