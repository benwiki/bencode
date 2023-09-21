```mindmap
Data structures
    Built-in Constants
        True <True>
        False <False>
        None <False>
        Ellipsis / ... <True>
        quit, exit <True>
        Was ist diese <???>
            "Truth Value Testing"
            kommt bei Verzweigungen
    Variables
        numeric
            int
                numBicycles = -2
                numGlasses = 2
            float
                percentReady = 0.01
            complex
                relationships = 5 + 12j
                myGF = 1j
        String
            saying = "Rede mir kein Vesper in die Tasche!"
        Bool
            youGuysAreTheBest = True
        None
            money = None
        OPs
            Arithmetic OPs
                + (plus)
                    print(numBicycles + numGlasses) # 0
                    print("Kartoffel" + "salat") # ???
                        LOESUNG
                            "Kartoffelsalat"
                    print(1j + 3 + 0.5j) # (3+1.5j)
                - (minus)
                    print(numBicycles - numGlasses) # 4
                    print(1j - 2 - 4j) # (-2-3j)
                    print("Kartoffel" - "salat") # ???
                        LOESUNG
                            TypeError :P
                * (times)
                    print(4+1j * 2+3j) # ???
                        LOESUNG
                            (4+5j)
                    print( ??? ) # (5+14j)
                        LOESUNG
                            print( (4+1j) * (2+3j) )
                    print("hey"*3) # ???
                        LOESUNG
                            "heyheyhey"
                / (division)
                    print(3 / 4) # 0.75
                    print(3 / 0) # ???
                        LOESUNG
                            ZeroDivisionError
                    print("hey" / 3) # ???
                        LOESUNG
                            TypeError ¯\_(ツ)_/¯
                    print(2j / 1j) # (2+0j)
                        print((1+2j) / (3+4j)) # (0.44+0.08j)
                        (a+bj) / (c+dj) = ???
                            LOESUNG
                                ( (ac + bd) + (bc - ad)j ) / (c^2 + d^2)
                % (modulo)
                    print(0 % 2) # 0
                        print(1 % 2) # 1
                        print(2 % 2) # 0
                        print(3 % 2) # 1
                    print(-1 % 2) # 1 !!!
                    print(1 % -2) # ???
                        LOESUNG
                            -1
                    print(0.7 % 0.5) # 0.2
                ** (exponent)
                    print(2**3) # 8
                    print(-2**3) # ???
                        LOESUNG
                            -8
                    print(0**0) # ???
                        LOESUNG
                            1
                    print((2+3j) ** 2) # (-5+12j)
                    ALTERNATIV: pow
                        pow(x, y) <=> (x ** y)
                        pow(x, y, z) <=> (x ** y) % z
                            pow ist schneller!
                            print( (120**12345678) % 31 ) #...
                                Dauert ewig
                            print( pow(120, 12345678, 31) ) # 2
                                Sofort fertig
                // (floor div.)
                    print(10 // 3) # 3
                    print(1 // 3) # ???
                        LOESUNG
                            0
                    Minuszahlen
                        Gegen -inf. gerundet!
                        print(-1 // 2) # ???
                            LOESUNG
                                -1
                        print(1 // -2) # ???
                            LOESUNG
                                -1
                        print(-1 // -2) # ???
                            LOESUNG
                                0
                    print(1 // 0) # ???
                        LOESUNG
                            ZeroDivisionError :)
            Conversions
                str(x)
                    print(str(4)) # "4"
                    print(str(4.86)) # "4.86"
                    print(str(1+2j)) # "1+2j"
                    Umw. des Z.systems
                        print(bin(170)) # "0b10101010"
                        print(oct(170)) # "0o252"
                            (0)10-> 2, 101-> 5, 010-> 2
                            3 
                        print(hex(170)) # "0xaa
                            1010-> a, 1010-> a
                int(x)
                    print(int(4.86)) # 4
                    print(int(4.26)) # 4
                    print(int("23")) # 23
                    Umw. des Z.systems
                        print(int("10101010"), 2)
                            170
                        print(int("2222", 4))
                            170
                        print(int("252", 8))
                            170
                        print(int("aa", 16))
                            170
                        print(int("hey", 36)) # 22570
                float(x)
                    print(float(4)) # 4.0
                    print(float("4")) # 4.0
                    print(float("4.86")) # 4.86
                complex(re, im) / complex(str)
                    print(complex(2, 3j)) # (2+3j)
                    print(complex("2+3j")) # (2+3j)
            Math
                abs(x)
                    print(abs(3), abs(-3)) # 3 3
                    print( abs(3+4j) ) # ???
                        LOESUNG
                            5.0
                c.conjugate()
                    (3+4j).conjugate() # ???
                        LOESUNG
                            (3-4j)
                divmod(x, y)
                    <=> (x // y, x % y)
                    nützlich: 2D
                        matrix = [[0, 1], [2, 3], [4, 5]]
                        n, m = 2, 3
                        i, j = divmod(4, n)
                        print(matrix[i][j]) # 4
                math.floor(x)
                    print(math.floor(4.86)) # 4
                    print(math.floor(4.26)) # 4
                    x float => (math.floor(x) <=> int(x))
                math.ceil(x)
                    print(math.ceil(4.26)) # ???
                        LOESUNG
                            5
                math.trunc(x)
                    print(math.trunc(4.56)) # 4
                        x > 0 => (math.trunc(x) <=> math.floor())
                    print(math.trunc(-4.56)) # -4
                        x < 0 => (math.trunc(x) <=> math.ceil())
                round(x)
                    print(round(4.86)) # 5
                    print(round(4.26)) # 4
                    x.5 nach gerade
                        print(round(4.5)) # 4
                        print(round(5.5)) # 6
                    print( round(3.14159265, 2) ) # 3.14
            Assignment OPs
                x = 2
                    "=" bei Variablen: copy
                        x = 2
                        y = x
                        y = y + 5
                        print(x) # ???
                            LOESUNG
                                2
                    x, y = 1, 2
                    x und y vertauschen?
                        LOESUNG
                            x, y = y, x
                x += 2
                    <=> x = x + 2
                x -= 2
                    <=> x = x - 2
                x *= 2
                    <=> x = x * 2
                x /= 2
                    <=> x = x / 2
                x %= 2
                    <=> x = x % 2
                x **= 2
                    <=> x = x ** 2
                x //= 2
                    <=> x = x // 2
    Sequence; 100
        Immutables
            "string"
                greeting = "Hello!"
                sentence = greeting
                sentence += " My name is Bob."
                print(greeting) # ???
                    "Hello!"
                print(sentence)
                    "Hello! My name is Bob."
            (tuple,)
                coord
            range(x, y, z)
                kein union & mult.
                    aber alles andere schon
        Mutables
            [list]
                z.B. columbus = [30, 11]
                churchill = columbus
                churchill += [1874]
                print(columbus) # ???
                    [30, 11, 1874]
                    Grund: mutability
        OPs
            union & mult.
                seq1 + seq2
                    [1, 3] + [2, 4] = ???
                        LOESUNG
                            [1, 3, 2, 4]
                        "ap" + "fel" = "apfel"
                seq * n (n * seq)
                    [4, 5] * 3 = ???
                        LOESUNG
                            [4, 5, 4, 5, 4, 5]
                        "apfel" * 3 = "apfelapfelapfel"
                    Was passiert bei mutables?
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
                        SUBstring testing
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
                    print( range(2, 4).count(2) ) # ???
                        LOESUNG
                            1
            index
                seq.index(el)
                seq.index(el, i)
                seq.index(el, i, j)
    Iterator
        Methods
            next(iterator)
            iter(seq)
                seq -> iterator
        Generator
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
        Secret tricks
        OPs
            comparison
                !=
                ==
                <
                >
                <=
                >=
            logic
                and
                    short-circuit eval.
                        a = 5
                        if a < 5 and 2/(a-5) < 1...
                            vollkommen gut so
                            2/(a-5) = 2/0 # ???
                                wenn a < 5 Falsch, der Teil nach "and"
                                ...wird gar nicht ausgewertet
                or
                    short-circuit eval.
                        a = 5
                        if a >= 5 or 2/(a-5) < 1...
                            dasselbe Effekt
                        BILD
                not
                    Priorität < als non-bool OPs
                        not a == b <=> not (a == b)
                        a == not b # ???
                            Syntax Error
            identity
                is
                    meistens mit None
                    if money is None...
                is not
            membership
                in
                    1 in [1, 2] = True
                    1 in (1, 2) = True
                    "1" in "12" = True
                    1 in range(1,2) = True
                    1 in {1: 2, 3: 4} = True
                        E in dict <=> E in dict.keys() !!!
                not in
    try-except-else-finally
    match
Loops
    for-in-else
    while-else
Functions
Classes & objects
```