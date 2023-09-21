with open('collection.txt', 'r', encoding='utf-8') as f:
    collection = eval(f.read())

collection = '\n'.join(elem[0] for elem in collection)

with open('words.txt', 'w', encoding='utf-8') as f:
    f.write(collection)