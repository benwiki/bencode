"""
To use this code, first unpack definitions.7z with 7-zip...
( https://7-zip.org/ )
... to the same folder, where this script is, then run the program.
"""

import json
import re
import pprint
from simplemma.simplemma import lemmatize


with open('definitions.json', 'r', encoding='utf-8') as f:
    json_obj = json.loads(f.read())

pages: list[dict] = json_obj['mediawiki']['page']

print("Reading 'definitions.json' file done.")

collection = {}

for i, page in enumerate(pages):
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

print("Sorting out and lemmatizing words done.")

collection_sorted = sorted(
    list(collection.items()),
    key=lambda x: x[1],
    reverse=True
)
collection_text = '\n'.join(
    f'{word} ({count})' for word, count in collection_sorted
)

with open('words.txt', 'w', encoding='utf-8') as f:
    f.write(collection_text)

print("Saving result ('words.txt') done.")