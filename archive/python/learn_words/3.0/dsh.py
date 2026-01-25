with open("dsh1.txt", "r", encoding="utf-8") as file:
    lines = [word.strip() for word in file]
with open("dsh_szavak.txt", "r", encoding="utf-8") as file:
    words = [word.strip() for word in file]

print(words, len(words), len(set(words)))
setwords = set(words)
zahl=0

def similar(given: str, correct: str, how=2):
    given, correct = given.lower(), correct.lower()
    return ( len(given)==len(correct) and
             sum(1 for L in given  if L in correct) >= len(correct)-how ) or \
             ( abs(len(given)-len(correct))<=how and
               all(L in correct for L in given) )
    
with open("dsh_szavak.txt", "w", encoding="utf-8") as file:
    for w in setwords:
        if all(w not in line for line in lines):
            file.write(w.lower()+"\n")
        else: zahl += 1
print(zahl)

