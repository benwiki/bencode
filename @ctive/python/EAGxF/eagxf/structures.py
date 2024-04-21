import discord
from discord import ButtonStyle

from eagxf.button import Button
from eagxf.constants import (
    ANSWERS,
    APP_NAME,
    COMMA_AND_SEPARATED,
    COMMA_AND_SEPARATED_LANGUAGES,
    DEFAULT_PRIO_ORDER,
    NUM_EMOJI,
    PRIO_LIST_LENGTH,
    PROFILE,
    QUESTION_BUTTONS,
    QUESTION_NAMES,
    SIMPLE_PROP_BUTTONS,
    STATUS_EMOJI,
    VISIBLE_SIMPLE_USER_PROPS,
)
from eagxf.structure import Structure

STRUCTURES = {
    "home": Structure(
        message="ℹ️ Status: <status>"
        f"\n\nWelcome to {APP_NAME}, **<name>**!"
        "\nClick the buttons to use the app!",
        buttons=[
            Button(label="👤 Profile", takes_to="profile", style=ButtonStyle.primary),
            Button(label="🔍 Search", takes_to="search"),
            Button(
                label="✨ Best Matches",
                takes_to="best_matches",
                style=ButtonStyle.primary,
            ),
            Button(label="Interests", takes_to="interests", emoji="↕️"),
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
            *SIMPLE_PROP_BUTTONS("edit", before_questions=True),
            Button(
                label="Answers to ❓Questions",
                takes_to="edit_answers",
                row=2,
            ),
            *SIMPLE_PROP_BUTTONS("edit", before_questions=False),
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
    "edit_answers": Structure(
        message="**Your current answers to questions are:**"
        f"\n{ANSWERS()}"
        "\n\nWhat do you want to change?",
        buttons=[
            *QUESTION_BUTTONS("edit"),
            Button(label="⬅️ Back", takes_to="edit_profile", row=1),
            Button(label="🏠 Home", style=ButtonStyle.primary, takes_to="home", row=1),
        ],
    ),
    **{  # Edit simple properties
        f"edit_{prop_id}": Structure(
            message=f"Your current {prop_id} is:\n*<{prop_id}>*"
            f"\n\nWhat do you want to change your {prop_id} to?",
            changes_property=prop_id,
        )
        for prop_id, prop in VISIBLE_SIMPLE_USER_PROPS.items()
        if not prop["comma_separated"]
    },
    **{  # Edit simple comma separated properties
        f"edit_{prop_id}": Structure(
            message=f"Your current {prop_id} are:\n*<{prop_id}>*"
            f"\n\nWhat do you want to change your {prop_id} to?"
            f"\n(Comma separated, e.g. {prop['example']})",
            changes_property=prop_id,
        )
        for prop_id, prop in VISIBLE_SIMPLE_USER_PROPS.items()
        if prop["comma_separated"]
    },
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
    **{  # Edit questions
        f"edit_{q_id}": Structure(
            message=f"Your current answer to **'{question['text']}'** is:\n*<{q_id}>*"
            "\n\nWhat do you want to change it to?",
            changes_property=q_id,
        )
        for q_id, question in QUESTION_NAMES.items()
    },
    "search": Structure(
        message="🔍 **Search**\n\n"
        f"{PROFILE(search=True)}"
        "\n\nClick the buttons to change the filters!",
        buttons=[
            *SIMPLE_PROP_BUTTONS("search", before_questions=True),
            Button(
                label="Answers to ❓Questions",
                takes_to="edit_search_answers",
                row=2,
            ),
            *SIMPLE_PROP_BUTTONS("search", before_questions=False),
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
                takes_to="show_search_results",
                row=4,
            ),
        ],
    ),
    "edit_search_answers": Structure(
        message="**The current question filters are:**"
        f"\n{ANSWERS(search=True)}"
        "\n\nWhat do you want to change?",
        buttons=[
            *QUESTION_BUTTONS("search"),
            Button(label="⬅️ Back", takes_to="search", row=1),
            Button(label="🏠 Home", style=ButtonStyle.primary, takes_to="home", row=1),
        ],
    ),
    **{  # Search simple properties
        f"search_{prop_id}": Structure(
            message=f"What {prop_id} do you want to search for?"
            + (
                COMMA_AND_SEPARATED
                if prop_id == "keywords"
                else COMMA_AND_SEPARATED_LANGUAGES if prop_id == "languages" else ""
            )
            + f"\n\nCurrent filter:\n*<search_{prop_id}>*"
            "\n\nType ? to search for any.",
            changes_property=f"search_{prop_id}",
        )
        for prop_id in VISIBLE_SIMPLE_USER_PROPS
    },
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
    **{  # Search questions
        f"search_{q_id}": Structure(
            message=f"What keywords do you want to search for in the answers to the question:"
            f"\n**'{question['text']}'**"
            f"{COMMA_AND_SEPARATED}"
            f"\n\nCurrent filter:\n*<search_{q_id}>*"
            "\n\nType ? to search for any keyword.",
            changes_property=f"search_{q_id}",
        )
        for q_id, question in QUESTION_NAMES.items()
    },
    "show_search_results": Structure(
        message="🔍 **Search Results**"
        f"\n\n{PROFILE(search=True)}"
        "\n\n**Results** <page_reference>"
        "\nClick on the corresponding reaction to select a user!"
        "\n\n<search_results>"
        "\n\n<page_reference>",
        paged=True,
        buttons=[
            Button(
                label="🔍 Search again",
                style=ButtonStyle.green,
                takes_to="show_search_results",
            ),
            Button(label="⬅️ Back", takes_to="search", row=1),
            Button(label="🏠 Home", style=ButtonStyle.primary, takes_to="home", row=1),
        ],
    ),
    "best_matches": Structure(
        message="✨ **Best matches**"
        "\n\nHere we have sorted all current users according to how well they match your interests"
        " and expertise. Feel free to browse and correct us if you find that our algorithm"
        " doesn't bring you the most suitable people!"
        "\n\n**Results** <page_reference>"
        "\nClick on the corresponding reaction to select a user!"
        "\n\n<best_matches>"
        "\n\n<page_reference>",
        paged=True,
        buttons=[
            Button(label="⬅️ Back", takes_to="home", row=1),
            Button(
                label="✏️ Change priority",
                takes_to="change_priority",
                style=ButtonStyle.primary,
                row=1,
            ),
        ],
    ),
    "change_priority": Structure(
        message=(
            PRIORITY_MESSAGE := "✨✏️ Best matches **priority change**"
            "\n\nHere you can change the priority order of your best matches."
            "\n***Click a number-reaction "
            f"({NUM_EMOJI[0]} - {NUM_EMOJI[PRIO_LIST_LENGTH - 1]}) "
            "to add the corresponding element to your new order!***"
            f"\nIf you select {PRIO_LIST_LENGTH - 1} or less elements, "
            "the omitted ones won't be considered in the matching process."
            "\n\n__Your current order:__"
            "\n<best_match_prio_order>"
            "\n\n__The default order to select from:__"
            f"\n{NUM_EMOJI[0]}**.** "
            + "\n{}**.** ".join(DEFAULT_PRIO_ORDER).format(
                *NUM_EMOJI[1:PRIO_LIST_LENGTH]
            )
            + "\n\n__Your new order:__"
            "\n<best_match_prio_order_new>\n" + r"\_" * 50
        ),
        after_button_effects="delete_message, reset_new_prio_order, reset_user_property_change",
        buttons=[
            Button(label="*️⃣ Default", takes_to="default_best_matches_confirm"),
            Button(label="🔄 Reset", takes_to="change_priority", style=ButtonStyle.red),
            Button(label="⬅️ Back", takes_to="best_matches", row=1),
            Button(label="🏠 Home", takes_to="home", style=ButtonStyle.primary, row=1),
        ],
        changes_property="best_match_prio_order",
        reactions=NUM_EMOJI[:PRIO_LIST_LENGTH],
    ),
    "default_best_matches_confirm": Structure(
        message="__The default priority order is:__"
        "\n1. "
        + "\n{}. ".join(DEFAULT_PRIO_ORDER).format(*range(2, PRIO_LIST_LENGTH + 1))
        + "\n\n**Are you sure** you want to reset your priority order to this?\n"
        + r"\_" * 50,
        buttons=[
            Button(label="No", takes_to="change_priority", effect="cancel_change_prio"),
            Button(
                label="Yes",
                takes_to="best_matches",
                effect="default_best_matches",
                style=ButtonStyle.primary,
            ),
        ],
    ),
    "interests": Structure(
        message="↕️ Interests"
        "\n\nHere you can see, who is interested in you, "
        "and whom did you send interest."
        "\n\nNumber of interests sent: **<num_of_interests_sent>**"
        "\nNumber of interests received: **<num_of_interests_received>**"
        "\n\nClick the buttons to navigate!",
        buttons=[
            Button(label="⬆️ Interests sent", takes_to="interests_sent"),
            Button(label="⬇️ Interests received", takes_to="interests_received"),
            Button(label="⬅️ Back", takes_to="home", row=1),
        ],
    ),
    "interests_sent": Structure(
        message="⬆️ **Interests sent**"
        "\n\nHere you can see, who you sent interest to."
        "\n\n<page_reference>"
        "\nClick on the corresponding reaction to manage the interest!"
        "\n\n<interests_sent>"
        "\n\n<page_reference>",
        paged=True,
        buttons=[
            Button(label="⬅️ Back", takes_to="interests"),
            Button(label="🏠 Home", style=ButtonStyle.primary, takes_to="home"),
        ],
    ),
    "interests_received": Structure(
        message="⬇️ **Interests received**"
        "\n\nHere you can see, who is interested in you."
        "\n\n<page_reference>"
        "\nClick on the corresponding reaction to manage the interest!"
        "\n\n<interests_received>"
        "\n\n<page_reference>",
        paged=True,
        buttons=[
            Button(label="⬅️ Back", takes_to="interests"),
            Button(label="🏠 Home", style=ButtonStyle.primary, takes_to="home"),
        ],
    ),
    "selected_user": Structure(
        message="You have selected ***<selected_user_name>*** !"
        "\n\n<selected_user_profile>"
        "\n\nWhat do you want to do with this user?",
        buttons=[
            Button(
                label="⬆️ Send interest",
                takes_to="selected_user",
                condition="interest_not_sent",
                effect="send_interest",
            ),
            Button(
                label="❌ Cancel interest",
                takes_to="selected_user",
                condition="interest_sent",
                effect="cancel_interest",
            ),
            Button(label="⬅️ Back", takes_to="<back>", row=1),
            Button(label="🏠 Home", style=ButtonStyle.primary, takes_to="home", row=1),
        ],
    ),
}
