########################################################

simple = [5 for i in range(10)]
"""
simple = []
for i in range(10):
    simple.append(5)
"""
print("simple: ", simple)
# ****************************************************************

same = [i for i in range(10)]
"""
same = []
for i in range(10):
    same.append(i)
"""
print("same: ", same)
# ****************************************************************

expression = [i*2 for i in range(10)]
"""
expression = []
for i in range(10):
    expression.append(i*2)
"""
print("expr:   ", expression)
# -------------------------------------------------------

expression_2 = [i*2 for i in same]
"""
expression_2 = []
for i in same:
    expression_2.append(i*2)
"""
print("expr_2: ", expression_2, "ugyanaz, mert a same-ben is számok vannak 0-9ig, \
ahogy a range(10)-ben is (az is egy iterable lényegében)")
# ****************************************************************
# ****************************************************************

filtered = [x for x in same if x < 5]
"""
filtered = []
for x in same:
    if x<5:
        filtered.append(x)
"""
print("filter (<5): ", filtered)
# ----------------------------------------------------

filtered_2 = [x for x in same if x < 5 or x > 6]
"""
filtered = []
for x in same:
    if x<5 or x>6:
        filtered.append(x)
"""
print("filter_2 (<5 or >6): ", filtered_2)
# ----------------------------------------------------

ifelse = [x if x < 5 else 5 for x in same]
"""
filtered = []
for x in same:
    if x<5:
        filtered.append(x)
    else:
        filtered.append(5)
"""
print("ifelse: ", ifelse)
# --------------------------------------------------------

multiple_if = [x if x < 5 else 5 if x < 7 else 7 for x in same]
"""
filtered = []
for x in same:
    if x<5:
        filtered.append(x)
    elif x<7:
        filtered.append(5)
    else:
        filtered.append(7)
"""
print("multiple_if: ", multiple_if)
# ...és ezt bármennyiszer megismételheted

# ****************************************************************
# ****************************************************************

nested = [x*y for x in simple for y in same]
"""
nested=[]
for x in simple:
    for y in same:
	nested.append(x*y)
"""
print('\nNested:', nested)
# ----------------------------------------------------------------

nested_2 = [x*y for y in same for x in simple]
"""
nested=[]
for y in same:
    for x in simple:
	nested.append(x*y)
"""
print('\nNested fordítva:', nested_2, "\n nem ugyanaz!!!!")
# a magyarázat jobban láttatja hogy miért nem ugyanaz a kettő
# -----------------------------------------------------------------

ifelse_nested = [x+y if x+y < 10 else 0 for x in simple for y in same]
"""
ifelse_nested = []
for x in simple:
    for y in same:
        if x+y<10:
            ifelse_nested.append(x+y)
        else:
            ifelse_nested.append(0)
"""
print("\nIfelse és nested:", ifelse_nested)
# ****************************************************************

xdim = 5
ydim = 10
multidim = [[x*ydim + y for y in range(ydim)] for x in range(xdim)]
"""
multidim = []
for x in range(xdim):
    multidim.append([])
    for y in range(ydim):
        multidim[x].append(x*ydim + y)
"""
print("\nmultidimensional:\n", multidim,
      '\nLast element: ', multidim[xdim-1][ydim-1], sep='')
# Itt az indexelés is be van mutatva - kiíratjuk a kétdimenziós tömb utsó elemét


# .
