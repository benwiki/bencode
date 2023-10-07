text=open("collemma.txt", 'r').readlines()
for i in range(len(text)):
	text[i]=text[i].lower()
text.sort()
for i in range(15):
	print (text[i], end='')
inp=input()
while inp!='mehet':
	inp=input()
back=open('collemma.txt', 'w')
for word in text:
	back.write(word)
back.close()