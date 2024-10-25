with open("/Users/benke/Downloads/word_database.txt", "r", encoding="utf-8") as file:
    words = file.read().splitlines()

for word in words:
    if word.endswith("u"):
        print(word)