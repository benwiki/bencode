from itertools import permutations
##import pickle
##import json

class Trie:

    def __init__(self):
        self._trie={}

    #~~~~~~~~~~~~~~~~~~~~~~
    def add(self, string):
        trie=self._trie
        for L in string:
            if L not in trie:
                trie[L]={}
            trie=trie[L]
        trie['']=''

    #~~~~~~~~~~~~~~~~~~~~~~
    def print(self):
        print(self._trie)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##    def easify(self, string):
##        n=0; prev=False; newstr=""
##        for c in string:
##            if c=="}":
##                if n==0: newstr+=c
##                prev=True
##                n+=1
##            elif prev and n>1:
##                newstr+=chr(n+48)+c # mert ord('0')=48
##                n=0
##                prev=False
##            else:
##                newstr+=c
##                n=0
##                prev=False
##        return newstr
##            
##    #~~~~~~~~~~~~~~~~~~~~~~
##    def dump(self):
##        with open('trie.json', 'w') as f:
##            f.write(self.easify(str(self._trie).replace(" ","").replace("'", "").replace("0:0", "").replace(":","")).replace(r"{}","!"))

    #~~~~~~~~~~~~~~~~~~~~~~~
    def contains(self, string):
        trie=self._trie
        for L in string:
            if L in trie:
                trie=trie[L]
            else: return False
        if '' in trie: return True
        else: return False

    #&&&&&&&&&&&&&&&&&&&&&&&&&&&&

class Crossword:

    def __init__(self, trieobj):
        self.trieobj=trieobj

    #~~~~~~~~~~~~~~~~~~~~~~~
    def getwords(self, words, letters=None, layer=0):
        if letters is None: letters=["" for word in words]
        if layer==len(words)-1:
            for L in words[layer]:
                letters[layer]=L
                yield ''.join(letters)
        else:
            for L in words[layer]:
                letters[layer]=L
                yield from self.getwords(words, letters, layer+1)

    #~~~~~~~~~~~~~~~~~~~~~~~~
    def getexisting(self, words, letters=None, layer=0, trie=None, collected=None, length=None):
        if letters is None: letters=['' for word in words]
        if trie is None: trie=self.trieobj._trie
        if length is None: length=len(words)
        if collected is None: collected=Trie()

        for L in words[layer]:
            if L not in trie: continue
            letters[layer] = L
            if layer==length-1:
                word = ''.join(letters)
                if '' in trie[L] and not collected.contains(word):
                    collected.add(word)
                    yield word
            else:
                yield from self.getexisting(words, letters, layer+1, trie[L], collected, length)

    #~~~~~~~~~~~~~~~~~~~~~~~
    def solutions(self, words):
        coll=Trie()
        for perm in permutations(i for i in range(len(words))):
            yield from self.getexisting([words[i] for i in perm], collected=coll)
    #~~~~~~~~~~~~~~~~~~~~~~~
    def solutionList(self, words):
        return list(self.solutions(words))

    #~~~~~~~~~~~~~~~~~~~~~~~
    def sortedSolutionList(self, words):
        return list(sorted(self.solutions(words)))
    

###########################

# <<<<<<<<<<<< Example >>>>>>>>>>>

##t=Trie()
##from time import time
##
##stop=time()
##for word in open("C:/Users/Acer/Google Drive/PROGRAMMING/Python/Trie/word_database.txt", "r"):
##    t.add(word.strip())
##print(time()-stop)
##t.dump()
"""
stop=time()
find=t.permexisting(["időgép", "pénzeszsák", "kutyaszorító", "mindszentség", "kvintesszencia", "jómagyar"])

for f in find:
print(f)
print(time()-stop)"""
