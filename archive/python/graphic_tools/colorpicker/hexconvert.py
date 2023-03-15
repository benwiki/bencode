from typing import Iterable


def remove_prefix(prefixed: str) -> str:
    return prefixed[2:]


def to_hex_component(component: int) -> str:
    return remove_prefix(str(hex(component))).rjust(2, '0')


def to_hex(rgb: Iterable[int]) -> str:
    components = (to_hex_component(component) for component in rgb)
    return '#' + ''.join(components)