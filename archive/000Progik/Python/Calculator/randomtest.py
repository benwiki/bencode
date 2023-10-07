words = open("word_database.txt", "r")
print("ok")
#words=['kleo', "hej"]


for word in words:
	for i in range(len(word)-1):
		if word[i:i+2]=="kl":
			print(word)
			break