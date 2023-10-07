tavir = [[item if (len(item)==2 and not item.isnumeric()) else 
[item[0:3], int(item[3:])] if len(item)==5 else
int(item) if len(item)==2 else 
item[0:2]+":"+item[2:] 
for item in row.split() ] 
for row in open("tavirathu13.txt", "r")]

anyag = { item[0] : { inner[1] : [inner[2][0], inner[2][1], inner[3]] for inner in tavir if inner[0]==item[0] } for item in tavir }

#anyag={}
#[[(anyag.update({row[0]:{}}) if row[0] not in anyag.keys() else []),
#	(if ) for row in tavir]

varos = input("2. feladat\nVaros neve: ")
try:
	print("Az utolso meres idopontja:",list(anyag[varos].items())[-1][0])
except:
	print("Nincs ilyen varos")
	
print("3. feladat")
hom = [[varos[0], data[0], data[1][2]] for varos in anyag.items() for data in varos[1].items()]
k = lambda a: a[2]
print("Legalacsonyabb homerseklet: {} {} {} fok".format(*min(hom, key=k)))
print("Legmagasabb homerseklet: {} {} {} fok".format(*max(hom, key=k)))

print("4.feladat")
[print(varos[0], data[0]) for varos in anyag.items() for data in varos[1].items() if data[1][0]=="000" and data[1][1]==0]

print("5.feladat")
avg = lambda L: round(sum(L)/len(L))
listinlist=lambda a, b: all(aitem in b for aitem in a)
times=['01', '07', '13', '19']

valid=[varos[0] for varos in anyag.items() if listinlist(times, [ido[0][:2] for ido in varos[1].items()])]

maxbolmin=lambda a: max(a)-min(a)
[print(
	varos[0], 
	"Kozephomerseklet:", 
	avg([ido[1][2] for ido in varos[1].items() if ido[0][:2] in times]) if varos[0] in valid else 'NA',
	"Ingadozas:", 
	maxbolmin([ido[1][2] for ido in varos[1].items()])) 
for varos in anyag.items()]

print("6.feladat")
[open(varos[0]+".txt", "w").write("\n".join([varos[0]]+[ido[0]+" "+"#"*ido[1][1] for ido in varos[1].items()])) for varos in anyag.items()]