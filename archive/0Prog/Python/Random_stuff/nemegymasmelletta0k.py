count=0

def go (lim, list=None, k=0):
	global count
	if list is None: list=[0 for i in range(lim)]
	for i in range(2):
		list[k]=i
		if k>0 and list[k-1]==0 and i==0:
			continue
		else:
			if k==lim-1:
				print(list)
				yield 1
			else:
				yield from go(lim,list,k+1)
				
print(sum(g for g in go(13)))

