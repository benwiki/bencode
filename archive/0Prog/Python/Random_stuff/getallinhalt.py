raw=[1, 2, 3]
group={raw[0]:{raw[1]:{raw[2]:{}}}}
h = lambda L: [L]+h(list(L.values())[0]) if len(L)>0 else [L]
print (h(group))