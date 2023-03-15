def conv(unidstr):
    unidstr=unidstr.upper()
    if unidstr == 'A':
        return '.-'
    elif unidstr == 'B':
        return '-...'
    elif unidstr == 'C':
        return '-.-.'
    elif unidstr == 'D':
        return '-..'
    elif unidstr == 'E':
        return '.'
    elif unidstr == 'F':
        return '..-.'
    elif unidstr == 'G':
        return '--.'
    elif unidstr == 'H':
        return '....'
    elif unidstr in 'IÍ':
        return '..'
    elif unidstr == 'J':
        return '.---'
    elif unidstr == 'K':
        return '-.-'
    elif unidstr == 'L':
        return '.-..'
    elif unidstr == 'M':
        return '--'
    elif unidstr == 'N':
        return '-.'
    elif unidstr in 'OÓ':
        return '---'
    elif unidstr == 'P':
        return '.--.'
    elif unidstr == 'Q':
        return '--.-'
    elif unidstr == 'R':
        return '.-.'
    elif unidstr == 'S':
        return '...'
    elif unidstr == 'T':
        return '-'
    elif unidstr in 'UÚ':
        return '..-'
    elif unidstr == 'V':
        return '...-'
    elif unidstr == 'W':
        return '.--'
    elif unidstr == 'X':
        return '-..-'
    elif unidstr == 'Y':
        return '-.--'
    elif unidstr == 'Z':
        return '--..'
    elif unidstr == 'Á':
        return '.--.-'
    elif unidstr == 'É':
        return '..-..'
    elif unidstr in 'ÖŐ':
        return '---.'
    elif unidstr in 'ÜŰ':
        return '..--'
    elif unidstr == 'Ä':
        return '.-.-'
    elif unidstr == '.': return '.-.-.-'
    elif unidstr == ',': return '--..--'
    elif unidstr == ':': return '---...'
    elif unidstr == '?': return '..--..'
    elif unidstr == '!': return '--..--'
    elif unidstr == '-': return '-....-'
    elif unidstr == '"': return '.----.'
    elif unidstr == '(': return '-.--.-'
    elif unidstr == '/': return '-..-.'
    elif unidstr == '*': return '-..-'
    elif unidstr.isnumeric():
        n=int(unidstr)
        if 0<n<=5:
            return '.'*n+'-'*(5-n)
        elif n>5:
            n-=5
            return '-'*n+'.'*(5-n)
        else: return '-'*5
    else:
        return '#'

from math import ceil
from time import time

stop=time()

f=open("morsepalindoms.txt", 'w')
for word in open("word_database.txt","r"):
    morse = ''.join(conv(L) for L in word.strip())
    mlen=len(morse)
    first=morse[:mlen//2]
    second=morse[-1:ceil(mlen/2)-1:-1]
    
    if first==second:
        f.write(morse+" "+word)

f.close()

print(time()-stop)
