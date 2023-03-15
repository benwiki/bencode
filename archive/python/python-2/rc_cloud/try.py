def to8bit(r, g, b):
    rb = int(int(r)*8/256)
    gb = int(int(g)*8/256)
    bb = int(int(b)*4/256)
    c = (rb << 5) | (gb << 2) | bb
    return c

while True:
    a = input('1.szam: ')
    b = input('2.szam: ')
    c = input('3.szam: ')
    print to8bit(a, b, c)
