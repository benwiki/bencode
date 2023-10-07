
with open('word_database.txt', 'r') as f:
	trie = dict.fromkeys(f.read().split('\n'))

for w in trie:
	if w[-3:-1]=='sá':
		print(w)