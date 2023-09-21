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
        Numeric
            int
                >>> numBicycles = -2
                >>> numGlasses = 2
            float
                >>> percentReady = 0.01
            complex
                >>> relationships = 5 + 12j
                >>> myGF = 1j
        String
            >>> spruch = "Uebung macht den Meister"
            >>> spruch = 'Uebung macht den Meister'
        Bool
            >>> youGuysAreTheBest = True
        None
            >>> money = None
        OPs
            Arithmetic OPs
                + (plus)
                    >>> numBicycles + numGlasses # 0
                    >>> "Kartoffel" + "salat" # ???
                        LOESUNG
                            "Kartoffelsalat"
                    >>> 1j + 3 + 0.5j # (3+1.5j)
                - (minus)
                    >>> numBicycles - numGlasses # 4
                    >>> 1j - 2 - 4j # (-2-3j)
                    >>> "Kartoffel" - "salat" # ???
                        LOESUNG
                            TypeError :P
                * (times)
                    >>> 4+1j * 2+3j # ???
                        LOESUNG
                            (4+5j)
                    >>> ???  # (5+14j)
                        LOESUNG
                            >>> (4+1j) * (2+3j) 
                    >>> "hey"*3 # ???
                        LOESUNG
                            "heyheyhey"
                / (division)
                    >>> 3 / 4 # 0.75
                    >>> 3 / 0 # ???
                        LOESUNG
                            ZeroDivisionError
                    >>> "hey" / 3 # ???
                        LOESUNG
                            TypeError ¯\_(ツ)_/¯
                    >>> 2j / 1j # (2+0j)
                        >>> (1+2j) / (3+4j) # (0.44+0.08j)
                        (a+bj) / (c+dj) <=> ???
                            LOESUNG
                                ( (ac + bd) + (bc - ad)j ) / (c^2 + d^2)
                % (modulo)
                    >>> 0 % 2 # 0
                        >>> 1 % 2 # 1
                        >>> 2 % 2 # 0
                        >>> 3 % 2 # 1
                    >>> -1 % 2 # 1 !!!
                    >>> 1 % -2 # ???
                        LOESUNG
                            -1
                    >>> 0.7 % 0.5 # 0.2
                ** (exponent)
                    >>> 2**3 # 8
                    >>> -2**3 # ???
                        LOESUNG
                            -8
                    >>> 0**0 # ???
                        LOESUNG
                            1
                    >>> (2+3j) ** 2 # (-5+12j)
                    ALTERNATIV: pow
                        pow(x, y) <=> (x ** y)
                        pow(x, y, z) <=> (x ** y) % z
                            pow ist schneller!
                            >>> (120**12345678) % 31 #...
                                Dauert ewig
                            >>> pow(120, 12345678, 31) # 2
                                Sofort fertig
                // (floor div.)
                    >>> 10 // 3 # 3
                    >>> 1 // 3 # ???
                        LOESUNG
                            0
                    Minuszahlen
                        Gegen -inf. gerundet!
                        >>> -1 // 2 # ???
                            LOESUNG
                                -1
                        >>> 1 // -2 # ???
                            LOESUNG
                                -1
                        >>> -1 // -2 # ???
                            LOESUNG
                                0
                    >>> 1 // 0 # ???
                        LOESUNG
                            ZeroDivisionError :)
            Conversions
                str(x)
                    >>> str(4) # "4"
                    >>> str(4.86) # "4.86"
                    >>> str(1+2j) # "1+2j"
                    Umw. des Z.systems
                        >>> bin(170) # "0b10101010"
                        >>> oct(170) # "0o252"
                            (0)10-> 2, 101-> 5, 010-> 2
                            3 
                        >>> hex(170) # "0xaa
                            1010-> a, 1010-> a
                int(x)
                    >>> int(4.86) # 4
                    >>> int(4.26) # 4
                    >>> int("23") # 23
                    Umw. des Z.systems
                        >>> int("10101010"), 2
                            170
                        >>> int("2222", 4)
                            170
                        >>> int("252", 8)
                            170
                        >>> int("aa", 16)
                            170
                        >>> int("hey", 36) # 22570
                float(x)
                    >>> float(4) # 4.0
                    >>> float("4") # 4.0
                    >>> float("4.86") # 4.86
                complex(re, im) / complex(str)
                    >>> complex(2, 3) # (2+3j)
                    >>> complex("2+3j") # (2+3j)
            Math
                abs(x)
                    >>> abs(3), abs(-3) # 3 3
                    >>> abs(3+4j)  # ???
                        LOESUNG
                            5.0
                c.conjugate()
                    >>> (3+4j).conjugate() # ???
                        LOESUNG
                            (3-4j)
                divmod(x, y)
                    <=> (x // y, x % y)
                    nuetzlich in 2D
                        >>> matrix = [[0, 1], [2, 3], [4, 5]]
                        >>> n, m = 2, 3
                        >>> i, j = divmod(4, n)
                        >>> matrix[i][j] # 4
                math.floor(x)
                    >>> math.floor(4.86) # 4
                    >>> math.floor(4.26) # 4
                    x float => (math.floor(x) <=> int(x))
                math.ceil(x)
                    >>> math.ceil(4.26) # ???
                        LOESUNG
                            5
                math.trunc(x)
                    >>> math.trunc(4.56) # 4
                        x > 0 => (math.trunc(x) <=> math.floor())
                    >>> math.trunc(-4.56) # -4
                        x < 0 => (math.trunc(x) <=> math.ceil())
                round(x)
                    >>> round(4.86) # 5
                    >>> round(4.26) # 4
                    x.5 nach gerade
                        >>> round(4.5) # 4
                        >>> round(5.5) # 6
                    >>> round(3.14159265, 2)  # 3.14
            Assignment OPs
                x = 2
                    "=" bei Variablen: copy
                        >>> x = 2
                        >>> y = x
                        >>> y = y + 5
                        >>> x # ???
                            LOESUNG
                                2
                    x, y = 1, 2
                        x, y, z = 3, 2, 1 ...
                        Tuple unpacking (spaeter)
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
                >>> greeting # ???
                    "Hello!"
                >>> sentence
                    "Hello! My name is Bob."
            (tuple,)
                >>> coords = (3, 1)
                >>> pi = coords
                >>> pi += (4,)
                >>> coords # ???
                    LOESUNG
                        (3, 1)
                >>> pi
                    (3, 1, 4)
            range(x, y, z)
                range(end)
                    range(5) ~ 0, 1, 2, 3, 4
                    Startet bei 0
                    "Ausschließend" (exclusive)
                        nimmt 'end' nicht rein
                        Slicing auch ausschließend!
                range(start, end)
                    range(2, 5) ~ 2, 3, 4
                range(start, end, step)
                    range(2, 10, 2) ~ 2, 4, 6, 8
        Mutables
            [list]
                z.B. columbus = [30, 11]
                churchill = columbus
                churchill += [1874]
                >>> columbus # ???
                    LOESUNG
                        [30, 11, 1874]
                        Grund: Referenz!
        OPs
            Union & Mult.
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
                        >>> a # [[], [], []]
                        a[0].append(3) # a = ???
                            Referenz wurde kopiert!
                            LOESUNG
                                [[3], [3], [3]]
            Slicing
                seq[i]
                    Indexierung beginnt mit 0
                        ... wie range(end)
                    >>> nums = [1, 2, 3]
                    >>> nums[1] # 2 !!!
                    >>> obst = "apfel"
                    >>> obst[2] # ???
                        LOESUNG
                            'f'
                seq[i:j]
                    >>> "apfel"[1:3] # "pf"
                        "Ausschließend"!!!
                    >>> "apfel"[1:] # "pfel"
                    >>> "apfel"[:3] # "apf"
                    >>> "apfel"[:] # ???
                        LOESUNG
                            'apfel'
                        seq[:] equivalent zu seq.copy()
                seq[i:j:k]
                    >>> "apfel"[0:4:2] # "af"
                    >>> "apfel"[0:5:2] # "afl"
                    >>> "apfel"[0:5:3] # "ae"
                    >>> "apfel"[0:5:1] # "apfel"
            Elements
                el in seq
                    >>> 2 in [7, 4, 2] # True
                    >>> 2 in [8, 3, 6] # False
                    >>> 'a' in "apfel" # True
                    >>> 'fel' in "apfel" # True
                        SUBstring testing
                    >>> 'ku' in "apfel" # False
                el not in seq
                    >>> 2 not in [7, 4, 2] # False
                    >>> 2 not in [8, 3, 6] # True
                    >>> 'a' not in "apfel" # False
                    >>> 'pfe' not in "apfel" # False
                    >>> 'ku' not in "apfel" # True
                len(seq)
                    >>> len([1, 2, 3, 4]) # 4
                    >>> len("apfel") # 5
                min(seq)
                    >>> min([4, 2, 5]) # 2
                    >>> min("apfel") # 'a'
                max(seq)
                    >>> max([4, 2, 5]) # 5
                    >>> max("apfel") # 'p'
                seq.count(el)
                    >>> [3, 5, 3, 5, 5, 5].count(3) # 2
                    >>> [3, 5, 3, 5, 5, 5].count(5) # 4
                    >>> "Hello there!".count('e') # 3
                    >>> range(2, 4).count(2)  # ???
                        LOESUNG
                            1
            Index
                seq.index(el)
                seq.index(el, i)
                seq.index(el, i, j)
    Iterator
        Methods
            next(iterator)
            iter(seq)
                seq -> iterator
        Generator
    Mapping
        dict
    Set
        set
        frozenset
    Binary
        bytes
        bytearray
        memoryview
        bitwise OPs
            & (and)
                >>> 11 & 6 # 2
                    szs. 1011 & (0)110
                    ~ 1&0 0&1 1&1 1&0
                    ~ 0010
                    ~ 2
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
                a == b
                a != b
                a < b
                a > b
                a <= b
                a >= b
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
                    Prioritaet < als non-bool OPs
                        not a == b <=> not (a == b)
                        a == not b # ???
                            Syntax Error
            identity
                is
                    meistens mit None
                    if money is None: ...
                is not
            membership
                in
                    >>> 1 in [1, 2] # True
                    >>> 1 in (1, 2) # True
                    >>> "1" in "12" # True
                    >>> 1 in range(1,2) # True
                    >>> 1 in {1: 2, 3: 4} # True
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