from enum import Enum


class Status(Enum):
    AVAILABLE = "Available"
    BUSY = "Busy"
    OFFLINE = "Offline"
    INVISIBLE = "Invisible"
    DO_NOT_DISTURB = "Do Not Disturb"
    ANY = "Any"

    def __lt__(self, other: "Status") -> bool:
        return ORDER.index(self) < ORDER.index(other)

    def __gt__(self, other: "Status") -> bool:
        return ORDER.index(self) > ORDER.index(other)

    def __le__(self, other: "Status") -> bool:
        return ORDER.index(self) <= ORDER.index(other)

    def __ge__(self, other: "Status") -> bool:
        return ORDER.index(self) >= ORDER.index(other)

    def __str__(self) -> str:
        from eagxf.constants import STATUS_EMOJI
        return f"{STATUS_EMOJI[self]} ({self.value})"


ORDER = [
    Status.ANY,
    Status.INVISIBLE,
    Status.DO_NOT_DISTURB,
    Status.OFFLINE,
    Status.BUSY,
    Status.AVAILABLE,
]
