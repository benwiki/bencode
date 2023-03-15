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
    
def NAlattK(n, k):
    if k == 0:
        return 1
    elif k == 1:
        return n
    elif k == (n-1):
        return n
    elif k == n:
        return 1
    else:
        return fact(n)/(fact(k)*fact(n-k))*1.0

def BinomPdf(n, k, p):
    return NAlattK(n, k) * hatv(p, k) * hatv((1-p), (n-k))

def BinomCdf(n, k, p):
    if k == 0:
        return BinomPdf(n, 0, p)
    else:
        return BinomPdf(n, k, p) + BinomCdf(n, (k-1), p)
    
n = input('n = ')
k = input('k = ')
p = input('p = ')
print BinomCdf(n, k, p)
