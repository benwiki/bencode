
import re
from eagxf.constant_functions import INIT_USERS_PATH
from eagxf.status import Status
from eagxf.util import invert_dict

APP_NAME = "EAGxF"

# ========== PATHS =====================================
TOKEN_PATH = "/Users/benke/Downloads/eagxf.txt"
USERS_FOLDER_PATH = "/Users/benke/Dev"
USERS_PATH = INIT_USERS_PATH()
# ======================================================

ADMINS = (
    348976146689294336,
    329635441433116674,
    704237105013850152,
)

SPACER = (
    f"Welcome to {APP_NAME}!\n\nScroll down "
    + ":arrow_down: " * 3
    + "if you see this!"
    + "\n" * 50
)

PAGE_STEP = 10

STATUS_EMOJI: dict[Status, str] = {
    Status.AVAILABLE: "🟢",
    Status.BUSY: "🟡",
    Status.OFFLINE: "⚪",
    Status.DO_NOT_DISTURB: "🔴",
    Status.INVISIBLE: "🟣",
}
EMOJI_STATUS = invert_dict(STATUS_EMOJI)

NUM_NAME = {
    1: "one",
    2: "two",
    3: "three",
    4: "four",
    5: "five",
    6: "six",
    7: "seven",
    8: "eight",
    9: "nine",
    0: "zero",
}
NAME_NUM = invert_dict(NUM_NAME)

NUM_EMOJI = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "0️⃣"]

DEFAULT_PRIO_ORDER = [
    "One matching language",
    "Number of matching words in questions",
    "Number of matching keywords",
    "Location distance",
    "Status",
    "Number of matching words in the headline",
]
PRIO_LIST_LENGTH = len(DEFAULT_PRIO_ORDER)

SPECIAL_DESTINATIONS = ("<back>",)

NOT_ALNUM = re.compile(r"[\W_]+", re.UNICODE)
DATE_FORMAT = re.compile(r"\d{2}\.\d{2}\.\d{4}(?: \d{2}:\d{2}(?::\d{2})?)?")

INCOMPLETE_PROFILE_MSG = (
    "*Your profile must be complete before you can "
    "change your status ;-)*"
    "\n*Fill out all details and try again!*"
)
INCOMPLETE_PROFILE_WARNING = (
    "\n\n*(Your profile is incomplete, so your status has been "
    "changed to invisible!)*"
)

QUESTION_NAMES = {
    "about_me": {
        "label": "About me",
        "text": "About me: (general info)",
        "emoji": "🙋",
    },
    "can_help": {
        "label": "Can help",
        "text": "How I can help others:",
        "emoji": "🫱",
    },
    "need_help": {
        "label": "Need help",
        "text": "How others can help me:",
        "emoji": "🫲",
    },
    "concerns": {
        "label": "Concerns",
        "text": "What am I concerned about:",
        "emoji": "🤔",
    },
}

VISIBLE_SIMPLE_USER_PROPS: dict[str, dict] = {
    "name": {
        "row": 0,
        "emoji": "🔤",
        "label": "Name",
        "before_questions": True,
        "comma_separated": False,
    },
    "headline": {
        "row": 0,
        "emoji": "🏷️",
        "label": "Headline",
        "before_questions": True,
        "comma_separated": False,
    },
    "location": {
        "row": 1,
        "emoji": "📍",
        "label": "Location",
        "before_questions": True,
        "comma_separated": False,
    },
    "languages": {
        "row": 1,
        "emoji": "💬",
        "label": "Languages",
        "before_questions": True,
        "comma_separated": True,
        "example": "English, German, Spanish",
    },
    "keywords": {
        "row": 3,
        "emoji": "🔑",
        "label": "Keywords",
        "before_questions": False,
        "comma_separated": True,
        "example": "psychology, Python, electric guitar",
    },
}

COMMA_AND_SEPARATED = (
    "\n\n( Comma and '&' separated, e.g.:"
    "\n- (A) psychology, Python, electric guitar --> will accept if "
    "AT LEAST ONE of the keywords is present in the profile"
    "\n- (B) psychology & Python & electric guitar --> will accept if "
    "EVERY keyword is present in the profile"
    "\n- (C) psychology & Python, electric guitar --> will accept if both "
    "'psychology' AND 'Python', or if 'electric guitar' "
    "is present in the profile"
    "\n\nExample:"
    "\n**Profile 1:**  psychology, gardening"
    "\n**Profile 2:**  cooking, reparing bikes, electric guitar"
    "\n**Profile 3:**  psychology, Python, electric guitar"
    "\n\n- (A) will accept all 3 profiles"
    "\n- (B) will only accept Profile 3"
    "\n- (C) will accept Profile 2 and Profile 3 )"
)
COMMA_AND_SEPARATED_LANGUAGES = (
    "\n\n( Comma and '&' separated, e.g.:"
    "\n- (A) English, German, Spanish --> will accept if "
    "AT LEAST ONE of the languages is present in the profile"
    "\n- (B) English & German & Spanish --> will accept if "
    "EVERY language is present in the profile"
    "\n- (C) English & German, Spanish --> will accept if both "
    "'English' AND 'German', or if 'Spanish' "
    "is present in the profile"
    "\n\nExample:"
    "\n**Profile 1:**  English, French"
    "\n**Profile 2:**  English, German, Spanish"
    "\n**Profile 3:**  English, German, Spanish, French"
    "\n\n- (A) will accept all 3 profiles"
    "\n- (B) will only accept Profile 3"
    "\n- (C) will accept Profile 2 and Profile 3 )"
)

COMMA_SEPARATED_MAP = {
    "keywords": COMMA_AND_SEPARATED,
    "languages": COMMA_AND_SEPARATED_LANGUAGES,
}
