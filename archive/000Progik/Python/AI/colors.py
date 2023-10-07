from tkinter import *
from random import uniform
from time import sleep
ablak=Tk()
rajz=Canvas(width=700, height=700, bg='white')
rajz.pack()
'''c1,c2,c3=0,0,0
s1=s2=s3=""
for i in range(70):
	for j in range(18):
		s1=s2=s3=""
		if c1<16:
			s1+="0"
		if c2<16:
			s2+="0"
		if c3<16:
			s3+="0"
		s1+=str(hex(c1)[2:])
		s2+=str(hex(c2)[2:])
		s3+=str(hex(c3)[2:])
		color="#"+s1+s2+s3
		rajz.create_rectangle(10*j,10*i, 10*j+10, 10*i+10, fill=color, outline=color)
		if c1==0 and c2==0 and c3<255:
			c3+=1
		elif c1==0 and c2<255 and c3==255:
			c2+=1
		elif c1==0 and c2==255 and c3>0:
			c3-=1
		elif c1<255 and c2==255 and c3==0:
			c1+=1
		elif c1==255 and c2>0 and c3==0:
			c2-=1'''
def coloring(a, b):
	which = 255*5*(a/b)
	if a==1:
		which= 0
	if which <256:
		color='#0000'
		if which<16:
			color+='0'
		color+= (str(hex(int(which)))[2:])
	elif which <511:
		color='#00'
		which -=255
		if which<16:
			color+='0'
		color+= (str(hex(int(which)))[2:])
		color+='ff'
	elif which <766:
		color='#00ff'
		which-=510
		which= 255-which
		if which<16:
			color+='0'
		color+= (str(hex(int(which)))[2:])
	elif which <1021:
		color='#'
		which-=765
		if which<16:
			color+='0'
		color+= (str(hex(int(which)))[2:])
		color+='ff00'
	elif which < 1276:
		color='#ff'
		which-=1020
		which= 255-which
		if which<16:
			color+='0'
		color+= (str(hex(int(which)))[2:])
		color+='00'
	return color

q=35
for i in range(20):
	for j in range(20):
		n,m=i,j+1
		color=coloring(n*20+m, 400)
		for k in range(1000):
			k+=1
			k-=1
		rajz.create_rectangle(q*i,q*j, q*i+q, q*j+q, fill=color, outline=color)
		ablak.update()
		sleep(0.03)
		
		
ablak.mainloop()