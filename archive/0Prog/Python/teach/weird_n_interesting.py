print([f'{stuff}'*2 for stuff in [3,2]])

cucc=15
print(f"{cucc:02X}")

columbus = (30, 11)
churchill = columbus
churchill += (1874,)
print(list(range(2,3,3)))
print(columbus)
print(bool(__debug__), end='')
print("\rj")
print(-2**2)
print(10j/(5+1j))
print(abs(3+4j))
print((1+2j)/(3+4j))
import math
print(math.floor(4.56))
print(int("10101",2))

def f(x, y):
	return x + y
	
from functools import partial

ff = partial(f, y=5)

print(ff(3))