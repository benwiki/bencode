
names = open("hungarian_female_names.txt", "r", encoding="utf/8").readlines()
names_stripped = map(lambda n: n.strip(), names)

names_by_len: dict[int, list[str]] = {}
for name in names_stripped:
    name_length = len(name)
    names_by_len[name_length] = names_by_len.get(name_length, []) + [name]

while True:
    _name_len = input("\nName length: ")
    try:
        name_len = int(_name_len)
        print('> ' + '\n> '.join(names_by_len[name_len]))
    except ValueError:
        print(f"{_name_len} is not a number!")
    except KeyError:
        print(f"There are no names with length {name_len}.")
