import discord
from discord import ButtonStyle

from eagxf.status import Status
from eagxf.structure import Button, Structure

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
EMOJI_STATUS = {v: k for k, v in STATUS_EMOJI.items()}

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
NAME_NUM = {v: k for k, v in NUM_NAME.items()}

NUM_EMOJI = {
    1: "1️⃣",
    2: "2️⃣",
    3: "3️⃣",
    4: "4️⃣",
    5: "5️⃣",
    6: "6️⃣",
    7: "7️⃣",
    8: "8️⃣",
    9: "9️⃣",
    0: "0️⃣",
}
EMOJI_NUM = {v: k for k, v in NUM_EMOJI.items()}

DEFAULT_PRIO_ORDER = [
    "One matching language",
    "Number of matching words in questions",
    "Number of matching keywords",
    "Location distance",
    "Status",
    "Number of matching words in title",
]
PRIO_LIST_LENGTH = len(DEFAULT_PRIO_ORDER)


def ANSWERS(search=False):  # pylint: disable=invalid-name
    prefix = "search_" if search else ""
    return (
        "\n___Where do I need help / what do I want to learn?___"
        f"\n🫲  <{prefix}need_help>"
        "\n___Where can I help / what is my expertise?___"
        f"\n🫱  <{prefix}can_help>"
    )


def PROFILE(search=False):  # pylint: disable=invalid-name
    prefix = "search_" if search else ""
    return (
        (
            "***====== Current filters ======***"
            if search
            else "***====== Your profile ======***"
        )
        # "\n\n**Metadata**"
        # "\n- 🆔 *User ID:* <id>"
        # "\n- 📅 *Date Joined:* <date_joined>"
        + f"\n- ***Name:***  <{prefix}name>"
        f"\n- ***Title:***  <{prefix}title>"
        f"\n- ***Location:***  <{prefix}location>"
        f"\n- ***Languages:***  <{prefix}languages>"
        "\n***======❓Questions ======***"
        f"{ANSWERS(search)}"
        "\n***========================***"
        f"\n- **Keywords:**  <{prefix}keywords>"
        f"\n- **Status:**  <{prefix}status>"
        "\n***========================***"
        + ("\n\nNumber of results: **<number_of_results>**" if search else "")
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

STRUCTURES = {
    "home": Structure(
        message="ℹ️ Status: <status>"
        f"\n\nWelcome to {APP_NAME}, **<name>**!"
        "\nClick the buttons to use the app!",
        buttons=[
            Button(label="👤 Profile", takes_to="profile", style=ButtonStyle.primary),
            Button(label="🔍 Search", takes_to="search", style=ButtonStyle.primary),
            Button(
                label="✨ Best Matches",
                takes_to="best_matches",
                style=ButtonStyle.primary,
            ),
        ],
    ),
    "profile": Structure(
        message=PROFILE(),
        buttons=[
            Button(label="⬅️ Back", takes_to="home"),
            Button(label="✏️ Edit", takes_to="edit_profile", style=ButtonStyle.primary),
        ],
    ),
    "edit_profile": Structure(
        message=PROFILE() + "\n\n✏️ **Editing Profile**" "\nWhat do you want to change?",
        buttons=[
            Button(label="🔤 Name", takes_to="edit_name"),
            Button(label="🏷️ Title", takes_to="edit_title"),
            Button(label="📍 Location", takes_to="edit_location", row=1),
            Button(label="💬 Languages", takes_to="edit_languages", row=1),
            Button(
                label="Answers to ❓Questions",
                takes_to="edit_answers",
                row=2,
            ),
            Button(label="🔑 Keywords", takes_to="edit_keywords", row=3),
            Button(
                label="Status",
                takes_to="edit_status",
                emoji=discord.PartialEmoji(name="ℹ️"),
                row=3,
            ),
            Button(label="⬅️ Back", takes_to="profile", row=4),
            Button(label="🏠 Home", style=ButtonStyle.primary, takes_to="home", row=4),
        ],
    ),
    "edit_name": Structure(
        message="Your current name is:\n*<name>*"
        "\n\nWhat do you want to change your name to?",
        changes_property="name",
    ),
    "edit_title": Structure(
        message="Your current title is:\n*<title>*"
        "\n\nWhat do you want to change your title to?",
        changes_property="title",
    ),
    "edit_location": Structure(
        message="Your current location is:\n*<location>*"
        "\n\nWhat do you want to change your location to?",
        changes_property="location",
    ),
    "edit_languages": Structure(
        message="Your current languages are:\n*<languages>*"
        "\n\nWhat do you want to change your languages to?"
        "\n(Comma separated, e.g. English, German, Spanish)",
        changes_property="languages",
        comma_separated=True,
    ),
    "edit_answers": Structure(
        message="**Your current answers to questions are:**"
        f"\n{ANSWERS()}"
        "\n\nWhat do you want to change?",
        buttons=[
            Button(label="🫲 Need Help", takes_to="edit_need_help"),
            Button(label="🫱 Can Help", takes_to="edit_can_help"),
            Button(label="⬅️ Back", takes_to="edit_profile", row=1),
            Button(label="🏠 Home", style=ButtonStyle.primary, takes_to="home", row=1),
        ],
    ),
    "edit_keywords": Structure(
        message="Your current keywords are:\n*<keywords>*"
        "\n\nWhat do you want to change your keywords to?"
        "\n(Comma separated, e.g. psychology, Python, electric guitar)",
        changes_property="keywords",
        comma_separated=True,
    ),
    "edit_status": Structure(
        message="Your current status is:\n*<status>*"
        "\nWhat do you want to change your status to?"
        "\n(Select the corresponding reaction!)\n"
        + "\n".join(
            f"{emoji} ({status.value})" for status, emoji in STATUS_EMOJI.items()
        ),
        reactions=list(STATUS_EMOJI.values()),
        changes_property="status",
        condition="profile_complete",
    ),
    "edit_need_help": Structure(
        message="Your current answer to **'Where do I need help /"
        " what do I want to learn?'** is:\n*<need_help>*"
        "\n\nWhat do you want to change it to?",
        changes_property="need_help",
    ),
    "edit_can_help": Structure(
        message="Your current answer to **'Where can I help /"
        " what is my expertise?'** is:\n*<can_help>*"
        "\n\nWhat do you want to change it to?",
        changes_property="can_help",
    ),
    "search": Structure(
        message="🔍 **Search**\n\n"
        f"{PROFILE(search=True)}"
        "\n\nClick the buttons to change the filters!",
        buttons=[
            Button(label="🔤 Name", takes_to="search_name"),
            Button(label="🏷️ Title", takes_to="search_title"),
            Button(label="📍 Location", takes_to="search_location", row=1),
            Button(label="💬 Languages", takes_to="search_languages", row=1),
            Button(label="🫲 Need Help", takes_to="search_need_help", row=2),
            Button(label="🫱 Can Help", takes_to="search_can_help", row=2),
            Button(label="🔑 Keywords", takes_to="search_keywords", row=3),
            Button(
                label="Status",
                takes_to="search_status",
                emoji=discord.PartialEmoji(name="ℹ️"),
                row=3,
            ),
            Button(label="⬅️ Back", takes_to="home", row=4),
            Button(
                label="SHOW RESULTS",
                style=ButtonStyle.green,
                takes_to="show_results",
                row=4,
            ),
        ],
    ),
    "search_name": Structure(
        message="What name do you want to search for?"
        "\n\nCurrent filter:\n*<search_name>*"
        "\n\nType ? to search for any name.",
        changes_property="search_name",
    ),
    "search_title": Structure(
        message="What title do you want to search for?"
        "\n\nCurrent filter:\n*<search_title>*"
        "\n\nType ? to search for any title.",
        changes_property="search_title",
    ),
    "search_location": Structure(
        message="What location do you want to search for?"
        "\n\nCurrent filter:\n*<search_location>*"
        "\n\nType ? to search for any location.",
        changes_property="search_location",
    ),
    "search_languages": Structure(
        message="What languages do you want to search for?"
        f"{COMMA_AND_SEPARATED_LANGUAGES}"
        "\n\nCurrent filter:\n*<search_languages>*"
        "\n\nType ? to search for any language.",
        changes_property="search_languages",
        comma_separated=True,
    ),
    "search_keywords": Structure(
        message="What keywords do you want to search for?"
        f"{COMMA_AND_SEPARATED}"
        "\n\nCurrent filter:\n*<search_keywords>*"
        "\n\nType ? to search for any keyword.",
        changes_property="search_keywords",
        comma_separated=True,
    ),
    "search_status": Structure(
        message="What status do you want to search for?"
        "\n(Select the corresponding reaction!)\n"
        + "\n".join(
            [f"{emoji} ({status.value})" for status, emoji in STATUS_EMOJI.items()]
            + ["❓ (Any)"]
        ),
        reactions=list(STATUS_EMOJI.values()) + ["❓"],
        changes_property="search_status",
    ),
    "search_need_help": Structure(
        message="What keywords do you want to search for in the answers to the question:"
        "\n**'Where do I need help / what do I want to learn?'**"
        f"{COMMA_AND_SEPARATED}"
        "\n\nCurrent filter:\n*<search_need_help>*"
        "\n\nType ? to search for any keyword.",
        changes_property="search_need_help",
        comma_separated=True,
    ),
    "search_can_help": Structure(
        message="What keywords do you want to search for in the answers to the question:"
        "\n**'Where can I help / what is my expertise?'**"
        f"{COMMA_AND_SEPARATED}"
        "\n\nCurrent filter:\n*<search_can_help>*"
        "\n\nType ? to search for any keyword.",
        changes_property="search_can_help",
        comma_separated=True,
    ),
    "show_results": Structure(
        message="🔍 **Search Results**\n\n"
        f"{PROFILE(search=True)}"
        "\n\n**Results:**\n\n<search_results>",
        buttons=[
            Button(
                label="🔍 Search again",
                style=ButtonStyle.green,
                takes_to="show_results",
            ),
            Button(label="⬅️ Back", takes_to="search", row=1),
            Button(label="🏠 Home", style=ButtonStyle.primary, takes_to="home", row=1),
        ],
    ),
    "best_matches": Structure(
        message="✨ **Best matches**\n\n"
        "Here we have sorted all current users according to how well they match your interests"
        " and expertise. Feel free to browse and correct us if you find that our algorithm"
        " doesn't bring you the most suitable people!"
        "\n\n**Results (<matches_from> - <matches_to>) from total <total_matches>**\n\n<best_matches>"
        "\n\n(<matches_from> - <matches_to>) from total <total_matches>",
        buttons=[
            Button(
                label="◀️ Previous",
                takes_to="best_matches",
                condition="has_previous",
                effect="best_matches_prev_page",
            ),
            Button(
                label="Next ▶️",
                takes_to="best_matches",
                condition="has_next",
                effect="best_matches_next_page",
            ),
            Button(label="⬅️ Back", takes_to="home", row=1),
            Button(
                label="✏️ Change priority",
                takes_to="change_priority",
                style=ButtonStyle.primary,
                effect="change_priority",
                row=1,
            ),
        ],
    ),
    "change_priority": Structure(
        message=(
            PRIORITY_MESSAGE := "✨✏️ Best matches **priority change**\n\n"
            "Here you can change the priority order of your best matches."
            "\n***Click a number-reaction "
            f"({NUM_EMOJI[1]} - {NUM_EMOJI[PRIO_LIST_LENGTH]}) "
            "to add the corresponding element to your new order!***"
            f"\nIf you select {PRIO_LIST_LENGTH - 1} or less elements, "
            "the omitted ones won't be considered in the matching process."
            "\n\n__Your current order:__"
            "\n<best_match_prio_order>"
            "\n\n__The default order to select from:__"
            f"\n{NUM_EMOJI[1]}**.** "
            + "\n{}**.** ".join(DEFAULT_PRIO_ORDER).format(
                *(list(NUM_EMOJI.values())[1 : PRIO_LIST_LENGTH + 1])
            )
            + "\n\n__Your new order:__"
            "\n<best_match_prio_order_new>\n" + r"\_" * 50
        ),
        buttons=[
            Button(
                label="*️⃣ Default",
                takes_to="default_best_matches_confirm",
                effect="reload_message",
            ),
            Button(
                label="🔄 Reset",
                takes_to="change_priority",
                effect="reload_message",
                style=ButtonStyle.danger,
            ),
            Button(
                label="⬅️ Back",
                takes_to="best_matches",
                effect="cancel_change_prio",
                row=1,
            ),
            Button(
                label="🏠 Home",
                takes_to="home",
                style=ButtonStyle.primary,
                effect="cancel_change_prio",
                row=1,
            ),
        ],
        changes_property="best_match_prio_order",
        reactions=list(NUM_EMOJI.values())[:PRIO_LIST_LENGTH],
    ),
    "default_best_matches_confirm": Structure(
        message="The default priority order is:"
        "\n1. "
        + "\n{}. ".join(DEFAULT_PRIO_ORDER).format(*range(2, PRIO_LIST_LENGTH + 1))
        + "\n\nAre you sure you want to reset your priority order to this?\n"
        + r"\_" * 50,
        buttons=[
            Button(
                label="No",
                takes_to="change_priority",
                effect="cancel_change_prio",
                style=ButtonStyle.red,
            ),
            Button(
                label="Yes",
                takes_to="best_matches",
                effect="default_best_matches",
                style=ButtonStyle.green,
            ),
        ],
    ),
}
