from enum import Enum, auto


class Effect(Enum):
    GO_TO_PREVIOUS_PAGE = auto()
    GO_TO_NEXT_PAGE = auto()
    DELETE_MESSAGE = auto()
    SAVE_BEST_MATCHES = auto()
    RESET_NEW_PRIO_ORDER = auto()
    DEFAULT_BEST_MATCHES = auto()
    RESET_USER_PROPERTY_CHANGE = auto()
    EMPTY_RESULTS = auto()
    SEND_INTEREST = auto()
    CANCEL_INTEREST = auto()
    CANCEL_MEETING = auto()
    START_CALL = auto()
    CANCEL_CALL = auto()
    CANCEL_RECOMMENDATION = auto()
    REMOVE_NOTIFICATION = auto()
    SELECT_NOTIFICATION_SENDER = auto()
    RESET = auto()
