```mindmap
Data structures
    variable
        numeric
            int
            float
            complex
        string
        bool
        None
        arithmetic OPs
            + (plus)
            - (minus)
            * (times)
            / (division)
            % (modulo)
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
        list
        tuple
        range
        (string)
        OPs
            union & mult.
                seq1 + seq2
                    [1, 3] + [2, 4] =
                        LOESUNG
                            [1, 3, 2, 4]
                        "ap" + "fel" = "apfel"
                seq * n oder n * seq
                    [4, 5] * 3 =
                        LOESUNG
                            [4, 5, 4, 5, 4, 5]
                        "apfel" * 3 = "apfelapfelapfel"
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
            elements;70
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
    set;96
        set
        frozenset
    binary
        bytes;40
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