from newtrie import Trie, Crossword
from time import time

trie=Trie()
cw=Crossword(trie)

stop=time()
for word in open("word_database.txt","r"):
    trie.add(word.strip())
print(time()-stop)

stop=time()
find=cw.solutions(["időgéputazás", "pénzeszsák", "kutyaszorító",
		   "mindszentség", "kvintesszencia", "jómagyar",
		   "beszámíthatatlan", "kötelezettség"])

file = open("collected.txt", "w")
for f in find:
    file.write(f)
file.close()
print(time()-stop)
