"""
Programming utilities.
"""

import discord
from eagxf.typedefs import DcClient

GUILD_ID = 1199560998328205452


def comma_and_search(a: str, b: str) -> bool:
    """Returns True if the ',' - '&' search succeeds.
    You can find more about this in [COMMA_AND_SEPARATED]
    from constants.py"""
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


def get_guild(client: DcClient) -> discord.Guild:
    guild = client.get_guild(GUILD_ID)
    assert guild, "(Error 15) Guild not found!"
    return guild


CHANNELS = []


def peek(text: str):
    if len(text) > 100:
        return f"{text[:101]}..."
    return text
