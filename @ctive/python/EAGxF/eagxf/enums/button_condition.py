from enum import Enum, auto


class ButtonCond(Enum):
    HAS_PREVIOUS_PAGE = auto()
    HAS_NEXT_PAGE = auto()
    HAS_MEETINGS = auto()
    PRIO_ORDER_FULL = auto()
    CAN_SEND_INTEREST = auto()
    CAN_CANCEL_INTEREST = auto()
    CAN_CONFIRM_INTEREST = auto()
    CAN_REQUEST_MEETING = auto()
    CAN_CANCEL_MEETING = auto()
    CAN_START_CALL = auto()
    CAN_CANCEL_CALL = auto()
    CAN_DELETE_MEETING = auto()
    CAN_CHANGE_MEETING_DATE = auto()
    CAN_SAVE = auto()

    def is_ability(self) -> bool:
        return self.name.startswith("CAN_")
