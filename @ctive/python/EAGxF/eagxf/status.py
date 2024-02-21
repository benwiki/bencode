from enum import Enum


class Status(Enum):
    AVAILABLE = "Available"
    BUSY = "Busy"
    OFFLINE = "Offline"
    INVISIBLE = "Invisible"
    DO_NOT_DISTURB = "Do Not Disturb"
    ANY = "Any"