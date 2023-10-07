from random import shuffle

nevek=['Géza f', 'Sz. István', 'O. Peti', 'Aba Sámuel', 'O. Peti', '1. András', '1. Béla', 'Salamon', '1. Géza', '1. szt Laci', 'K. Kálmán', '2. István', '2. Béla', '2. Géza', '3. István', '3. Béla', '1. Imre', '2. András', '4. Béla', '5. István', '4. k. Laci', '3. András','K. Robi']
evszam=[[972, 997],[997, 1038],[1038,1041],[1041,1044],[1044,1046],[1046,1060],[1060,1063],[1063,1074],[1074,1077],[1077,1095],[1095,1116],[1116,1031],[1131,1141],[1141,1162],[1162,1172],[1172,1196],[1196,1204],[1205,1235],[1235,1270],[1270,1272],[1272,1290],[1290,1301],[1308,1340]]

kozos=list(zip(nevek,evszam))
print(kozos)
while 1:
	shuffle(kozos)
	nevek = [e[0] for e in kozos]
	evszam = [e[1] for e in kozos]
	for i in range(23):
		input(nevek[i])
		print(evszam[i][0],'-',evszam[i][1])
		
		
		