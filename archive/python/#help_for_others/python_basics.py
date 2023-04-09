
# ADATSZERKEZETEK

mirko = 21
#. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
lista = [1, 2, 3, 4, 5]
# append(lista) = 14
lista.append(14) # csak egy dolgot append-elhetsz egyszerre
lista += [12, 19]
print(lista) # [1, 2, 3, 4, 5, 14, 12, 19]
# #lista objektumon belül:
# def append(x):
#     hozzáadom a listához az x-et
#     kész
#. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
tup = (255, 0, 0)
tup += (23, 12) #tup = tup + ...
#. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .
dik = {"benke": 100, "mirko": 101}
print(dik["benke"] == 100) # True
print(dik["benke"]) # 100  csillagos 5-ös
dik["boró"] = 4325178
print(dik) # {'benke': 100, 'mirko': 101, 'boró': 4325178}
#---------------------------------------------------------------
# ELÁGAZÁSOK

if mirko < 21:
    print("Ne igyál alkoholt amerikában.")
elif mirko >= 100:
    print("Tesó te már halott vagy. Vagy nem?")
else:
    print("VEDELJ ÖCSÉM!!!")

try:
    print(cuccom)
except Exception:
    print("Valami gebasz van.")

#----------------------------------------------------------------
# CIKLUSOK
csako = 2

while csako <= 6:
    csako += 1
    print("Ennyi csákód van", csako)


for i in range(10, 15+1): # range(10, 15) -> [10, 11, 12, 13, 14, 15]
    print(i)

for i in ["cucc", "bucc", 12, 73, 3.14159265]: # a range() helyére bármit rakhatsz, és az i helyére is
    print(i)

for _ in range(10):
    print("Ezt épp 10-szer akarom kiíratni, de rohadtul nem kell az indexváltozó hozzá hehehehehehe.")

#----------------------------------------------------------------
# FÜGGVÉNYEK
asd = 12
asd = str(asd)
asd = int(asd)
asd = float(asd)

print("Szép a fejem") # True

def append_hulyeseg(lista):
    lista.append("hehehehehe xddd")

emberek = ["egyik", "másik"]
append_hulyeseg(emberek)
print(emberek) # ['egyik', 'másik', 'hehehehehe xddd']

def yoshi(x):
    x *= 2
    return x

print(yoshi(3))

lista = [yoshi(123), yoshi(12)]

yoshi_magassaga = yoshi(3)

#.
