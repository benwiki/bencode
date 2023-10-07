from itertools import permutations
from typing import Iterator

class Trie:
	
	def __init__(self, trie=None):
		if trie is None:
			self._trie={}
		else:
			self._trie=trie
	
	def add(self, string):
		trie=self._trie
		for L in string:
			if L not in trie:
				trie[L]={}
			trie=trie[L]
		trie['']=''
	
	def print(self):
		print("visuals coming soon")
		
	def find(self, string):
		trie=self._trie
		for L in string:
			if L in trie:
				trie=trie[L]
			else: return False
		if '' in trie: return True
		else: return False
		
	def dig(self, chars: str):
		trie=self._trie
		for char in chars:
			if char in trie:
				trie=trie[char]
			else:
				return None
		return Trie(trie)

	def __contains__(self, item):
		return item in self._trie

	def __getitem__(self, item):
		return Trie(self._trie[item])

	def keys(self):
		return self._trie.keys()

	def values(self):
		return (Trie(branch) for branch in self._trie.values())

	def items(self):
		return zip(self.keys(), self.values())

		
# ==================================

class Crossword:
	
	def __init__(self, trieobj):
		self.trie=trieobj._trie
	
	#~~~~~~~~~~~~~~~~~~~~~~~
	def getwords(
			self, words,
			letters=None,
			layer=0
			) -> Iterator[str]:
		if letters is None: letters=["" for _ in words]

		if layer == len(words):
			yield ''.join(letters)

		for L in words[layer]:
			letters[layer]=L
			yield from self.getwords(words, letters, layer+1)
					
	#~~~~~~~~~~~~~~~~~~~~~~~~
	def getexisting(
			self, words,
			letters=None,
			layer=0,
			trie=None,
			collected=None
			) -> Iterator[str]:
		if letters is None: letters=["" for _ in words]
		if trie is None: trie=self.trie
		if collected is None: collected=Trie()
		
		if layer == len(words):
			res=''.join(letters)
			if '' in trie and not collected.find(res):
				collected.add(res)
				yield res
		
		word = words[layer]
		for L in word:
			if L not in trie: continue
			letters[layer]=L
			yield from self.getexisting(words, letters, layer+1, trie[L], collected)
	
	#~~~~~~~~~~~~~~~~~~~~~~~
	def solutions(self, words) -> Iterator[str]:
		coll=Trie()
		for perm in permutations(range(len(words))):
			# print('|',end='',flush=True)
			yield from self.getexisting([words[i] for i in perm], collected=coll)
			
	#~~~~~~~~~~~~~~~~~~~~~~~
	def solutionList(self, words) -> list[str]:
		return list(self.solutions(words))
		


# <<<<<<<<<<<< Example >>>>>>>>>>>

"""
t=Trie()
from time import time

stop=time()
for word in open("word_database.txt","r"):
	t.add(word.strip())
print(time()-stop)

stop=time()
solutions=t.solutions(["időgép", "pénzeszsák", "kutyaszorító", "mindszentség", "kvintesszencia", "jómagyar"])

for f in solutions:
	print(f)
print(time()-stop)
"""
