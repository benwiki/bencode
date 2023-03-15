```mindmap
Data structures
	variable
		numeric
			int
				numFish = 0
				numGlasses = 2
			float
				percentReady = 0.01
			complex
				relationships = 5 + 12j
				myGF = 1j
		string
			saying = "Rede mir kein Vesper in die Tasche!"
		bool
			youGuysAreTheBest = True
		None
			money = None
		arithmetic OPs
			+ (plus)
				print(numFish + numGlasses) # 2
				print(num_of_fish + 3) # 3
				print(1j + 3 + 0.5j) # (3+1.5j)
			- (minus)
				print(numGlasses - 2) # 0
				print(1j - 2 - 4j) # (-2-3j)
			* (times)
				print(4+1j * 2+3j) # ???
					(4+5j)
				print( ??? ) # (5+14j)
					LOESUNG
						print( (4+1j) * (2+3j) )
				print("hey"*3) # ???
					LOESUNG
						"heyheyhey"
			/ (division)
				print(3/4) # 0.75
			% (modulo)
				print(0 % 2) # 0
				print(1 % 2) # 1
				print(2 % 2) # 0
				print(3 % 2) # 1...
				print(-1 % 2) # 1 !!!
				print(1 % -2) # ???
					-1
			** (exponent)
			// (floor div.)
		assignment OPs
			x = 2
			x += 2
			x -= 2
			x *= 2
			x /= 2
			x %= 2
			x **= 2
			x //= 2
	iterator
	sequence
		sind *Objekten* (ausser string)
			bei Variablen
				int
					aepfel = 5
					birnen = aepfel
					birnen += 3
					print(aepfel) # ???
						5
					print(birnen)
						8
				string
					greeting = "Hello!"
					sentence = greeting
					sentence += " My name is Bob."
					print(greeting) # ???
						"Hello!"
					print(sentence)
						"Hello! My name is Bob."
				float, complex, bool ebenso
			bei Objekten
				z.B. columbus = [30, 11]
				churchill = columbus
				churchill += [1874]
				print(columbus) # ???
					[30, 11, 1874]
		list
		tuple
		range (!!!)
			kein union & mult.
				aber alles andere schon
			print( range(2, 4).count(2) ) # ???
				1
		(string)
		OPs
			union & mult.
				seq1 + seq2
					[1, 3] + [2, 4] = ???
						LOESUNG
							[1, 3, 2, 4]
						"ap" + "fel" = "apfel"
				seq * n oder n * seq
					[4, 5] * 3 = ???
						LOESUNG
							[4, 5, 4, 5, 4, 5]
						"apfel" * 3 = "apfelapfelapfel"
					Referenz! KEIN copy!
						a = [ [] ]*3
							print(a) # [[], [], []]
							a[0].append(3) # a = ???
								Referenz: das gleiche Objekt
								LOESUNG
									[[3], [3], [3]]
			slicing
				seq[i]
				seq[i:j]
					"apfel"[1:3] = "pf"
					"apfel"[1:] = "pfel"
					"apfel"[:3] = "apf"
					"apfel"[:]
						LOESUNG
							"apfel"
						seq[:] equivalent zu seq.copy()
				seq[i:j:k]
					"apfel"[0:4:2] = "af"
					"apfel"[0:5:2] = "afl"
					"apfel"[0:5:3] = "ae"
					"apfel"[0:5:1] = "apfel"
			elements
				el in seq
					2 in [7, 4, 2] = True
					2 in [8, 3, 6] = False
					'a' in "apfel" = True
					'pfe' in "apfel" = True
					'kl' in "apfel" = False
				el not in seq
					2 not in [7, 4, 2] = False
					2 not in [8, 3, 6] = True
					'a' not in "apfel" = False
					'pfe' not in "apfel" = False
					'kl' not in "apfel" = True
				len(seq)
					len( [1, 2, 3, 4] ) = 4
					len( "apfel" ) = 5
				min(seq)
					min( [4, 2, 5] ) = 2
					min( "apfel" ) = 'a'
				max(seq)
					max( [4, 2, 5] ) = 5
					max( "apfel" ) = 'p'
				seq.count(el)
					[3, 5, 3, 5, 5, 5].count(3) = 2
					[3, 5, 3, 5, 5, 5].count(5) = 4
					"Hello there!".count('e') = 3
			index
				seq.index(el)
				seq.index(el, i)
				seq.index(el, i, j)
	mapping
		dict
	set
		set
		frozenset
	binary
		bytes
		bytearray
		memoryview
		bitwise operators
			& (and)
			| (or)
			^ (xor)
			~ (not)
			<< (zero fill LEFT shift)
			>> (signed RIGHT shift)
		bitwise assignment
			x &= 21
			x |= 21
			x ^= 21
			x <<= 3
			x >>= 3
Branchings
	if-elif-else
		comparison
			!=
			==
			<
			>
			<=
			>=
		logic
			and
			or
			not
		identity
			is
			is not
		membership
			in
			not in
	try-except-else-finally
	match
Loops
	for-in-else
	while-else
Functions
Classes & objects
```