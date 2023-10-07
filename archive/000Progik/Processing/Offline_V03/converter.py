table=["{"+",".join(line[:-1])+"}," for line in open("repello_table.txt", "r").readlines()]
table[0]="{"+table[0]
table[-1]+="}"
new=open("table.txt", "w")
for line in table:
	new.write(line+'\n')
new.close()