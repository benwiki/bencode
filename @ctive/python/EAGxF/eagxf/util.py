"""
Programming utilities.
"""

from typing import Callable


def comma_and_search(a: str, b: str) -> bool:
    """Returns True if... for God's sake, just read the code!"""
    return (
        any(
            all(kw.strip().lower() in a.lower() for kw in block.split("&"))
            for block in b.split(", ")
        )
        or b == "?"
    )


def invert_dict(d: dict) -> dict:
    """Inverts a dictionary."""
    return {v: k for k, v in d.items()}


def subtract(a: list, b: list) -> list:
    """Subtracts list b from list a."""
    return [x for x in a if x not in b]


def intersect(a: list, b: list) -> list:
    """Returns the intersection of two lists."""
    return [x for x in a if x in b]


def to_emojis(number: int) -> str:
    """Converts a number to emojis. E.g. 123 -> ":one::two::three:"""
    from eagxf.constants import NUM_NAME

    return "".join(f":{NUM_NAME[int(n)]}:" for n in str(number))
