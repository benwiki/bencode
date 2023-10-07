f=open('autok.txt', 'r')
data=[line.split() for line in f]
f.close()

#2. Feladat~~~~~~~~~~~~~~~~~~~
print('2. feladat:')
for d in reversed(data):
	if d[5]=='0':
		print(d[0]+'. nap, rendszam: '+d[2])
		break
#3. Feladat~~~~~~~~~~~~~~~~~~~
print('3. feladat:')
nap=input('Nap: ')
for d in data:
	if d[0]==nap:
		print(d[1], d[2], d[3], 'ki' if d[5]=='0' else 'be')
#4. Feladat~~~~~~~~~~~~~~~~~~~
print('4. feladat:')
autokint=[]
for d in data:
	if d[5]=='0':
		autokint.append(d[2])
	else:
		autokint.remove(d[2])
print (str(len(autokint))+' autot nem hoztak vissza ho vegere')

#5. Feladat~~~~~~~~~~~~~~~~~~~
def linear(arr):
	return [item for sub in arr for item in sub]

print('5. feladat:')
start=[]
end=[]
for d in data:
	if len(start)==10:
		break
	if not d[2] in linear(start):
		start.append([d[2], d[4]])
		
solution=[]
		
for d in reversed(data):
	if len(end)==10:
		break
	for s in start:
		if s[0] == d[2] and d[2] in linear(start):
			if d[5]=='1':
				solution.append(d[2]+' '+str(int(d[4])-int(s[1]))+' km')
				start.remove(s)
			break
solution.sort()
for s in solution:
	print(s)
			

#7. Feladat~~~~~~~~~~~~~~~~~
print('7. feladat:')
auto=input('Auto: ')
f=open('X_menetlevel.txt', 'w')
kimenet=''
t='\t'
for d in data:
	if d[2]==auto:
		if d[5]=='0':
			kimenet=d[3]+t+d[0]+'. '+d[1]+t+d[4]+' km'
		else:
			bemenet=t+d[0]+'. '+d[1]+t+d[4]+' km\n'
			f.write(kimenet+bemenet)
			kimenet=''
if kimenet!='':
	f.write(kimenet)
f.close()

