import json


with open('definitions.json', 'r', encoding='utf-8') as f:
    json_obj = json.loads(f.read())


pages: list[dict] = json_obj['mediawiki']['page']

count = 0
for page in pages:
    text1 = page['revision']['text']
    text1 = text1.get('#text', '')
    if '31.5.2016' in text1:
        count += 1

print(count)