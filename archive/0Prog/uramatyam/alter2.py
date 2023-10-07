Eingabe = input()
Personen = Eingabe.split('\n\n')
Anzahl = int(Personen[0])
Personen.remove(Personen[0])
for x in range(Anzahl):
    y = x + 1
    current = Personen[x]  # index out of range?????
    liste = current.split('\n')
    letzterW = liste[0]
    gebD = liste[1]
    gebZ = int(gebD[6:]) * 10000 + int(gebD[3:5]) * 100 + int(gebD[:2])
    letZ = int(letzterW[6:]) * 10000 + int(letzterW[3:5]) * 100 + int(letzterW[:2])
    alterganz = letZ - gebZ
    if alterganz >= 10000:
        alter = str(alterganz)[:-4]
        inter = int(alter)
        if inter < 0:
            print('Person #' + str(y) + ': Ungueltiges Geburtsdatum')
            continue
        if inter > 130:
            print('Person #' + str(y) + ': Zu alt')
            continue
        else:
            print('Person #' + str(y) + ': ' + alter)
            continue
    if alterganz < 0:
        print('Person #' + str(y) + ': Ungueltiges Geburtsdatum')
    else:
        print('Person #' + str(y) + ': 0')
# 0
# 1\n\n01 01 2007\n10 02 2007
# 2\n\n01 01 2007\n10 02 2007\n\n09 06 2007\n28 02 1871
# 3\n\n01 01 2007\n10 02 2007\n\n09 06 2007\n28 02 1871\n\n12 11 2007\n01 01 1984
# 4\n\n01 01 2009\n10 02 2007\n\n09 06 2007\n28 02 1871\n\n12 11 2007\n01 01 1984\n\n28 02 2005\n29 02 2004
