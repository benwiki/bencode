from itertools import permutations, product
from time import sleep
pms=permutations

osszbetu=[]
def betuszerintbont(arr):
	global osszbetu
	new=[]
	ind=0
	for i in range(len(arr)):
		if i==0:
			new.append([arr[i]])
			osszbetu.append(arr[i][0])
			continue
		if arr[i][0]==arr[i-1][0]:
			new[ind].append([arr[i]])
		else:
			new.append([arr[i]])
			osszbetu.append(arr[i][0])
			ind+=1
	return new

f=open('Sort_lemma.txt', 'r', encoding='latin-1')
print('Filet megnyitottam')
kivalogat=[szo.split()[0].lower() for szo in f if len(szo.split())!=0]
print('Kivalogattam')
kivalogat.sort()
szotar=betuszerintbont(kivalogat)
print('Betu szerint bontottam')
f.close()

print (osszbetu)

hany=int(input('Hany szo lesz: '))
words=[]
for i in range(hany):
	word=input('Köv. szó: ')
	words.append(word)

def getwords(s, w, n, a):
	for i in range(len(w[n])):
		if n==len(w)-1:
			szo=''.join([w[k][a[k]] for k in range(len(w))])
			s.append(szo)
		else:
			getwords(s, w, n+1, a)
		if a[n]<len(w[n])-1:
			a[n]+=1
		else:
			a[n]=0

perm=pms([i for i in range(len(words))])
zs=1
osszes=[]
for p in perm:
	print (str(zs))
	zs+=1
	wds=[words[k] for k in p]
	index=[0 for w in words]
	s=[]
	getwords(s, wds, 0, index)
	for ell in s:
		if ell in szotar[osszbetu.index(ell[0])] and not ell in osszes:
			print (ell)
			osszes.append(ell)
			
print ('Kigyujtve')
			
f=open('kigyujtott.txt', 'w')
for o in osszes:
	f.write(str(o)+'\n')
f.close()

print ('Elmentve')