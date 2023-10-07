words=[word.strip() for word in open("word_database.txt", "r")]

listinlist=lambda a,b: all(aitem in b for aitem in a)
letters=['e','t','i','m','s','o','r','k','h','x','p']
got = [print(word) for word in words if listinlist(word, letters)]
