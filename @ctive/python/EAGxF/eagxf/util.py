"""
Programming utilities.

"""


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
