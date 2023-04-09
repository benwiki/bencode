from pprint import pprint

titles = open('liquicity_only_titles.txt', 'r').read().split('\n')
count_titles: dict[str, int] = {}
for title in titles:
    count_titles[title] = count_titles.get(title, 0) + 1
count_titles_vals = list(count_titles.items())
count_titles_vals.sort(key=lambda x: x[1], reverse=True)
with open('liquicity_only_titles_count.txt', 'w') as f:
    for title, count in count_titles_vals:
        if count == 1:
            break
        f.write(f'{title} {count}\n')
