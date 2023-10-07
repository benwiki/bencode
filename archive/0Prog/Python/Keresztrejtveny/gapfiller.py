from newtrie import Trie

trie = Trie()

with open('word_database.txt', 'r') as f:
	for word in f.readlines():
		trie.add(word.strip())

#gappedtext = input("Enter gapped text: ")

def fillGaps(gapped: str, trie: dict):
	res=[]
	for i, char in enumerate(gapped):
		if char in trie:
			trie = trie[char]
		elif char=="_":
			for letter, branch in trie.items():
				if letter=='': continue
				res += [gapped[:i] + letter + fill for fill in fillGaps(gapped[i+1:], branch)]
			break
		else:
			return []
	else:
		res += ([gapped] if '' in trie else [])
	return res
		
print(fillGaps("mo___hatna", trie))