f= open("word_database.txt", "r")
for word in f:
	if word[-5:-1]=='szét':
		print(word, end='')