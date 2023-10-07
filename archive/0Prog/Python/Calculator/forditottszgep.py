# -*- coding: utf-8 -*-

f=open("suffixed.txt", "r", encoding="latin-1")
outf=open("collford.txt", "w")
words= [word for line in f for word in line.split()]

def okay(c):
	c= c.lower()
	if c=='h' or c=='o' or c=='i' or c=='e' or c=='s' or c=='z' or c=='b' or c=='l':
		return True
	else:
		return False

for word in words:
	ok=True
	for ch in word:
		if not okay(ch):
			ok=False
	if ok:
		outf.write(word+'\n')
		print ('|', end='', flush=True)
		
f.close()
outf.close()
	
	
	
	
	
	
	