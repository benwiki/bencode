import json
import re
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
# import xmltodict
# import pprint

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

wholeText = ""

for page in pages:
    #if i < 500: continue
    #if i > 550: break
    # print('--------------------------------------------------')
    # print(page.get('title', '_'))
    # print('--------------------------------------------------')
    text1: str = page['revision']['text'].get('#text', '')
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

    wholeText += f' {text} '

    # print(text, end='\n'*3)

for word in stopwords.words("finnish"):
    wholeText = wholeText.replace(f' {word.upper()} ', '')

print(1)
stemmer = SnowballStemmer("finnish")
wholeText = wholeText.split(' ')
for i in range(len(wholeText)):
    wholeText[i] = stemmer.stem(wholeText[i])

print(2)
d = {}
for word in filter(lambda x: x != '', wholeText):
    d[word] = d.get(word, 0) + 1

# open('ready.txt', 'w').write(' '.join(filter(lambda x: x != '', wholeText)))
# open('ready.txt', 'w').write(wholeText)

open('ready.txt', 'w', encoding='utf-8').write(str(dict(sorted(list(d.items()), key=lambda x: x[1], reverse=True))))
# print(type(obj))
# pprint.pprint(obj[200:203])
