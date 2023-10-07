# -*- coding: utf-8 
f=open("Sort_lemma.txt", "r", encoding="latin-1")
lines=f.readlines()
print (lines[135])
f.close()
print ("Collected")
words=[line.split()[0:2].lower() for line in lines if len(line.split())>0]
print ("formatted")

def okay(c):
	c= c.lower()
	if c=='a' or c=='o' or c=='i' or c=='e' or c=='s' or c=='z' or c=='b' or c=='c' or c=='d' or c=='f' or c=='g':
		return True
	else:
		return False
		
def ok(inp):
	if inp in words and inp in ossz:
		return True
	else:
		ossz.append(inp)
		return False

print('Read-in complete!')

ossz=[]
f=open('lya2.txt', 'w')
f2=open('vers.txt', 'r')
vers = [words[words.index(word.lower())][1] for line in vers for word in line]

for word in vers:
	if ok(word):
		f.write(line.split()[0]+'\n')
f.close()

"""f=open('newlemmatyi.txt', 'w')
for word in words:
	itsok=True
	for ch in word:
		if not okay(ch):
			itsok=False
	if itsok:
		f.write(word+'\n')
f.close()

print('File ready!')"""
		
	
	
	
	
	