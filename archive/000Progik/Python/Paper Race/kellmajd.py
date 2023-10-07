def linecross(line1, line2):
	x1, y1, x2, y2= (line1[i] for i in range(4))
	x3, y3, x4, y4= (line2[i] for i in range(4))
	oszt1=((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1))
	oszt2=((y4-y3)*(x2-x1) - (x4-x3)*(y2-y1))
	if oszt1!=0 and oszt2!=0:
		px = ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3)) / oszt1
		py = ((x2-x1)*(y1-y3) - (y2-y1)*(x1-x3)) / oszt2
	else:
		return False
	print ((px, py))
	if px>0 and px<1 and py>0 and py<1:
		return True
	else:
		return False
		
while 1:
	line1=[int(input())for i in range(4)]
	line2=[int(input())for i in range(4)]
	print('\n')
	linecross(line1, line2)
	
	
	
	
	