from newtrie import Trie, Crossword
from time import time

trie=Trie()
cw=Crossword(trie)

def conv(unidstr):
    unidstr=unidstr.upper()
    if unidstr == 'A':
        return '.-'
    elif unidstr == 'B':
        return '-...'
    elif unidstr == 'C':
        return '-.-.'
    elif unidstr == 'D':
        return '-..'
    elif unidstr == 'E':
        return '.'
    elif unidstr == 'F':
        return '..-.'
    elif unidstr == 'G':
        return '--.'
    elif unidstr == 'H':
        return '....'
    elif unidstr in 'IÍ':
        return '..'
    elif unidstr == 'J':
        return '.---'
    elif unidstr == 'K':
        return '-.-'
    elif unidstr == 'L':
        return '.-..'
    elif unidstr == 'M':
        return '--'
    elif unidstr == 'N':
        return '-.'
    elif unidstr in 'OÓ':
        return '---'
    elif unidstr == 'P':
        return '.--.'
    elif unidstr == 'Q':
        return '--.-'
    elif unidstr == 'R':
        return '.-.'
    elif unidstr == 'S':
        return '...'
    elif unidstr == 'T':
        return '-'
    elif unidstr in 'UÚ':
        return '..-'
    elif unidstr == 'V':
        return '...-'
    elif unidstr == 'W':
        return '.--'
    elif unidstr == 'X':
        return '-..-'
    elif unidstr == 'Y':
        return '-.--'
    elif unidstr == 'Z':
        return '--..'
    elif unidstr == 'Á':
        return '.--.-'
    elif unidstr == 'É':
        return '..-..'
    elif unidstr in 'ÖŐ':
        return '---.'
    elif unidstr in 'ÜŰ':
        return '..--'
    elif unidstr == 'Ä':
        return '.-.-'
    elif unidstr == '.': return '.-.-.-'
    elif unidstr == ',': return '--..--'
    elif unidstr == ':': return '---...'
    elif unidstr == '?': return '..--..'
    elif unidstr == '!': return '--..--'
    elif unidstr == '-': return '-....-'
    elif unidstr == '"': return '.----.'
    elif unidstr == '(': return '-.--.-'
    elif unidstr == '/': return '-..-.'
    elif unidstr == '*': return '-..-'
    elif unidstr.isnumeric():
        n=int(unidstr)
        if 0<n<=5:
            return '.'*n+'-'*(5-n)
        elif n>5:
            n-=5
            return '-'*n+'.'*(5-n)
        else: return '-'*5
    else:
        return '#'
    

#i=0
#for line in reversed(list(open("Sort_lemma.txt", 'r', encoding='latin-1'))):
#    if i<300:
#        print(line.strip().split("\t"))
#        i+=1

stop=time()
from math import ceil
f=open("word_database.txt", 'w')
for word in open("word_database_correct.txt","r"):
    if not trie.find(word):
    	trie.add(word)
    	f.write(word)
f.close()
    #if word.startswith('kib'): print(word.strip())	
    #morse = ''.join(conv(L) for L in word.strip())
#    mlen=len(morse)
#    first=morse[:mlen//2]
#    second=morse[-1:ceil(mlen/2)-1:-1]
#    
#    if first==second:
#        f.write(morse+word)

#f.close()

#corrected=[word.replace('û', 'ű').replace('õ', 'ő') for word in open("word_database.txt","r")]
#f=open("word_database_correct.txt","w")
#for word in corrected:
#        f.write(word)
#f.close()
        
    #trie.add(word.strip())
#for word in ("eee", "jcken", "xexe"):
#    trie.add(word.strip())

"""t=''.join(filter(lambda a:a!=' ' and a!='\'', str(trie._trie)))
f=open("trie.txt","w")
f.write(t)
f.close()"""
print(time()-stop)

def collect_from(list, trie, word=None, layer=0):
    if word is None: word=[]
    yielded=False
    for L in list:
        if L in trie:
            if len(word)<=layer: word.append("")
            word[layer]=L
            yield from collect_from(list, trie[L],word, layer+1)
        elif "" in trie and not yielded:
            yielded=True
            yield ''.join(word[:layer])
            

stop=time()
#letters=['e','t','i','m','s','o','r','k','h','x','p','é','í','ó','ö','ő']
#szavak=sorted(collect_from(letters, trie))
#from pprint import pprint
#pprint(szavak)
#print(trie.find("miért"))

"""find=cw.solutions(["időgéputazás", "pénzeszsák", "kutyaszorító", "mindszentség", "kvintesszencia", "jómagyar", "beszámíthatatlan", "kötelezettség", "cserediák"])"""

"""sol = sorted(
            cw.solutionList(["időgéputazás", "pénzeszsák", "kutyaszorító", "mindszentségű", "kvintesszencia", "jómagyar"]))
print("sorting done")"""

"""f=open("kigyujt.txt", "w")
for s in sol:
    f.write(s+'\n')
f.close()"""
#print(sol)
print(time()-stop)