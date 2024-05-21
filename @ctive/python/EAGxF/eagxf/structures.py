import discord
from discord import ButtonStyle

from eagxf.button import Button
from eagxf.constant_functions import ANSWERS, PROFILE
from eagxf.constants import (
    APP_NAME,
    COMMA_AND_SEPARATED,
    COMMA_SEPARATED_MAP,
    DEFAULT_PRIO_ORDER,
    NUM_EMOJI,
    PRIO_LIST_LENGTH,
    QUESTION_NAMES,
    STATUS_EMOJI,
    VISIBLE_SIMPLE_USER_PROPS,
)
from eagxf.structure import Structure


def back_home(row=None):
    return [
        Button(label="⬅️ Back", takes_to="<back>", row=row),
        Button(label="🏠 Home", style=ButtonStyle.primary, takes_to="home", row=row),
    ]


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
            Button(label="🗓️ Meetings", takes_to="meetings", style=ButtonStyle.primary),
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
            *Button.simple_prop_buttons("edit", before_questions=True),
            Button(
                label="Answers to ❓Questions",
                takes_to="edit_answers",
                row=2,
            ),
            *Button.simple_prop_buttons("edit", before_questions=False),
            Button(
                label="Status",
                takes_to="edit_status",
                emoji=discord.PartialEmoji(name="ℹ️"),
                row=3,
            ),
            *back_home(row=4),
        ],
    ),
    "edit_answers": Structure(
        message="**Your current answers to questions are:**"
        f"\n{ANSWERS()}"
        "\n\nWhat do you want to change?",
        buttons=[
            *Button.question_buttons("edit"),
            *back_home(row=1),
        ],
        stacked=False,
    ),
    **{  # Edit simple properties
        f"edit_{prop_id}": Structure(
            message=f"Your current {prop_id} is:\n*<{prop_id}>*"
            f"\n\nWhat do you want to change your {prop_id} to?",
            changed_property=prop_id,
            buttons=back_home(),
            stacked=False,
        )
        for prop_id, prop in VISIBLE_SIMPLE_USER_PROPS.items()
        if not prop["comma_separated"]
    },
    **{  # Edit simple comma separated properties
        f"edit_{prop_id}": Structure(
            message=f"Your current {prop_id} are:\n*<{prop_id}>*"
            f"\n\nWhat do you want to change your {prop_id} to?"
            f"\n(Comma separated, e.g. {prop['example']})",
            changed_property=prop_id,
            buttons=back_home(),
            stacked=False,
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
        changed_property="status",
        condition="profile_complete",
        buttons=back_home(),
        stacked=False,
    ),
    **{  # Edit questions
        f"edit_{q_id}": Structure(
            message=f"Your current answer to **'{question['text']}'** is:\n*<{q_id}>*"
            "\n\nWhat do you want to change it to?",
            changed_property=q_id,
            buttons=back_home(),
            stacked=False,
        )
        for q_id, question in QUESTION_NAMES.items()
    },
    "search": Structure(
        message="🔍 **Search**\n\n"
        f"{PROFILE(search=True)}"
        "\n\nClick the buttons to change the filters!",
        buttons=[
            *Button.simple_prop_buttons("search", before_questions=True),
            Button(
                label="Answers to ❓Questions",
                takes_to="edit_search_answers",
                row=2,
            ),
            *Button.simple_prop_buttons("search", before_questions=False),
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
            *Button.question_buttons("search"),
            *back_home(row=1),
        ],
        stacked=False,
    ),
    **{  # Search simple properties
        f"search_{prop_id}": Structure(
            message=f"What {prop_id} do you want to search for?"
            + COMMA_SEPARATED_MAP.get(prop_id, "")
            + f"\n\nCurrent filter:\n*<search_{prop_id}>*"
            "\n\nType ? to search for any.",
            changed_property=f"search_{prop_id}",
            buttons=back_home(),
            stacked=False,
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
        changed_property="search_status",
        buttons=back_home(),
        stacked=False,
    ),
    **{  # Search questions
        f"search_{q_id}": Structure(
            message=f"What keywords do you want to search for in the answers to the question:"
            f"\n**'{question['text']}'**"
            f"{COMMA_AND_SEPARATED}"
            f"\n\nCurrent filter:\n*<search_{q_id}>*"
            "\n\nType ? to search for any keyword.",
            changed_property=f"search_{q_id}",
            buttons=back_home(),
            stacked=False,
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
            *back_home(row=1),
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
            "\n<prio_order>"
            "\n\n__The default order to select from:__"
            f"\n{NUM_EMOJI[0]}**.** "
            + "\n{}**.** ".join(DEFAULT_PRIO_ORDER).format(
                *NUM_EMOJI[1:PRIO_LIST_LENGTH]
            )
            + "\n\n__Your new order:__"
            "\n<prio_order_new>\n" + r"\_" * 50
        ),
        after_button_effects="delete_message, reset_new_prio_order, reset_user_property_change",
        buttons=[
            Button(label="*️⃣ Default", takes_to="default_best_matches_confirm"),
            Button(label="🔄 Reset", takes_to="change_priority", style=ButtonStyle.red),
            *back_home(row=1),
        ],
        changed_property="best_match_prio_order",
        reactions=NUM_EMOJI[:PRIO_LIST_LENGTH],
    ),
    "default_best_matches_confirm": Structure(
        message="__The default priority order is:__"
        "\n1. "
        + "\n{}. ".join(DEFAULT_PRIO_ORDER).format(*range(2, PRIO_LIST_LENGTH + 1))
        + "\n\n**Are you sure** you want to reset your priority order to this?\n"
        + r"\_" * 50,
        buttons=[
            Button(
                label="No", takes_to="change_priority", effects="cancel_change_prio"
            ),
            Button(
                label="Yes",
                takes_to="best_matches",
                effects="default_best_matches",
                style=ButtonStyle.primary,
            ),
        ],
        stacked=False,
    ),
    "interests": Structure(
        message="↕️ Interests"
        "\n\nHere you can see, who is interested in you, "
        "and whom did you send interest."
        "\n\nNumber of interests __sent__: **<num_of_interests_sent>**"
        "\nNumber of interests __received__: **<num_of_interests_received>**"
        "\nNumber of __mutual__ interests: **<num_of_mutual_interests>**"
        "\n\nClick the buttons to navigate!",
        buttons=[
            Button(label="⬆️ Sent", takes_to="interests_sent"),
            Button(label="⬇️ Received", takes_to="interests_received"),
            Button(label="✅ Mutual", takes_to="mutual_interests"),
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
        buttons=back_home(),
    ),
    "interests_received": Structure(
        message="⬇️ **Interests received**"
        "\n\nHere you can see, who is interested in you."
        "\n\n<page_reference>"
        "\nClick on the corresponding reaction to manage the interest!"
        "\n\n<interests_received>"
        "\n\n<page_reference>",
        paged=True,
        buttons=back_home(),
    ),
    "mutual_interests": Structure(
        message="✅ **Mutual interests**"
        "\n\nHere you can see the people who you have a mutual interest with.."
        "\n\n<page_reference>"
        "\nClick on the corresponding reaction to manage the interest!"
        "\n\n<mutual_interests>"
        "\n\n<page_reference>",
        paged=True,
        buttons=back_home(),
    ),
    "selected_user": Structure(
        message="You have selected ***<selected_user_name>*** !"
        "\n\n<selected_user_profile>"
        "\n\nYour interest status with this user:\n**<interest_status>**"
        "\n\nMeetings with this user:"
        "\n<selected_user_meetings>"
        "\n\nWhat do you want to do with this user?",
        buttons=[
            Button(
                label="⬆️ Send interest",
                takes_to="selected_user",
                conditions="can_send_interest",
                effects="send_interest",
            ),
            Button(
                label="❌ Cancel interest",
                takes_to="selected_user",
                conditions="can_cancel_interest",
                effects="cancel_interest",
            ),
            Button(
                label="✅ Confirm interest",
                takes_to="selected_user",
                conditions="can_confirm_interest",
                effects="send_interest",
            ),
            Button(
                label="📅 Request meeting",
                takes_to="meeting_request",
                conditions="can_request_meeting",
            ),
            Button(
                label="❌ Cancel meeting",
                takes_to="cancel_meeting_confirm",
                conditions="can_cancel_meeting",
            ),
            *back_home(row=2),
        ],
    ),
    "meeting_request": Structure(
        message="📅 **Meeting Request**"
        "\n\nYou are requesting a meeting with ***<selected_user_name>*** !"
        "\n\nPlease specify a date and time for the meeting in this format:"
        "\ndd.mm.yyyy hh:mm"
        "\n\nExample: 03.11.2024 09:30",
        changed_property="meeting_request",
        buttons=back_home(),
        stacked=False,
    ),
    "cancel_meeting_confirm": Structure(
        message="Are you sure you want to cancel the meeting with ***<selected_user_name>*** ?",
        buttons=[
            Button(label="No", takes_to="selected_user"),
            Button(
                label="Yes",
                takes_to="selected_user",
                effects="cancel_meeting",
                style=ButtonStyle.red,
            ),
        ],
        stacked=False,
    ),
    "meetings": Structure(
        message="🗓️ **Meetings**"
        "\n\n( **<num_of_upcoming_meetings>** ) Upcoming meetings:"
        "\n<upcoming_meetings>"
        "\n\n( **<num_of_past_meetings>** ) Past meetings:"
        "\n<past_meetings>"
        "\n\nChoose a meeting to manage it! (coming soon)",
        buttons=back_home(),
    ),
}
