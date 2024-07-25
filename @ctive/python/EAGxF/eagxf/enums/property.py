from enum import Enum, auto


class Property(Enum):
    SELECTED_USER = auto()
    BEST_MATCH_PRIO_ORDER = auto()
    NAME = auto()
    JOB = auto()
    COMPANY = auto()
    LOCATION = auto()
    LANGUAGES = auto()
    KEYWORDS = auto()
    STATUS = auto()
    ABOUT_ME = auto()
    CAN_HELP = auto()
    NEED_HELP = auto()
    CONCERNS = auto()
    SEARCH_STATUS = auto()
    SEARCH_ABOUT_ME = auto()
    SEARCH_CAN_HELP = auto()
    SEARCH_NEED_HELP = auto()
    SEARCH_CONCERNS = auto()
    MEETING_REQUEST = auto()
    MEETING = auto()
    MEETING_DATE = auto()

    @staticmethod
    def search(thing: "Property") -> "Property":
        matchdict = {
            Property.ABOUT_ME: Property.SEARCH_ABOUT_ME,
            Property.CAN_HELP: Property.SEARCH_CAN_HELP,
            Property.NEED_HELP: Property.SEARCH_NEED_HELP,
            Property.CONCERNS: Property.SEARCH_CONCERNS,
        }
        return matchdict.get(thing, thing)

    @property
    def low(self) -> str:
        return self.name.lower()

    def __str__(self) -> str:
        return self.name.lower()

    def __repr__(self) -> str:
        return self.name.lower()

    def is_search(self) -> bool:
        return self.name.startswith("SEARCH_")

    def from_search(self) -> "Property":
        if not self.is_search():
            raise ValueError(f"Property {self} is not a search property")
        return Property[self.name[7:]]
