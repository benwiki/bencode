elso = [5 for i in range(10)]
print("1. ", elso)

masodik = [i for i in range(10)]
print("2. ", masodik)

harmadik = [i**2 for i in range(10)]
print("3.   ", harmadik)
harmadik_2 = [i**2 for i in masodik]
print("3.2. ", harmadik_2, "ugyanaz ¯\_(ツ)_/¯")

negyedik = [x for x in masodik if x<5]
print("4. ", negyedik)

otodik = [x if x<5 else 5 for x in masodik]
print("5. ", otodik)

hatodik = [x*y for x in elso for y in masodik]
"""
hatodik=[]
for x in elso:
	for y in masodik:
		hatodik.append(x*y)
"""
print('\n6.', hatodik)

hatodik_2 =[x*y for y in masodik for x in elso]
"""
hatodik=[]
for y in masodik:
	for x in elso:
		hatodik.append(x*y)
"""
print('\n6.2.', hatodik_2, "\n nem ugyanaz!!!!")
#a magyarázat jobban láttatja hogy miért nem ugyanaz a kettő 

otodik_es_hatodik =[True if x+y<10 else False for x in elso for y in masodik]
print(otodik_es_hatodik)
