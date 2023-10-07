import random
from math import sqrt
from time import sleep

class ProjectEuler:
	
	def __init__(self):
		self.qucc=7382
		pass
		
	def p(self, stuff):
		
		
	def m1(self):
		#codeless:
		#print((3+999)*333/2+(5+995)*199/2-(15+990)*66/2)
		print('first', sum(i for i in range(1,1000) if i%3==0 or i%5==0))

	def m2(self):
		i, j = 1, 2
		sum=0
		while j < 4000000:
			if j%2==0: sum+=j
			i, j = j, i+j
		print('second', sum)
		
	def m3(self):
		num=600851475143
		factors=[]
		while not self._isPrime(num):
			for i in range(3, int(sqrt(num)), 2):
				if num%i==0:
					factors.append(i)
					num/=i
					num=int(num)
					break
			else: break
		factors.append(num)
		print('third', max(factors))
	
	def m4(self):
		def palindrome(n):
			L=list(map(int, list(str(n))))
			if L[:len(L)//2]==list(reversed(L[len(L)//2:])):
				return True
			return False
		for period in range(9):
			for i in range(999, 100-1, -1):
				for j in range(999-period*100, 100+(8-period)*100-1, -1):
					if palindrome(i*j):
						print('fourth', i*j)
						break
				else: continue
				break
			else: continue
			break
	
	def m5(self):
		#codeless
		print('fifth', (2**4)*(3**2)*5*7*11*13*17*19)
		
	def m6(self):
		print('sixth', sum(i*j for i in range(1, 101) for j in range(1, 101) if i!=j))
		
	def m7(self):
		return
		pnum=2
		p=3
		while pnum!=10001:
			p+=2
			if self._isPrime(p, 10):
				print('\r', p, pnum, end='')
				pnum+=1
		print('\rseventh', p, ' '*10)
		
	def m8(self):
		num="7316717653133062491922511967442657474235534919493496983520312774506326239578318016984801869478851843858615607891129494954595017379583319528532088055111254069874715852386305071569329096329522744304355766896648950445244523161731856403098711121722383113622298934233803081353362766142828064444866452387493035890729629049156044077239071381051585930796086670172427121883998797908792274921901699720888093776657273330010533678812202354218097512545405947522435258490771167055601360483958644670632441572215539753697817977846174064955149290862569321978468622482839722413756570560574902614079729686524145351004748216637048440319989000889524345065854122758866688116427171479924442928230863465674813919123162824586178664583591245665294765456828489128831426076900422421902267105562632111110937054421750694165896040807198403850962455444362981230987879927244284909188845801561660979191338754992005240636899125607176060588611646710940507754100225698315520005593572972571636269561882670428252483600823257530420752963450"
		digits=num[:13]
		from functools import reduce
		prod=reduce(lambda x,y:x*y, [int(L) for L in digits])
		maxprod=prod
		
		for i in range(13, len(num)):
			digits=num[i-12:i+1]
			prod = reduce(lambda x,y:x*y, map(int, digits))
			if prod > maxprod and "0" not in digits:
				maxprod=prod
				
		print('eight', maxprod)
		
	def m9(self):
		from math import sqrt
		for i in range(100, 400):
			for j in range(i+1, 400):
				k=sqrt(i**2+j**2)
				if k%1==0 and i+j+int(k)==1000:
					print("nineth", int(i*j*k))
					return
	
	def mm1(self):
		print(2+3+sum(i for i in range(5, 2000000, 2) if self._isPrime(i, 5)))
	#~~~~~~~~~~~~~~~~~~~~
	def _isPrime(self, n, k=40):
	    if n == 2:
	        return True

	    if n % 2 == 0:
	        return False

	    r, s = 0, n - 1
	    while s % 2 == 0:
	        r += 1
	        s //= 2
	        
	    for _ in range(k):
	        a = random.randrange(2, n - 1)
	        x = pow(a, s, n)
	        if x == 1 or x == n - 1:
	            continue
	        for _ in range(r - 1):
	            x = pow(x, 2, n)
	            if x == n - 1:
	                break
	        else:
	            return False
	    return True

	    
pe=ProjectEuler()
attrs=(getattr(pe, x) for x in dir(pe) if not x.startswith('_'))
for method in attrs:
	if callable(method): method();