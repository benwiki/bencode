from itertools import permutations, product
pms=permutations

f=open('Sort_lemma.txt', 'r', encoding='latin-1')
szotar=[szo.split()[0].lower() for szo in f if len(szo.split())!=0]
f.close()

words=[]
for i in range(4):
    word=input('Next word: ')
    words.append(word)

def getwords(w, n, a):
    global s
    for i in range(len(w[n])):
        if n==len(w)-1:
            szo=''
            szo=szo.join([w[k][a[k]] for k in range(len(w))])
            s.append(szo)
        else:
            getwords(w, n+1, a)
        if a[n]<len(w[n])-1:
            a[n]+=1
        else:
            a[n]=0
    if n==0: return s

perm=pms([i for i in range(len(words))])
zs=0
osszes=[]
for p in perm:
    print ('Perm '+str(zs))
    zs+=1
    wds=[words[k] for k in p]
    index=[0 for w in words]
    s=[]
    getwords(wds, 0, index)
    print('Getted words')
    for ell in s:
        if ell in szotar and not ell in osszes:
            print(ell)
            osszes.append(ell)
                    
print ('Kigyujtve')
                    
f=open('kigyujtott.txt', 'w')
for o in osszes:
    f.write(str(o)+'\n')
f.close()

print ('Elmentve')
