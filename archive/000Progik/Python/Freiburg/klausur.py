from dataclasses import dataclass

@dataclass
class Node:
	id: int
	children: list
	
print([Node(3, []), Node(4, []), Node(5, [])])
#from functools import cache

fib = lambda n: ([-fib(x) for x in range(-1, -n-1, -1)] if n>=0 else fib(n+1)+fib(n+2) if n < -2 else n+1)

#print(fib(25))

from math import sqrt
def is_prime(n: int):
	return n!=1 and n!=0 and n%2!=0 and not any(n % x == 0 for x in range(3, int(sqrt(n))+1, 2)) or n==2
	
print(is_prime(33))





def howmanytimes(n, a):
	count = 0
	while n < a:
		if n%2==0:
			n \\= 2
		else:
			n = 9*n+3
	return count

@dataclass
class Node:
	mark: str
	left: "Node"
	right: "Node"
	
	
ex = Node(1,
					Node(2, None, None),
					Node(3,
								Node(4, None, None),
								Node(5, None, None)))
	
def paths(tree: Node):
	out = [""]
	if isinstance(tree.left, Node):
		out.extend(['l'+L for L in paths(tree.left)])
	if isinstance(tree.right, Node):
		out.extend(['r'+L for L in paths(tree.right)])
	return out
	
print(paths(ex))

def matrix2(f, m):
	return list(map(lambda row: list(map(f, row)), m))
	
	def m(f, m):
		return ([map(f(x)), x]for x in m);