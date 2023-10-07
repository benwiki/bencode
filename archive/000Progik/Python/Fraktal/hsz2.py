from turtle import *

begin_fill()
left(90)
def hsz(d):
	for i in range(3):
		color('red', 'yellow')
		#fd(400*d)
		#right(120)
		fd(200*d)
		right(120)
		fd(50*d)
		color('blue', 'yellow')
		if d>0.25:
			hsz(d/4)
		fd(100*d)
		right(120)
		fd(100*d)
		right(120)
		fd(400*d)
		right(120)
	
hsz(1)

end_fill() 
done()