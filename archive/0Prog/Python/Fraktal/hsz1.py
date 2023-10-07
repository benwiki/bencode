from turtle import *
right(60)
deg=120
szog=3
e=60

def hsz(d, h=None):
	if h is None: h=d;
	a = 0.22**(h-d)
	for i in range(szog):
		color('red', 'yellow')
		#fd(400*d)
		#right(120)
		fd(4*e*a)
		right(deg)
		fd(e*a)
		color('blue', 'yellow')
		if d>1:
			hsz(d-1, h)
		else:
			for j in range(szog-1):
				fd(2*e*a)
				right(deg)
		fd(8*e*a)
		if i<szog-1:
			right(deg)
	
hsz(3)
done()