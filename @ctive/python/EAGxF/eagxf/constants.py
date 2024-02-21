import discord
from discord import ButtonStyle
from eagxf.status import Status
from eagxf.structure import Button, Structure

APP_NAME = "EAGxF"

SPACER = f"{APP_NAME}" + "\n" * 50

STATUS_EMOJI: dict[Status, str] = {
    Status.AVAILABLE: "🟢",
    Status.BUSY: "🟡",
    Status.OFFLINE: "⚪",
    Status.INVISIBLE: "🟣",
    Status.DO_NOT_DISTURB: "🔴",
}
EMOJI_STATUS = {v: k for k, v in STATUS_EMOJI.items()}

def ANSWERS(search=False):
    prefix = "search_" if search else ""
    return (
        "\n*Where do I need help / what do I want to learn?*"
        f"\n🫲 <{prefix}need_help>"
        "\n*Where can I help / what is my expertise?*"
        f"\n🫱 <{prefix}can_help>"
    )

def PROFILE(search=False):  # noqa  # type: ignore
    prefix = "search_" if search else ""
    return (
        ("***====== Your profile ======***"
         if not search else
         "***====== Current filters ======***")
        # "\n\n**Metadata**"
        # "\n- 🆔 *User ID:* <id>"
        # "\n- 📅 *Date Joined:* <date_joined>"
        + "\n**Personal**"
        f"\n🔤 *Name:* <{prefix}name>"
        f"\n🏷️ *Title:* <{prefix}title>"
        f"\n📍 *Location:* <{prefix}location>"
        f"\n💬 *Languages:* <{prefix}languages>"
        "\n***========================***"
        "\n❓**Questions**"
        f"{ANSWERS(search)}"
        "\n***========================***"
        f"\n**🔑 Keywords**: <{prefix}keywords>"
        f"\n**ℹ️ Status**: <{prefix}status>"
        "\n***========================***"
        + ("\n\nNumber of results: **<number_of_results>**"
         if search else "")
    )

COMMA_AND_SEPARATED = (
    "\n\n(Comma and '&' separated, e.g.:"
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
    "\n- (C) will accept Profile 2 and Profile 3"
)
COMMA_AND_SEPARATED_LANGUAGES = (
    "\n\n(Comma and '&' separated, e.g.:"
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
    "\n- (C) will accept Profile 2 and Profile 3"
)

STRUCTURES = {
    "home": Structure(
        message="ℹ️ Status: <status>"
        f"\n\nWelcome to {APP_NAME}, **<name>**!"
        "\nClick the buttons to use the app!",
        buttons=[
            Button(label="👤 Profile", takes_to="profile", style=ButtonStyle.primary),
            Button(label="🔍 Search", takes_to="search", style=ButtonStyle.primary),
        ],
    ),
    "profile": Structure(
        message=PROFILE(),
        buttons=[
            Button(label="⬅️ Back", style=ButtonStyle.red, takes_to="home"),
            Button(label="✏️ Edit", takes_to="edit_profile", style=ButtonStyle.primary),
        ],
    ),
    "edit_profile": Structure(
        message=PROFILE() + "\n\n✏️ **Editing Profile**" "\nWhat do you want to change?",
        buttons=[
            Button(label="⬅️ Back", style=ButtonStyle.red, takes_to="profile"),
            Button(label="🏠 Home", style=ButtonStyle.primary, takes_to="home"),
            Button(label="🔤 Name", takes_to="edit_name", row=1),
            Button(label="🏷️ Title", takes_to="edit_title", row=1),
            Button(label="📍 Location", takes_to="edit_location", row=2),
            Button(label="💬 Languages", takes_to="edit_languages", row=2),
            Button(
                label="Answers to ❓Questions",
                takes_to="edit_answers",
                row=3,
            ),
            Button(label="🔑 Keywords", takes_to="edit_keywords", row=4),
            Button(
                label="Status",
                takes_to="edit_status",
                emoji=discord.PartialEmoji(name="ℹ️"),
                row=4,
            ),
        ],
    ),
    "edit_name": Structure(
        message="Your current name is: <name>."
        "\nWhat do you want to change your name to?",
        changes_property="name",
    ),
    "edit_title": Structure(
        message="Your current title is: <title>."
        "\nWhat do you want to change your title to?",
        changes_property="title",
    ),
    "edit_location": Structure(
        message="Your current location is: <location>."
        "\nWhat do you want to change your location to?",
        changes_property="location",
    ),
    "edit_languages": Structure(
        message="Your current languages are: <languages>."
        "\nWhat do you want to change your languages to?"
        "\n(Comma separated, e.g. English, German, Spanish)",
        changes_property="languages",
        comma_separated=True,
    ),
    "edit_answers": Structure(
        message="**Your current answers to questions are:**"
        f"\n{ANSWERS()}"
        "\n\nWhat do you want to change?",
        buttons=[
            Button(label="⬅️ Back", style=ButtonStyle.red, takes_to="edit_profile"),
            Button(label="🫲 Need Help", takes_to="edit_need_help"),
            Button(label="🫱 Can Help", takes_to="edit_can_help"),
        ],
    ),
    "edit_keywords": Structure(
        message="Your current keywords are: <keywords>."
        "\nWhat do you want to change your keywords to?"
        "\n(Comma separated, e.g. psychology, Python, electric guitar)",
        changes_property="keywords",
        comma_separated=True,
    ),
    "edit_status": Structure(
        message="Your current status is: <status>."
        "\nWhat do you want to change your status to?"
        "\n(Select the corresponding reaction!)\n"
        + "\n".join(
            f"{emoji} ({status.value})" for status, emoji in STATUS_EMOJI.items()
        ),
        reactions=list(STATUS_EMOJI.values()),
        changes_property="status",
    ),
    "edit_need_help": Structure(
        message="Your current answer to 'Where do I need help /"
        " what do I want to learn?' is: <need_help>."
        "\nWhat do you want to change it to?",
        changes_property="need_help",
    ),
    "edit_can_help": Structure(
        message="Your current answer to 'Where can I help /"
        " what is my expertise?' is: <can_help>."
        "\nWhat do you want to change it to?",
        changes_property="can_help",
    ),
    "search": Structure(
        message="🔍 **Search**\n\n"
        f"{PROFILE(search=True)}"
        "\n\nClick the buttons to change the filters!",
        buttons=[
            Button(label="⬅️ Back", style=ButtonStyle.red, takes_to="home"),
            Button(label="SHOW RESULTS", style=ButtonStyle.green, takes_to="show_results"),
            Button(label="🔤 Name", takes_to="search_name", row=1),
            Button(label="🏷️ Title", takes_to="search_title", row=1),
            Button(label="📍 Location", takes_to="search_location", row=2),
            Button(label="💬 Languages", takes_to="search_languages", row=2),
            Button(label="🫲 Need Help", takes_to="search_need_help", row=3),
            Button(label="🫱 Can Help", takes_to="search_can_help", row=3),
            Button(label="🔑 Keywords", takes_to="search_keywords", row=4),
            Button(label="Status", takes_to="search_status", row=4, emoji=discord.PartialEmoji(name="ℹ️")),
        ],
    ),
    "search_name": Structure(
        message="What name do you want to search for?"
        "\nType ? to search for any name.",
        changes_property="search_name",
    ),
    "search_title": Structure(
        message="What title do you want to search for?"
        "\nType ? to search for any title.",
        changes_property="search_title",
    ),
    "search_location": Structure(
        message="What location do you want to search for?"
        "\nType ? to search for any location.",
        changes_property="search_location",
    ),
    "search_languages": Structure(
        message="What languages do you want to search for?"
        f"{COMMA_AND_SEPARATED_LANGUAGES}"
        "\n\nType ? to search for any language.",
        changes_property="search_languages",
        comma_separated=True,
    ),
    "search_keywords": Structure(
        message="What keywords do you want to search for?"
        f"{COMMA_AND_SEPARATED}"
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
        "\n\nType ? to search for any keyword.",
        changes_property="search_need_help",
        comma_separated=True,
    ),
    "search_can_help": Structure(
        message="What keywords do you want to search for in the answers to the question:"
        "\n**'Where can I help / what is my expertise?'**"
        f"{COMMA_AND_SEPARATED}"
        "\n\nType ? to search for any keyword.",
        changes_property="search_can_help",
        comma_separated=True,
    ),
    "show_results": Structure(
        message="🔍 **Search Results**\n\n"
        f"{PROFILE(search=True)}"
        "\n\n**Results:**\n\n<search_results>",
        buttons=[
            Button(label="⬅️ Back", style=ButtonStyle.red, takes_to="search"),
            Button(label="🔍 Search again", style=ButtonStyle.green, takes_to="show_results"),
            Button(label="🏠 Home", style=ButtonStyle.primary, takes_to="home"),
        ],
    ),
}
