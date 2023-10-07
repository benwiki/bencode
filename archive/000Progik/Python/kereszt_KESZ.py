from itertools import permutations, product
from time import sleep, time
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
        new[ind].append(arr[i])
    else:
        new.append([arr[i]])
        osszbetu.append(arr[i][0])
        ind+=1
    return new

def graph(arr, layer=0, letters=1, word=0, graphized=[]):
    if layer==0:
        graph(arr, layer=1, graphized=graphized)
        return graphized
	
    elif letters<=len(arr[word]) and word<len(arr):
        cur_word=word

        while cur_word<len(arr) and arr[word][:letters-1] == arr[cur_word][:letters-1]:
            new_index=cur_word

            if word==cur_word or arr[cur_word][letters-1] not in graphized:
                graphized.append(arr[cur_word][letters-1])

            if letters < len(arr[cur_word]):
                if arr[cur_word-1][:letters]==arr[cur_word][:letters] and cur_word>0:
                    graphized.append([''])
                else:
                    graphized.append([])
                part=graphized[len(graphized)-1]
                new_index=graph(arr, layer+1, letters+1, cur_word, part)

            if new_index==cur_word:
                cur_word+=1
            else: cur_word=new_index
        return cur_word

    return word
    
    
def search(graph, word, letter=0):
    wlen=len(word)
    if letter<wlen and word[letter] in graph:
        #print(letter, word[letter], "*")
        list_ind=graph.index(word[letter])+1
        if len(graph)>list_ind:
            #print(list_ind, "**")
            part=graph[list_ind]
            if isinstance(part, list):
                #print("***")
                return search(part,word,letter+1)
            elif letter==wlen-1:
                #print("teli találat")
                return True
            else:
                return False
        elif letter==wlen-1:
            #print("Listavégi találat")
            return True
        else:
            return False
    elif '' in graph and letter==wlen:
        #print("üres találat")
        return True
    else:
        return False

"""f=open('Sort_lemma.txt', 'r', encoding='latin-1')
print('Filet megnyitottam')
kivalogat=[szo.split()[0].lower() for szo in f if len(szo.split())!=0]
print('Kivalogattam')
kivalogat.sort()
szotar=betuszerintbont(kivalogat)
print('Betu szerint bontottam')
f.close()"""

f=open('Sort_lemma.txt', 'r', encoding='latin-1')
print('Filet megnyitottam')
kivalogat=[szo.split()[0].lower() for szo in f if len(szo.split())!=0]
print('Kivalogattam')
kivalogat.sort()
f.close()

print("Elkezdtem graffa alakitani")
t=time()
mygraph=graph(kivalogat)
print('Kesz vagyok, es ez', str(time()-t), 'masodperc volt.')



hany = int(input('Hány szó lesz: '))

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

perm=list(pms([i for i in range(len(words))]))
zs=1
osszes=[]
for p in perm:
    wds=[words[k] for k in p]
    index=[0 for w in words]
    s=[]
    getwords(s, wds, 0, index)
    #print (len(s))
    for ell in s:
        if search(mygraph, ell) and not ell in osszes:
            osszes.append(ell)
            print('|', end='', flush=True)
    print(zs)
    zs+=1
f=open('kigyujtott.txt', 'w')
for o in osszes:
    f.write(str(o)+'\n')
f.close()
	    
print ('Osszes kigyujtve')

