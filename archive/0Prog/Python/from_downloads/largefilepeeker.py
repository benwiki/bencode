with open('html (1).lst', encoding="utf-8") as f:
	print(''.join(f.readline() for _ in range(35000)))