from itertools import permutations

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

    #~~~~~~~~~~~~~~~~~~~~~~~
    def find(self, string):
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
                for g in self.getwords(words, letters, layer+1):
                    yield g

    #~~~~~~~~~~~~~~~~~~~~~~~~
    def getexisting(self, words, letters=None, layer=None, trie=None, collected=None, length=None):
        if letters is None: letters=["" for word in words]
        if trie is None: trie=self.trieobj._trie
        if length is None: length=len(words)
        if collected is None: collected=Trie()
        if layer is None: layer=0

        if layer==length-1:
            for L in words[layer]:
                if L not in trie: continue
                letters[layer]=L
                word=''.join(letters)
                if '' in trie[L] and not collected.find(word):
                    collected.add(word)
                    yield word
        else:
            for L in words[layer]:
                if L not in trie: continue
                letters[layer]=L
                for g in self.getexisting(words, letters, layer+1, trie[L], collected, length):
                    yield g

    #~~~~~~~~~~~~~~~~~~~~~~~
    def solutions(self, words):
        coll=Trie()
        count=0
        for perm in permutations([i for i in range(len(words))]):
            print(count, end=': ', flush=True)
            count+=1
            for g in self.getexisting([words[i] for i in perm], collected=coll):
                print('|', end='', flush=True)
                yield g
            print(' ', flush=True)
    #~~~~~~~~~~~~~~~~~~~~~~~
    def solutionList(self, words):
        return[p for p in self.solutions(words)]

###########################

# <<<<<<<<<<<< Example >>>>>>>>>>>

"""t=Trie()
from time import time

stop=time()
for word in open("word_database.txt","r"):
t.add(word.strip())
print(time()-stop)

stop=time()
find=t.permexisting(["időgép", "pénzeszsák", "kutyaszorító", "mindszentség", "kvintesszencia", "jómagyar"])

for f in find:
print(f)
print(time()-stop)"""
