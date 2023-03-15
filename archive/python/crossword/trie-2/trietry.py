from newtrie import Trie, Crossword
from time import time
import os

dir = os.path.realpath(__file__)
ind = dir[::-1].index("\\")
dir = dir[0:-ind]

trie = Trie()
cw = Crossword(trie)

stop = time()
for word in open(dir + "word_database.txt", "r"):
    trie.add(word.strip())
print(time() - stop)

stop = time()
find = cw.solutions(["időgéputazás", "pénzeszsák", "kutyaszorító",
                     "mindszentség", "kvintesszencia", "jómagyar",
                     "beszámíthatatlan", "kötelezettség", "cserediák"])

for f in find:
    print(f, end=' ', flush=True)
print(time() - stop)
