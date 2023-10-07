# -*- coding: utf-8 -*-

f=open("suffixed.txt", "r", encoding="latin-1")
outf=open("collected.txt", "w")
words= [word for line in f for word in line.split()]
print(len(words))

def okay(c):
	c= c.lower()
	if c=='a' or c=='o' or c=='i' or c=='e' or c=='s' or c=='z' or c=='b' or c=='c' or c=='d' or c=='f' or c=='g':
		return True
	else:
		return False

i=0
for word in words:
	ok=True
	for ch in word:
		if not okay(ch):
			ok=False
	if ok:
		outf.write(word+'\n')
	if ( i%int(len(words)/40))==0:
		print ('|', end='', flush=True)
	i+=1
		
f.close()
outf.close()
	
	
	
	
	
	
	