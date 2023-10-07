from math import factorial
from time import sleep
nums=[i for i in range(0, 3)]

def tear(arr, n):
	if len(arr)%n!=0:
		print ('Error: can\'t tear it apart')
		return arr
	ready=[[arr[i*n+j] for j in range(n)] for i in range(len(arr)//n)]
	return ready

def permutate(arr):
	done=True
	n, m=0,0
	L=len(arr)
	for i in range(L-2, -1, -1):
		if arr[i]<arr[i+1]:
			done=False
			n=i
			break
	print (arr)
	orig=arr.copy()
	for i in range(L-1, -1, -1):
		if arr[i]>arr[n]:
			m=i
			break
	arr[n], arr[m] = arr[m], arr[n]
	rev=list(reversed(arr[n+1:]))
	arr=arr[:n+1]+rev
	if done: return orig
	else: return orig+permutate(arr)
	
def permarray(arr):
	return tear(permutate(arr), len(arr))
	
cucc=permarray(nums)
print (cucc)