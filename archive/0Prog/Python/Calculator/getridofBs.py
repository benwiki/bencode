# -*- coding: utf-8 -*-

f=open("collford.txt", "r", encoding="latin-1")
words= [word for word in f]
outf=open("collford_wo_b.txt", "w")

for word in words:
	ok=True
	for ch in word:
		ch=ch.lower()
		if ch=='b':
			ok=False
	if ok:
		outf.write(word)
		print ('|', end='', flush=True)
		
f.close()
outf.close()
	
	
	
	
	
	
	