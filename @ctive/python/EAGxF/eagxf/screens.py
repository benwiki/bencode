import discord
from discord import ButtonStyle

from eagxf.button import Button
from eagxf.constant_functions import PAGE_REFERENCE, PROFILE
from eagxf.constants import (
    APP_NAME,
    COMMA_AND_SEPARATED,
    COMMA_SEPARATED_MAP,
    DEFAULT_PRIO_ORDER,
    MAX_PROP_LENGTH,
    MEETINGS,
    NUM_EMOJI,
    PRIO_LIST_LENGTH,
    QUESTION_NAMES,
    VISIBLE_SIMPLE_USER_PROPS,
)
from eagxf.enums.button_condition import ButtonCond
from eagxf.enums.effect import Effect
from eagxf.enums.property import Property
from eagxf.enums.screen_condition import ScreenCond
from eagxf.enums.screen_id import ScreenId
from eagxf.screen import Screen
from eagxf.status import STATUS_EMOJI

SCREENS: dict[ScreenId, Screen] = {
    ScreenId.HOME: Screen(
        message="ℹ️ Status: <status>"
        f"\n\nWelcome to {APP_NAME}, **<name>**!"
        "\nClick the buttons to use the app!",
        buttons=[
            Button(
                label="👤 Profile", takes_to=ScreenId.PROFILE, style=ButtonStyle.primary
            ),
            Button(label="🔍 Search", takes_to=ScreenId.SEARCH),
            Button(
                label="✨ Best Matches",
                takes_to=ScreenId.BEST_MATCHES,
                style=ButtonStyle.primary,
            ),
            Button(label="Interests", takes_to=ScreenId.INTERESTS, emoji="↕️"),
            Button(
                label="👆👇 Recommendations",
                takes_to=ScreenId.RECOMMENDATIONS,
                style=ButtonStyle.primary,
                row=1,
            ),
            Button(label="🗓️ Meetings", takes_to=ScreenId.MEETINGS, row=1),
        ],
    ),
    ScreenId.PROFILE: Screen(
        message=PROFILE(),
        buttons=[
            Button.back(),
            Button(
                label="✏️ Edit",
                takes_to=ScreenId.EDIT_PROFILE,
                style=ButtonStyle.primary,
            ),
        ],
    ),
    ScreenId.EDIT_PROFILE: Screen(
        message=PROFILE() + "\n\n✏️ **Editing Profile**" "\nWhat do you want to change?",
        buttons=[
            *Button.simple_prop_buttons("edit", before_questions=True),
            *Button.question_buttons("edit"),
            *Button.simple_prop_buttons("edit", before_questions=False),
            Button(
                label="Status",
                takes_to=ScreenId.EDIT_STATUS,
                emoji=discord.PartialEmoji(name="ℹ️"),
                row=3,
            ),
            *Button.back_home(row=4),
        ],
        stop_screen=True,
    ),
    ScreenId.EDIT_STATUS: Screen(
        message="Your current status is:\n*<status>*"
        "\nWhat do you want to change your status to?"
        "\n(Select the corresponding reaction!)\n"
        + "\n".join(
            f"{emoji} ({status.value})" for status, emoji in STATUS_EMOJI.items()
        ),
        reactions=list(STATUS_EMOJI.values()),
        changed_property=Property.STATUS,
        conditions=[ScreenCond.PROFILE_COMPLETE],
        buttons=[*Button.back_home()],
    ),
    ScreenId.SEARCH: Screen(
        message="🔍 **Search**\n\n"
        f"{PROFILE(search=True)}"
        "\n\nClick the buttons to change the filters!",
        buttons=[
            *Button.simple_prop_buttons("search", before_questions=True),
            *Button.question_buttons("search"),
            *Button.simple_prop_buttons("search", before_questions=False),
            Button(
                label="Status",
                takes_to=ScreenId.SEARCH_STATUS,
                emoji=discord.PartialEmoji(name="ℹ️"),
                row=3,
            ),
            Button.back(row=4),
            Button(
                label="SHOW RESULTS",
                style=ButtonStyle.green,
                takes_to=ScreenId.SHOW_SEARCH_RESULTS,
                row=4,
            ),
        ],
        conditions=[ScreenCond.VISIBLE],
        stop_screen=True,
    ),
    ScreenId.SEARCH_STATUS: Screen(
        message="What status do you want to search for?"
        "\n(Select the corresponding reaction!)\n"
        + "\n".join(
            [f"{emoji} ({status.value})" for status, emoji in STATUS_EMOJI.items()]
            + ["❓ (Any)"]
        ),
        reactions=list(STATUS_EMOJI.values()) + ["❓"],
        changed_property=Property.SEARCH_STATUS,
        buttons=[*Button.back_home()],
    ),
    ScreenId.SHOW_SEARCH_RESULTS: Screen(
        message="🔍 **Search Results**"
        f"\n\n{PROFILE(search=True)}"
        "\n\n**Results**\n" + PAGE_REFERENCE("select a user", "<search_results>"),
        paged=True,
        buttons=[
            Button(
                label="🔍 Search again",
                style=ButtonStyle.green,
                takes_to=ScreenId.SHOW_SEARCH_RESULTS,
            ),
            *Button.back_home(row=1),
        ],
    ),
    ScreenId.BEST_MATCHES: Screen(
        message="✨ **Best matches**"
        "\n\nHere we have sorted all current users according to how well they match your interests"
        " and expertise. Feel free to browse and correct us if you find that our algorithm"
        " doesn't bring you the most suitable people!"
        "\n\n**Results**\n" + PAGE_REFERENCE("select a user", "<best_matches>"),
        paged=True,
        buttons=[
            Button.back(row=1),
            Button(
                label="✏️ Change priority",
                takes_to=ScreenId.CHANGE_BEST_MATCHES_PRIORITY,
                style=ButtonStyle.primary,
                row=1,
            ),
        ],
        conditions=[ScreenCond.VISIBLE],
    ),
    ScreenId.CHANGE_BEST_MATCHES_PRIORITY: Screen(
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
        after_button_effects=[
            Effect.DELETE_MESSAGE,
            Effect.RESET_NEW_PRIO_ORDER,
            Effect.RESET_USER_PROPERTY_CHANGE,
        ],
        buttons=[
            Button(label="*️⃣ Default", takes_to=ScreenId.DEFAULT_BEST_MATCHES_CONFIRM),
            Button(
                label="🔄 Reset",
                takes_to=ScreenId.CHANGE_BEST_MATCHES_PRIORITY,
                style=ButtonStyle.red,
            ),
            *Button.back_home(row=1),
        ],
        changed_property=Property.BEST_MATCH_PRIO_ORDER,
        reactions=NUM_EMOJI[:PRIO_LIST_LENGTH],
    ),
    ScreenId.DEFAULT_BEST_MATCHES_CONFIRM: Screen(
        message="__The default priority order is:__"
        "\n1. "
        + "\n{}. ".join(DEFAULT_PRIO_ORDER).format(*range(2, PRIO_LIST_LENGTH + 1))
        + "\n\nAre you sure you want to reset your priority order to this?\n"
        + r"\_" * 50,
        buttons=[
            Button(label="No", takes_to=ScreenId.CHANGE_BEST_MATCHES_PRIORITY),
            Button(
                label="Yes",
                takes_to=ScreenId.BEST_MATCHES,
                effects=[Effect.DEFAULT_BEST_MATCHES],
                style=ButtonStyle.primary,
            ),
        ],
    ),
    ScreenId.INTERESTS: Screen(
        message="↕️ Interests"
        "\n\nHere you can see, who is interested in you, "
        "and whom did you send interest."
        "\n\nNumber of interests __sent__: **<num_of_interests_sent>**"
        "\nNumber of interests __received__: **<num_of_interests_received>**"
        "\nNumber of __mutual__ interests: **<num_of_mutual_interests>**"
        "\n\nClick the buttons to navigate!",
        buttons=[
            Button(label="⬆️ Sent", takes_to=ScreenId.INTERESTS_SENT),
            Button(label="⬇️ Received", takes_to=ScreenId.INTERESTS_RECEIVED),
            Button(label="✅ Mutual", takes_to=ScreenId.MUTUAL_INTERESTS),
            Button.back(row=1),
        ],
    ),
    ScreenId.INTERESTS_SENT: Screen(
        message="⬆️ **Interests sent**"
        "\n\nHere you can see, who you sent interest to.\n\n"
        + PAGE_REFERENCE("manage the interest", "<interests_sent>"),
        paged=True,
        buttons=[*Button.back_home()],
    ),
    ScreenId.INTERESTS_RECEIVED: Screen(
        message="⬇️ **Interests received**"
        "\n\nHere you can see, who is interested in you.\n\n"
        + PAGE_REFERENCE("manage the interest", "<interests_received>"),
        paged=True,
        buttons=[*Button.back_home()],
    ),
    ScreenId.MUTUAL_INTERESTS: Screen(
        message="✅ **Mutual interests**"
        "\n\nHere you can see the people who you have a mutual interest with.\n\n"
        + PAGE_REFERENCE("manage the interest", "<mutual_interests>"),
        paged=True,
        buttons=[*Button.back_home()],
    ),
    ScreenId.SELECTED_USER: Screen(
        message="You have selected ***<selected_user_name>*** !"
        "\n\n<selected_user_profile>"
        "\n\nYour interest status with this user:\n**<interest_status>**"
        "\n\n🗓️ Meetings with this user:"
        "\n<selected_user_meetings>"
        "<video_call_link>"
        "\n\nWhat do you want to do with this user?",
        buttons=[
            Button(
                label="⬆️ Send interest",
                takes_to=ScreenId.SELECTED_USER,
                conditions=[ButtonCond.CAN_SEND_INTEREST],
                effects=[Effect.SEND_INTEREST],
            ),
            Button(
                label="❌ Cancel interest",
                takes_to=ScreenId.SELECTED_USER,
                conditions=[ButtonCond.CAN_CANCEL_INTEREST],
                effects=[Effect.CANCEL_INTEREST],
            ),
            Button(
                label="✅ Confirm interest",
                takes_to=ScreenId.SELECTED_USER,
                conditions=[ButtonCond.CAN_CONFIRM_INTEREST],
                effects=[Effect.SEND_INTEREST],
            ),
            Button(
                label="📅 Request meeting",
                takes_to=ScreenId.MEETING_REQUEST,
                conditions=[ButtonCond.CAN_REQUEST_MEETING],
            ),
            Button(
                label="🛠️ Manage meetings",
                takes_to=ScreenId.MEETINGS,
                conditions=[ButtonCond.HAS_MEETINGS],
            ),
            Button(
                label="📞 Start call",
                takes_to=ScreenId.SELECTED_USER,
                conditions=[ButtonCond.CAN_START_CALL],
                effects=[Effect.START_CALL],
                style=ButtonStyle.green,
            ),
            Button(
                label="❌ Cancel call",
                takes_to=ScreenId.SELECTED_USER,
                conditions=[ButtonCond.CAN_CANCEL_CALL],
                effects=[Effect.CANCEL_CALL],
            ),
            Button(
                label="👆 Recommend to a connection",
                takes_to=ScreenId.RECOMMEND_USER,
                row=1,
            ),
            *Button.back_home(row=2),
        ],
        stop_screen=True,
    ),
    ScreenId.MEETING_REQUEST: Screen(
        message="📅 **Meeting Request**"
        "\n\nYou are requesting a meeting with ***<selected_user_name>*** !"
        "\n\nPlease specify a date and time (in the future) for the meeting in this format:"
        "\n**dd.mm.yyyy hh:mm**"
        "\nand send it via text message."
        "\n\nExample: 23.05.<next_year> 09:30",
        changed_property=Property.MEETING_REQUEST,
        buttons=[*Button.back_home()],
    ),
    ScreenId.MEETINGS: Screen(
        message="🗓️ **Meetings**"
        "\n\n( **<num_of_past_meetings>** )  ◀️ Past meetings:"
        "\n<past_meetings_peek>"
        "\n\n( **<num_of_future_meetings>** )  ▶️ Future meetings:"
        "\n<future_meetings_peek>"
        "\n\nDo you want to manage past or future meetings?",
        buttons=[
            Button(label="◀️ Past", takes_to=ScreenId.PAST_MEETINGS),
            Button(label="▶️ Future", takes_to=ScreenId.FUTURE_MEETINGS),
            *Button.back_home(row=1),
        ],
    ),
    ScreenId.EDIT_MEETING: Screen(
        message="You have selected a meeting with ***<selected_user_name>*** "
        "at **<selected_meeting_time>** !"
        "\n\nWhat do you want to do with this meeting?",
        buttons=[
            Button(
                label="❌ Cancel meeting",
                takes_to=ScreenId.CANCEL_MEETING_CONFIRM,
                conditions=[ButtonCond.CAN_CANCEL_MEETING],
            ),
            Button(
                label="🗑️ Delete meeting",
                takes_to=ScreenId.DELETE_MEETING_CONFIRM,
                conditions=[ButtonCond.CAN_DELETE_MEETING],
            ),
            Button(
                label="📅 Change date",
                takes_to=ScreenId.CHANGE_MEETING_DATE,
                conditions=[ButtonCond.CAN_CHANGE_MEETING_DATE],
            ),
            Button(
                label="👤 Go to their profile",
                takes_to=ScreenId.SELECTED_USER,
                style=ButtonStyle.primary,
            ),
            *Button.back_home(row=1),
        ],
    ),
    ScreenId.CHANGE_MEETING_DATE: Screen(
        message="You want to change the meeting with ***<selected_user_name>*** "
        "at **<selected_meeting_time>** !"
        "\n\nPlease specify a new date and time for the meeting in this format:"
        "\n**dd.mm.yyyy hh:mm**"
        "\nand send it via text message."
        "\n\nExample: 03.11.2024 09:30",
        changed_property=Property.CHANGE_MEETING_DATE,
        buttons=[*Button.back_home()],
    ),
    ScreenId.INVALID_DATE: Screen(
        message="❌ Invalid date, try again!\nFormat should be: **dd.mm.yyyy hh:mm**"
        "\nAnd it should be in the future!",
        buttons=[*Button.ok_home()],
        spacer=False,
    ),
    ScreenId.TOO_LONG_PROP_TEXT: Screen(
        message="❌ <changed_prop> is too long! "
        f"Max length is {MAX_PROP_LENGTH} characters."
        "\n\nYou have <exceeding_number> too many."
        "\n\nHint: The last <exceeding_number> characters are:"
        "```<to_cut_off>```"
        "\nSo if you'd chop this off, you'd be good to go.",
        buttons=[*Button.ok_home()],
        spacer=False,
    ),
    ScreenId.SUCCESSFUL_PROP_CHANGE: Screen(
        message="✅ Successfully <changed_prop> to <new_value>!<plus_info>",
        buttons=[*Button.ok_home()],
        spacer=False,
    ),
    ScreenId.DELETING_OLD_MESSAGES: Screen(
        message="🗑️ Deleting old messages... Hang on tight!",
        buttons=[],
        spacer=False,
    ),
    ScreenId.ALREADY_IN_PLATFORM: Screen(
        message="You are already in the platform! :)",
        buttons=[Button.home()],
        spacer=False,
    ),
    ScreenId.RECOMMEND_USER: Screen(
        message="👆🔄️ Recommending ***<user_to_recommend>*** to a "
        "connection of yours\n\n"
        + PAGE_REFERENCE(
            action="select the connection that you want to recommend "
            "<user_to_recommend> to",
            content="<mutual_interests>",
        ),
        changed_property=Property.SEND_RECOMMENDATION,
        paged=True,
    ),
    ScreenId.RECOMMENDATIONS: Screen(
        message="👆👇 **Recommendations**"
        "\n\n( **<num_of_recommendations_sent>** ) 👆 Recommendations sent:"
        "\n<recommendations_sent_peek>"
        "\n\n( **<num_of_recommendations_received>** ) 👇 Recommendations received:"
        "\n<recommendations_received_peek>"
        "\n\nClick the buttons to navigate!",
        buttons=[
            Button(label="👆 Sent", takes_to=ScreenId.RECOMMENDATIONS_SENT),
            Button(label="👇 Received", takes_to=ScreenId.RECOMMENDATIONS_RECEIVED),
            *Button.back_home(row=1),
        ],
    ),
    ScreenId.RECOMMENDATIONS_SENT: Screen(
        message="👆 **Recommendations sent**"
        "\n\nYou recommended...\n\n"
        + PAGE_REFERENCE("manage the recommendation", "<recommendations_sent>"),
        paged=True,
        buttons=[*Button.back_home()],
        changed_property=Property.RECOMMENDATION,
        stop_screen=True,
    ),
    ScreenId.RECOMMENDATIONS_RECEIVED: Screen(
        message="👇 **Recommendations received**"
        "\n\nThese people have been recommended to you:\n\n"
        + PAGE_REFERENCE("manage the recommendation", "<recommendations_received>"),
        paged=True,
        buttons=[*Button.back_home()],
        changed_property=Property.RECOMMENDATION,
        stop_screen=True,
    ),
    ScreenId.SUCCESSFUL_RECOMMENDATION: Screen(
        message="✅ Successfully recommended ***<recommended_user_name>*** to ***<connection_name>***!",
        buttons=[*Button.ok_home()],
        spacer=False,
    ),
    ScreenId.RECOMMENDATION: Screen(
        message="You have selected a recommendation, where you recommended "
        "***<recommendation_receiver_name>*** to *<recommended_person_name>*."
        "\n\nWhat do you want to do with this recommendation?",
        buttons=[
            Button(
                label="❌ Cancel recommendation",
                takes_to=ScreenId.CANCEL_RECOMMENDATION_CONFIRM,
                # conditions=[ButtonCond.CAN_CANCEL_RECOMMENDATION],
            ),
            Button(
                label="👤 Recommended person's profile",
                takes_to=ScreenId.SELECTED_USER,
                style=ButtonStyle.primary,
            ),
            *Button.back_home(row=1),
        ],
    ),
    ScreenId.CANCEL_RECOMMENDATION_CONFIRM: Screen(
        message="Are you sure you want to cancel the recommendation of "
        "***<recommendation_receiver_name>*** to *<recommended_person_name>*?",
        buttons=[
            Button(label="No", takes_to=ScreenId.RECOMMENDATION),
            Button(
                label="Yes",
                takes_to=ScreenId.BACK_UNTIL_STOP__,
                effects=[Effect.CANCEL_RECOMMENDATION],
                style=ButtonStyle.red,
            ),
        ],
    ),
    # ______________________________________________________________
    # ==================== GENERATED SCREENS =======================
    # ______________________________________________________________
    **{  # Confirm "cancel" or "delete" meeting
        ScreenId.confirm(kw): Screen(
            message=f"Are you sure you want to {kw} the meeting at "
            "**<selected_meeting_time>** with ***<selected_user_name>*** ?",
            buttons=[
                Button(label="No", takes_to=ScreenId.BACK__),
                Button(
                    label="Yes",
                    takes_to=ScreenId.BACK_UNTIL_STOP__,
                    effects=[Effect.CANCEL_MEETING],
                    style=ButtonStyle.red,
                ),
            ],
        )
        for kw in ("cancel", "delete")
    },
    **{  # FUTURE and PAST meetings
        ScreenId.meetings(time_id.to_str): Screen(
            message=f"{time['emoji']} **{time['label']}**\n\n"
            + PAGE_REFERENCE("manage the meeting", f"<{time_id}_meetings>"),
            paged=True,
            buttons=[*Button.back_home()],
            changed_property=Property.MEETING,
            stop_screen=True,
        )
        for time_id, time in MEETINGS.items()
    },
    **{  # Edit questions
        ScreenId.edit(q_id.to_str): Screen(
            message=f"Your current answer to **'{question['text']}'** is:\n*<{q_id}>*"
            "\n\nWhat do you want to change it to?",
            changed_property=q_id,
            buttons=[*Button.back_home()],
        )
        for q_id, question in QUESTION_NAMES.items()
    },
    **{  # Edit simple properties
        ScreenId.edit(prop_id.to_str): Screen(
            message=f"Your current {prop_id} "
            f"{'are' if prop['comma_separated'] else 'is'}"
            f":\n*<{prop_id}>*"
            f"\n\nWhat do you want to change your {prop_id} to?"
            + (
                f"\n(Comma separated, e.g. {prop['example']})"
                if prop["comma_separated"]
                else ""
            ),
            changed_property=prop_id,
            buttons=[*Button.back_home()],
        )
        for prop_id, prop in VISIBLE_SIMPLE_USER_PROPS.items()
    },
    **{  # Search simple properties
        ScreenId.search(prop_id.to_str): Screen(
            message=f"What {prop_id} do you want to search for?"
            + COMMA_SEPARATED_MAP.get(prop_id, "")
            + f"\n\nCurrent filter:\n*<search_{prop_id}>*"
            "\n\nType ? to search for any.",
            changed_property=Property.search(prop_id),
            buttons=[*Button.back_home()],
        )
        for prop_id in VISIBLE_SIMPLE_USER_PROPS
    },
    **{  # Search questions
        ScreenId.search(q_id.to_str): Screen(
            message=f"What keywords do you want to search for in the answers to the question:"
            f"\n**'{question['text']}'**"
            f"{COMMA_AND_SEPARATED}"
            f"\n\nCurrent filter:\n*<search_{q_id}>*"
            "\n\nType ? to search for any keyword.",
            changed_property=Property.search(q_id),
            buttons=[*Button.back_home()],
        )
        for q_id, question in QUESTION_NAMES.items()
    },
}
