num=56
to_bin = lambda num: list(reversed(map(int, str(bin(num))[2:]])))
print(to_bin(56))