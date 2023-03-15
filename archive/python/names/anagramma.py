from functools import reduce
from itertools import permutations
from typing import Iterator


def get_anagrams(name: str) -> Iterator[str]:
    yield from sorted(set(map(lambda p: ''.join(p), permutations(list(name)))))


your_name = input("Your name: ")
for anagram in get_anagrams(your_name):
    print('>', anagram)
