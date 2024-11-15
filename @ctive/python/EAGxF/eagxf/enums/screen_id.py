from enum import Enum, auto


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
    CHANGE_BEST_MATCHES_PRIORITY = auto()
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
    INVALID_DATE = auto()
    TOO_LONG_PROP_TEXT = auto()
    SUCCESSFUL_PROP_CHANGE = auto()
    CANCEL_MEETING_CONFIRM = auto()
    DELETE_MEETING_CONFIRM = auto()
    FUTURE_MEETINGS = auto()
    PAST_MEETINGS = auto()
    SEE_ABOUT_ME = auto()
    SEE_CAN_HELP = auto()
    SEE_NEED_HELP = auto()
    SEE_CONCERNS = auto()
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
    ALREADY_IN_PLATFORM = auto()
    DELETING_OLD_MESSAGES = auto()
    RECOMMEND_USER = auto()
    RECOMMENDATIONS = auto()
    RECOMMENDATIONS_SENT = auto()
    RECOMMENDATIONS_RECEIVED = auto()
    SUCCESSFUL_RECOMMENDATION = auto()
    RECOMMENDATION = auto()
    CANCEL_RECOMMENDATION_CONFIRM = auto()
    # ==== Notifications ====
    NOTI_INTEREST_RECEIVED = auto()
    NOTI_INTEREST_CONFIRMED = auto()
    NOTI_MEETING_REQUEST_RECEIVED = auto()
    NOTI_MEETING_REQUEST_CONFIRMED = auto()
    NOTI_CALL_STARTED = auto()
    # ==== special IDs ====
    BACK__ = auto()
    BACK_UNTIL_STOP__ = auto()

    @staticmethod
    def edit(thing: str) -> "ScreenId":
        return EDIT_SCREEN[thing]

    @staticmethod
    def search(thing: str) -> "ScreenId":
        return SEARCH_SCREEN[thing]

    @staticmethod
    def see(thing: str) -> "ScreenId":
        return SEE_SCREEN[thing]

    @staticmethod
    def confirm(erase_type: str) -> "ScreenId":
        return CONFIRM_CANCEL_OR_DELETE[erase_type]

    @staticmethod
    def meetings(meeting_time: str) -> "ScreenId":
        return MEETINGS_TIME[meeting_time]

    @staticmethod
    def action(action: str, thing: str) -> "ScreenId":
        match action:
            case "edit":
                return ScreenId.edit(thing)
            case "search":
                return ScreenId.search(thing)
            case "see":
                return ScreenId.see(thing)
            case _:
                raise RuntimeError("`action` invalid!")


SEARCH_SCREEN = {
    "about_me": ScreenId.SEARCH_ABOUT_ME,
    "can_help": ScreenId.SEARCH_CAN_HELP,
    "need_help": ScreenId.SEARCH_NEED_HELP,
    "concerns": ScreenId.SEARCH_CONCERNS,
    "name": ScreenId.SEARCH_NAME,
    "job": ScreenId.SEARCH_JOB,
    "company": ScreenId.SEARCH_COMPANY,
    "location": ScreenId.SEARCH_LOCATION,
    "languages": ScreenId.SEARCH_LANGUAGES,
    "keywords": ScreenId.SEARCH_KEYWORDS,
}

EDIT_SCREEN = {
    "about_me": ScreenId.EDIT_ABOUT_ME,
    "can_help": ScreenId.EDIT_CAN_HELP,
    "need_help": ScreenId.EDIT_NEED_HELP,
    "concerns": ScreenId.EDIT_CONCERNS,
    "name": ScreenId.EDIT_NAME,
    "job": ScreenId.EDIT_JOB,
    "company": ScreenId.EDIT_COMPANY,
    "location": ScreenId.EDIT_LOCATION,
    "languages": ScreenId.EDIT_LANGUAGES,
    "keywords": ScreenId.EDIT_KEYWORDS,
}

SEE_SCREEN = {
    "about_me": ScreenId.SEE_ABOUT_ME,
    "can_help": ScreenId.SEE_CAN_HELP,
    "need_help": ScreenId.SEE_NEED_HELP,
    "concerns": ScreenId.SEE_CONCERNS,
}

MEETINGS_TIME = {
    "past": ScreenId.PAST_MEETINGS,
    "future": ScreenId.FUTURE_MEETINGS,
}

CONFIRM_CANCEL_OR_DELETE = {
    "cancel": ScreenId.CANCEL_MEETING_CONFIRM,
    "delete": ScreenId.DELETE_MEETING_CONFIRM,
}
