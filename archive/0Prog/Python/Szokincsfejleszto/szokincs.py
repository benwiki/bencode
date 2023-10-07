# ['a', 'a', 'ART', 'ART', '1', 'v', '52706200', '71143086']

class Word:
	changed:str
	base:str
	chType:str
	bType:str
	len:str
	letterType:str
	rate1:str
	rate2:str
	def __init__(self, wordlist: list):
		if wordlist == ['']:
			self.len=0
			return
		keys = ('changed', 'base', 'chType', 'bType', 'len', 'letterType', 'rate1', 'rate2')
		self.__dict__ = dict(zip(keys, wordlist))


words={}
with open("Sort_lemma.txt", 'r', encoding="latin-1") as wordfile:
	i=0
	for line in wordfile:
		w = Word(line.strip().split('\t'))
		if int(w.len) > 1 and w.changed == w.base and w.base == w.base.lower() and 'PREV' not in w.bType:
			rate = int(w.rate2)
			R = words[rate] = words.get(rate, {})
			R[w.bType] = R.get(w.bType, []) + [w.base]
			i+=1
		if i>=100000:
			break

with open('oft8.txt', 'w') as oft:
	for rate, words in sorted(words.items()):
		for wtype, word in words.items():
			oft.write(f'{rate} {wtype} {word}\n')
print('ready')