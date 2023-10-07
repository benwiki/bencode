# -*- coding: utf-8 -*-

f=open("web2.2-freq-sorted-lemmatized.txt", "r", encoding="latin-1")
outf=open("collemma.txt", "w")
#words= [word for line in f for word in line.split()]
rows= sum(1 for row in f)
print (rows, flush=True)
f.close()

f=open("web2.2-freq-sorted-lemmatized.txt", "r", encoding="latin-1")
words=[]
i=0
"""for line in f:
	if len(line.split())!=0:
		words.append(line.split()[0])
		if (i % int(rows/20)) ==0:
			print('|', end='', flush=True)
		i+=1"""
words = [line.split()[0] for line in f if len( line.split()) != 0]

def okay(c):
	c= c.lower()
	if c=='a' or c=='o' or c=='i' or c=='e' or c=='s' or c=='z' or c=='b' or c=='c' or c=='d' or c=='f' or c=='g':
		return True
	else:
		return False

print('\nRead-in complete!\n')
"""i=0
for word in words:
	ok=True
	for ch in word:
		if not okay(ch):
			ok=False
	if ok:
		outf.write(word+'\n')
	if (i%int(len(words)/20))==0:
		print ('|', end='', flush=True)
	i+=1
print('\nFile ready!')
		
f.close()
outf.close()"""
	
	
	
	
	
	
	