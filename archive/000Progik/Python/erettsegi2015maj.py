#1. feladat ----
vetel = [list(map(int, item.split())) if len(item)<10 else item for item in open("veetel.txt", "r")]

group = [[vetel[i*2], vetel[i*2+1]] for i in range(int(len(vetel)/2))]

#2. feladat ----
print("2. feladat")
print("Elso uzenet rogzitoje: ", group[0][0][1])
print("Utolso uzenet rogzitoje: ", group[-1][0][1])

#3. feladat ----
print("\n3. feladat")

group.sort(key=lambda li: li[0][0])

anyag = { i : { item[0][1] : item[1] for item in group if item[0][0]==i } for i in range(1, group[-1][0][0]+1) }

get = [[day[0], idms[0]] for day in anyag.items() for idms in day[1].items() if "farkas" in idms[1]]
for item in get:
    print ("{}.nap, {}.radioamator".format(item[0], item[1]))

#4. feladat ----

print("\n4. feladat")

for day in anyag.items():
	if len(day[1])>0:
		print("{}.nap: {} radioamator".format(day[0], len(day[1])))
	else:
		print("{}.nap: 0 radioamator".format(day[0]))

#5.feladat ----

adas=[]
for day in anyag.values():
	ms=["#" for i in range(90)]
	for curms in day.values():
		ms=[curms[i] if curms[i]!="#" else ms[i] for i in range(len(curms))]
	adas.append(''.join(ms))

out = open("adaas.txt", 'w')
for item in adas:
    out.write(item)
out.close()

#6. feladat

def szame(s):
    for c in s:
        if c<'0' or c>'9':
            return False
    return True

#7. feladat

print("\n7. feladat")
gday = int(input("Nap sorszama: "))
gid = int(input("Radioamator sorszama: "))

strDB=uzenet=""
db=0

try:
	ms = anyag[gday][gid]
except KeyError:
	ms=""
	uzenet="Nincs ilyen adat"

for c in ms:
	if c.isdigit():
		strDB+=c
	elif c=="/":
		db=int(strDB)
		strDB=""
	elif c==" ":
		db+=int(strDB)
		break
	else:
		uzenet="Hibas formatum"
		break

if uzenet != "":
	print(uzenet)
else:
	print("{} db farkas volt aznap".format(db))