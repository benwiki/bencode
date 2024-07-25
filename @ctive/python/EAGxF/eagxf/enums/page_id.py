from enum import Enum, auto

from eagxf.constants import (
    CONFIRM_CANCEL_OR_DELETE,
    EDIT_SCREEN,
    MEETINGS_TIME,
    SEARCH_SCREEN,
)


class ScreenId(Enum):
    HOME = auto()
    PROFILE = auto()
    EDIT_PROFILE = auto()
    EDIT_ANSWERS = auto()
    EDIT_STATUS = auto()
    SEARCH = auto()
    EDIT_SEARCH_ANSWERS = auto()
    SEARCH_STATUS = auto()
    SHOW_SEARCH_RESULTS = auto()
    BEST_MATCHES = auto()
    CHANGE_PRIORITY = auto()
    DEFAULT_BEST_MATCHES_CONFIRM = auto()
    INTERESTS = auto()
    INTERESTS_SENT = auto()
    INTERESTS_RECEIVED = auto()
    MUTUAL_INTERESTS = auto()
    SELECTED_USER = auto()
    MEETING_REQUEST = auto()
    MEETINGS = auto()
    EDIT_MEETING = auto()
    CHANGE_MEETING_DATE = auto()
    CANCEL_MEETING_CONFIRM = auto()
    DELETE_MEETING_CONFIRM = auto()
    FUTURE_MEETINGS = auto()
    PAST_MEETINGS = auto()
    EDIT_ABOUT_ME = auto()
    EDIT_CAN_HELP = auto()
    EDIT_NEED_HELP = auto()
    EDIT_CONCERNS = auto()
    EDIT_NAME = auto()
    EDIT_JOB = auto()
    EDIT_COMPANY = auto()
    EDIT_LOCATION = auto()
    EDIT_LANGUAGES = auto()
    EDIT_KEYWORDS = auto()
    SEARCH_ABOUT_ME = auto()
    SEARCH_CAN_HELP = auto()
    SEARCH_NEED_HELP = auto()
    SEARCH_CONCERNS = auto()
    SEARCH_NAME = auto()
    SEARCH_JOB = auto()
    SEARCH_COMPANY = auto()
    SEARCH_LOCATION = auto()
    SEARCH_LANGUAGES = auto()
    SEARCH_KEYWORDS = auto()
    # ==== special IDs ====
    BACK__ = auto()

    @staticmethod
    def search(thing: str) -> "ScreenId":
        return SEARCH_SCREEN[thing]

    @staticmethod
    def edit(thing: str) -> "ScreenId":
        return EDIT_SCREEN[thing]

    @staticmethod
    def confirm(erase_type: str) -> "ScreenId":
        return CONFIRM_CANCEL_OR_DELETE[erase_type]

    @staticmethod
    def meetings(meeting_time: str) -> "ScreenId":
        return MEETINGS_TIME[meeting_time]

    @staticmethod
    def search_or_edit(action: str, thing: str) -> "ScreenId":
        match action:
            case "edit":
                return ScreenId.edit(thing)
            case "search":
                return ScreenId.search(thing)
            case _:
                raise RuntimeError("`action` invalid!")
