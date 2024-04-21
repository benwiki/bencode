from eagxf.status import Status
from eagxf.structure import Button
from eagxf.util import invert_dict

APP_NAME = "EAGxF"

# ========== PATHS =====================================
TOKEN_PATH = "C:/Users/b.hargitai/prog/tokens/eagxf.txt"
USERS_FOLDER_PATH = "C:/Users/b.hargitai/prog"
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
    "Number of matching words in title",
]
PRIO_LIST_LENGTH = len(DEFAULT_PRIO_ORDER)

QUESTION_NAMES = {
    "about_me": {
        "label": "About me",
        "text": "About me: (general info)",
        "emoji": "🙋",
    },
    "can_help": {"label": "Can help", "text": "How I can help others:", "emoji": "🫱"},
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
    "title": {
        "row": 0,
        "emoji": "🏷️",
        "label": "Title",
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


def ANSWERS(search=False) -> str:  # pylint: disable=invalid-name
    prefix = "search_" if search else ""
    return "\n" + "\n".join(
        f"__{question['text']}__" f"\n{question['emoji']}  <{prefix}{q_id}>"
        for q_id, question in QUESTION_NAMES.items()
    )


def PROFILE(search=False):  # pylint: disable=invalid-name
    prefix = "search_" if search else ""
    return (
        (
            "***------ Current filters ------***"
            if search
            else "***------ Your profile ------***"
        )
        # "\n\n**Metadata**"
        # "\n- 🆔 *User ID:* <id>"
        # "\n- 📅 *Date Joined:* <date_joined>"
        + SIMPLE_PROPS(prefix, before_questions=True)
        + "\n***------❓Questions ------***"
        f"{ANSWERS(search)}"
        "\n***------------------------***"
        + SIMPLE_PROPS(prefix, before_questions=False)
        + f"\n- ***Status:***  <{prefix}status>"
        + "\n***------------------------***"
        + ("\n\nNumber of results: **<number_of_results>**" if search else "")
    )


def SIMPLE_PROPS(prefix, before_questions=True):  # pylint: disable=invalid-name
    return "".join(
        f"\n- ***{prop['label']}:***  <{prefix}{prop_id}>"
        for prop_id, prop in VISIBLE_SIMPLE_USER_PROPS.items()
        if before_questions == prop["before_questions"]
    )


def SIMPLE_PROP_BUTTONS(action, before_questions=True):  # pylint: disable=invalid-name
    """Returns a list of buttons for [simple properties]"""
    return (
        Button(
            label=prop["label"],
            emoji=prop["emoji"],
            takes_to=f"{action}_{prop_id}",
            row=prop["row"],
        )
        for prop_id, prop in VISIBLE_SIMPLE_USER_PROPS.items()
        if before_questions == prop["before_questions"]
    )


def QUESTION_BUTTONS(action):  # pylint: disable=invalid-name
    return (
        Button(
            label=question["label"],
            emoji=question["emoji"],
            takes_to=f"{action}_{q_id}",
        )
        for q_id, question in QUESTION_NAMES.items()
    )


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
