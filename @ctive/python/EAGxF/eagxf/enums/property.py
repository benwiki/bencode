from enum import Enum, auto


class Property(Enum):
    # === Simple user properties ===
    SELECTED_USER = auto()
    BEST_MATCH_PRIO_ORDER = auto()
    NAME = auto()
    JOB = auto()
    COMPANY = auto()
    LOCATION = auto()
    LANGUAGES = auto()
    KEYWORDS = auto()
    STATUS = auto()
    # === Answers to questions ===
    ABOUT_ME = auto()
    CAN_HELP = auto()
    NEED_HELP = auto()
    CONCERNS = auto()
    SEARCH_STATUS = auto()
    SEARCH_ABOUT_ME = auto()
    SEARCH_CAN_HELP = auto()
    SEARCH_NEED_HELP = auto()
    SEARCH_CONCERNS = auto()
    # === Strange properties ===
    MEETING_REQUEST = auto()
    MEETING = auto()
    CHANGE_MEETING_DATE = auto()
    SEND_RECOMMENDATION = auto()
    RECOMMENDATION = auto()

    @staticmethod
    def search(thing: "Property") -> "Property":
        return {
            Property.ABOUT_ME: Property.SEARCH_ABOUT_ME,
            Property.CAN_HELP: Property.SEARCH_CAN_HELP,
            Property.NEED_HELP: Property.SEARCH_NEED_HELP,
            Property.CONCERNS: Property.SEARCH_CONCERNS,
        }.get(thing, thing)

    @property
    def to_str(self) -> str:
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

    def to_search(self) -> "Property":
        if self.is_search():
            raise ValueError(f"Property {self} is already a search property")
        return Property.search(self)
