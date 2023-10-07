

# ['a', 'a', 'ART', 'ART', '1', 'v', '52706200', '71143086']

words=[]
with open("Sort_lemma.txt", 'r', encoding="latin-1") as wordfile:
	i=0
	for line in wordfile:
		word = line.strip().split('\t')
		if word[0]=='felvérez': print(word)
		if len(word)>1 and word[0]==word[1] and word[0]==word[0].lower() and 'PREV' not in word[3]:
			#if 'PREV' in word[3] and '+' not in word[3]: print(word)
			words.append((int(word[7]), word[0], word[3]))
			i+=1
		if i>=100000:
			break

words.sort()
with open('oft3.txt', 'w') as oft:
	for word in words:
		oft.write(f'{word[0]} {word[1]} {word[2]}\n')
print('ready')