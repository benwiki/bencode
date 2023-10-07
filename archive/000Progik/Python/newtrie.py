from itertools import permutations

class Trie:
	
	def __init__(self):
		self._trie={}
	
	#~~~~~~~~~~~~~~~~~~~~~~
	def add(self, string):
		trie=self._trie
		for L in string:
			if L not in trie:
				#if trie is self._trie:
				#	print(L, end=', ', flush=True)
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
	#~~~~~~
	def __contains__(self, item):
		return item in self._trie
	def __getitem__(self, item):
		return self._trie[item]
		
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&

class Crossword:
	
	def __init__(self, trieobj):
		self.trie=trieobj._trie
	
	#~~~~~~~~~~~~~~~~~~~~~~~
	def getwords(words, letters=None, layer=0):
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
		if letters is None: letters=["" for word in words]
		if trie is None: trie=self.trie
		if length is None: length=len(words)
		if collected is None: collected=Trie()
		
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
				yield from self.getexisting(words, letters, layer+1, trie[L], collected, length)
	
	#~~~~~~~~~~~~~~~~~~~~~~~
	def solutions(self, words):
		coll=Trie()
		for perm in permutations(i for i in range(len(words))):
			print('|',end='',flush=True)
			yield from self.getexisting([words[i] for i in perm], collected=coll)
			
	#~~~~~~~~~~~~~~~~~~~~~~~
	def solutionList(self, words):
		return list(self.solutions(words))
		
#&&&&&&&&&&&&&&&&&&&&&&&&&&&&
		
"""class RealCrosswordPuzzle:
	
	def __init__(self, trie):
			self.trie = trie._trie
			
	def """
			
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
