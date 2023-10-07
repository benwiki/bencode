# -*- coding: utf-8 -*-

f=open("collected.txt", "r", encoding="latin-1")
words= [word for word in f]
outf=open("coll_wo_g.txt", "w")

for word in words:
	ok=True
	for ch in word:
		ch=ch.lower()
		if ch=='g':
			ok=False
	if ok:
		outf.write(word)
		print ('|', end='', flush=True)
		
f.close()
outf.close()
	
	
	
	
	
	
	