import json
import re
import pprint
from simplemma.simplemma import lemmatize

# with open('fiwiktionary-20230820-pages-articles-multistream.xml', 'r', encoding='utf-8') as f:
#     data_dict = xmltodict.parse(f.read())
# print('1')
# json_data = json.dumps(data_dict)
# print('2')
# open('definitions.json', 'w', encoding='utf-8').write(json_data)

with open('definitions.json', 'r', encoding='utf-8') as f:
    json_obj = json.loads(f.read())

# print(str(json_obj)[20_000_000:20_020_000])

# def explore(obj, name="", counter=0) -> int:
#     m = 0
#     match obj:
#         case dict():
#             print(name, list(obj.keys()), flush=True)
#             m = 0
#             for key, val in obj.items():
#                 if (n := explore(val, name=key)) > m:
#                     m = n
#             return m + 1
#         # case list():
#         #     print(name, len(obj), flush=True)
#         #     m = 0
#         #     for val in obj:
#         #         if (n := explore(val, counter=counter+1)) > m:
#         #             m = n
#         #     return m + 1
#         case _:
#             print(name, type(obj), "#")
#             return 1

# print(explore(json_obj))


pages: list[dict] = json_obj['mediawiki']['page']

print(1)

collection = {}

for i, page in enumerate(pages):
    # print('--------------------------------------------------')
    # print(page.get('title', '_'))
    # print('--------------------------------------------------')
    text1 = page['revision']['text']
    text1 = text1.get('#text', '')
    
    if "==Suomi==" not in text1:
        continue
    
    text1_5 = text1.split('==Suomi==')[1]
    text2 = text1_5.split('====Ääntäminen====')[0]
    text3 = text2.split('===')[:3][-1]
    text = text3.split('<gallery>')[0]

    text = re.sub(r'\{\{[^\{]+\}\}', '', text)
    text = re.sub(r'\[\[([^\[]+)\|[^\]]+\]\]', r'\1', text)
    text = text.replace('[', '').replace(']', '')
    text = text.replace('#:', '').replace('#', '')
    text = text.replace('\'', '').replace('\n', '')
    text = text.upper()
    text = re.sub(r'[^\wÖÜÄÅ ]+', '', text)
    
    for word in filter(lambda x: x != '', text.split(' ')):
        lemmatized = lemmatize(word, lang='fi')
        collection[lemmatized] = collection.get(lemmatized, 0) + 1

print(3)

# with open('collection.txt', 'r', encoding='utf-8') as f:
    # collection = eval(f.read())

collection = sorted(list(collection.items()), key=lambda x: x[1], reverse=True)
collection_text = '\n'.join(' '.join(pair) for pair in collection)

with open('words.txt', 'w', encoding='utf-8') as f:
    f.write(collection_text)

# open('collection.txt', 'w', encoding='utf-8').write(str(collection))

# print(type(obj))
# pprint.pprint(obj[200:203])
