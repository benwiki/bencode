
# ========== Importing libs ===========
from functools import reduce

# ========== Defining functions ===========
floatrange = lambda a, b, c, d: [x/d for x in range(int(a*d), int(b*d), int(c*d))]

to_time = lambda x: f'{int(x)}:00' if int(x)==x else f'{int(x)}:30'

gen_times = lambda start, end: [
    to_time(x)+'-'+to_time(x+0.5)
    for x in floatrange(start, end, 0.5, 10)
]

# ========== Getting data ===========
original = """=REGEXREPLACE(REGEXREPLACE(textjoin(" ♦ "; 0; QUERY($B$2:$G; "select B where (D matches '.*<activity>.*' and <daycol> matches '.*<time>.*') label B ''";0) );" ♦ \$";" = \$");" ♦ ";CHAR(10))"""

activities = ['Programming', 'Singing', 'Dancing', 'Maths', 'Philosophy', 'Language']
daycols = ('E'*7,'F'*4, 'G'*10)
daytimes = ((16.5, 20), (17, 19), (15, 20))

add = lambda a, b: a + b

time_data = reduce(add, map(list, [
    zip(daycol, gen_times(start, end))
    for daycol, (start, end) in zip(daycols, daytimes)
]))

# ========== Test ===========
# print(gen_times(16.5, 20))
# print(time_data)

result = '\n'.join(
    '\t'.join(
        original.replace('<activity>', activity)
                .replace('<daycol>', daycol)
                .replace('<time>', time)
        for activity in activities )
    for daycol, time in time_data )

# ========== Storing data ===========
# open("result.txt", 'w', encoding='utf-8').write(result)