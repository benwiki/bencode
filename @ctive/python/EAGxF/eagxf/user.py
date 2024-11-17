import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional, TypeVar

import discord

from eagxf.button import Button
from eagxf.constants import (
    COMPLETE_PROFILE_HINT,
    DEFAULT_PRIO_ORDER,
    INCOMPLETE_PROFILE_WARNING,
    NOT_ALPHANUMERIC,
    NUM_EMOJI,
    PAGE_STEP,
    PRIO_LIST_LENGTH,
    QUESTION_PROPS,
    VISIBLE_SIMPLE_USER_PROPS,
)
from eagxf.date import Date
from eagxf.enums.button_condition import ButtonCond
from eagxf.enums.property import Property
from eagxf.enums.screen_condition import ScreenCond
from eagxf.enums.screen_id import ScreenId
from eagxf.interests import Interests
from eagxf.meetings import Meeting, Meetings
from eagxf.message import Message
from eagxf.message_bundle import MessageBundle
from eagxf.questions import Questions
from eagxf.recommendations import Recommendation, Recommendations
from eagxf.screen import Screen
from eagxf.status import STATUS_EMOJI, Status
from eagxf.typedefs import (
    DcButton,
    DcClient,
    DcEmoji,
    DcMessage,
    DcUser,
    DcView,
    Receiver,
    ReceiverFuture,
)
from eagxf.users_path import USERS_PATH
from eagxf.util import (
    CHANNELS,
    GUILD_ID,
    comma_and_search,
    get_guild,
    intersect,
    peek,
    subtract,
)

T = TypeVar("T")


@dataclass
class User:
    # Properties to save
    id: int = 0
    date_joined: Date = field(default_factory=Date.current)
    name: str = "?"  # max 50 chars
    job: str = "?"  # max 100 chars
    company: str = "?"  # max 50 chars
    location: str = "?"
    languages: str = "?"  # comma separated
    questions: Questions = field(default_factory=Questions)
    keywords: str = "?"  # comma separated
    status: Status = Status.INVISIBLE
    best_match_prio_order: list[int] = field(default_factory=list)
    interests: Interests = field(default_factory=Interests)
    recommendations: Recommendations = field(default_factory=Recommendations)
    meetings: Meetings = field(default_factory=Meetings)

    # Properties to use only in runtime
    best_match_prio_order_new: list[int] = field(default_factory=list)
    screen_stack: list[Screen] = field(default_factory=list)
    replace: dict[str, str] = field(default_factory=dict)
    notification_inbox: dict[int, int] = field(default_factory=dict)
    msg_bundle: MessageBundle = field(default_factory=MessageBundle)
    results: list[Any] = field(default_factory=list)
    selected_recommendation: Optional[Recommendation] = None
    selected_meeting: Optional[Meeting] = None
    selected_user: "User | None" = None
    search_filter: "User | None" = None
    change: Optional[Property] = None
    has_save_btn: bool = False
    add_reactions: bool = True
    feedback_message: str = ""
    call_channel_id: int = 0
    page: int = 0

    @property
    def stack_names(self) -> str:
        return " > ".join(str(screen.id) for screen in self.screen_stack)

    @staticmethod
    def search_profile() -> "User":
        return User(status=Status.ANY)

    @property
    def last_screen(self) -> Screen | None:
        if not self.screen_stack:
            return None
        return self.screen_stack[-1]

    @property
    def can_go_back(self) -> bool:
        return len(self.screen_stack) > 1

    def remove_last_screen(self) -> None:
        self.screen_stack.pop()

    def remove_screens_until_stop(self) -> None:
        """(Some screens have the `stop_screen` attribute set to `True`.
        They are kind of "fallback" screens, which should be shown
        when the user is done with the current flow.)
        - This method removes all screens from the stack until it finds
        a screen with the `stop_screen` attribute set to `True`."""
        for i in range(len(self.screen_stack) - 1, -1, -1):
            if self.screen_stack[i].stop_screen:
                break
            self.screen_stack.pop()

    def is_complete(self) -> bool:
        basic_filled = all(
            getattr(self, attr.to_str) not in ("?", "")
            for attr in VISIBLE_SIMPLE_USER_PROPS
        )
        return basic_filled and self.questions.is_complete()

    def is_selected_by(self, searcher: "User") -> bool:
        if searcher.search_filter is None:
            return False
        return (
            searcher.id != self.id
            and all(
                comma_and_search(
                    getattr(self, prop_id.to_str),
                    getattr(searcher.search_filter, prop_id.to_str),
                )
                for prop_id, prop in VISIBLE_SIMPLE_USER_PROPS.items()
                if prop["comma_separated"]
            )
            and all(
                getattr(searcher.search_filter, prop_id.to_str).lower()
                in getattr(self, prop_id.to_str).lower()
                or getattr(searcher.search_filter, prop_id.to_str) == "?"
                for prop_id, prop in VISIBLE_SIMPLE_USER_PROPS.items()
                if not prop["comma_separated"]
            )
            and self.status != Status.INVISIBLE
            and (
                searcher.search_filter.status == self.status
                or searcher.search_filter.status == Status.ANY
            )
            and all(  # TODO: ratyi!
                comma_and_search(
                    self.questions[q],
                    searcher.search_filter.questions[q],
                )
                for q in QUESTION_PROPS
            )
        )

    @staticmethod
    def dumps(user: "User") -> str:
        return json.dumps(
            {
                "id": user.id,
                "date_joined": str(user.date_joined),
                "questions": user.questions.to_dict(),
                "status": user.status.value,
                "best_match_prio_order": user.best_match_prio_order,
                "interests": user.interests.to_dict(),
                "meetings": user.meetings.to_dict(),
                "recommendations": user.recommendations.to_dict(),
                **{
                    attr.to_str: getattr(user, attr.to_str)
                    for attr in VISIBLE_SIMPLE_USER_PROPS
                },
            },
            indent=4,
        )

    @staticmethod
    def load_by_id(id_str: str) -> "User":
        filename = f"{USERS_PATH}/{id_str}.json"
        with open(filename, "r", encoding="utf-8") as file:
            raw_user: dict = json.loads(file.read())
            return User.load(raw_user)

    @staticmethod
    def load(user_data: dict[str, Any]) -> "User":
        if "headline" in user_data:
            user_data = User.migrate_headline(user_data)
        if "recommendations" not in user_data:
            user_data["recommendations"] = []
        return User(
            id=user_data["id"],
            date_joined=Date.from_str(user_data["date_joined"]),
            questions=Questions.from_dict(user_data["questions"]),
            status=Status(user_data["status"]),
            best_match_prio_order=user_data["best_match_prio_order"],
            interests=Interests.from_dict(user_data["interests"]),
            search_filter=User.search_profile(),
            meetings=Meetings.from_dict(user_data["meetings"]),
            recommendations=Recommendations.from_dict(user_data["recommendations"]),
            **{
                attr.to_str: user_data[attr.to_str]
                for attr in VISIBLE_SIMPLE_USER_PROPS
            },
        )

    @staticmethod
    def migrate_headline(input_data: dict[str, Any]) -> dict[str, Any]:
        data = input_data.copy()
        job = data["headline"]
        del data["headline"]
        data["job"] = job
        data["company"] = "?"
        return data

    @staticmethod
    def from_dc_user(dc_user: DcUser):
        return User(
            id=dc_user.id,
            name=dc_user.name,
            search_filter=User.search_profile(),
            best_match_prio_order=list(range(PRIO_LIST_LENGTH)),
        )

    def save(self) -> None:
        filename = f"{USERS_PATH}/{self.id}.json"
        with open(filename, "w", encoding="utf-8") as file:
            file.write(User.dumps(self))

    def valid_condition(self, condition: ScreenCond) -> bool:
        return {
            ScreenCond.PROFILE_COMPLETE: self.is_complete(),
            ScreenCond.VISIBLE: self.status != Status.INVISIBLE,
        }.get(condition, False)

    def screen_conditions_apply_for(self, screen: Screen) -> bool:
        if not screen.conditions:
            return True
        for condition in screen.conditions:
            if not self.valid_condition(condition):
                return False
        return True

    def save_priority_order(self):
        self.best_match_prio_order = self.best_match_prio_order_new
        self.save()

    def update_priority_order(self, new_order: list[int]):
        self.best_match_prio_order_new = new_order
        self.save()

    def format_priority_order(self, mode: str = "") -> str:
        """Returns the best match priority order of the user in a formatted way."""
        order = self.best_match_prio_order
        strike = ""
        if mode == "new":
            order = self.best_match_prio_order_new
        elif mode == "omitted":
            order = [i for i in range(PRIO_LIST_LENGTH) if i not in order]
            strike = "~~"
        return "\n".join(
            f"{k+1}. {strike}{DEFAULT_PRIO_ORDER[i]}{strike}"
            for k, i in enumerate(order)
        )

    def get_status(self, u: "User") -> Status:
        """Returns the status of the user."""
        return u.status

    def get_language_score(self, other: "User") -> int:
        """Returns 1 if the user and the other user have at least one matching language,
        0 otherwise."""
        return int(
            any(
                kw.strip() in other.languages.lower()
                for kw in self.languages.lower().split(",")
            )
        )

    def get_question_score(self, other: "User") -> int:
        """Returns the number of matching keywords in the questions of the user
        and the other user."""
        return self.questions.get_score(other.questions)

    def get_keywords_score(self, other: "User") -> int:
        """Returns the number of matching keywords in the keywords of the user
        and the other user."""
        return sum(
            kw.strip() in other.keywords.lower()
            for kw in self.keywords.lower().split(",")
        )

    def get_job_score(self, other: "User") -> int:
        """Returns the number of matching words in the job of the user
        and the other user."""
        return sum(
            kw in other.job.lower() for kw in NOT_ALPHANUMERIC.split(self.job.lower())
        )

    def get_company_score(self, other: "User") -> int:
        """Returns the number of matching words in the company of the user
        and the other user."""
        return sum(
            kw in other.company.lower()
            for kw in NOT_ALPHANUMERIC.split(self.company.lower())
        )

    def get_location_distance(self, other: "User") -> int:
        """Should return the distance between the location of the user and the other user.
        For now it just returns the number of matching words in the location of the user
        and the other user.
        """
        return sum(
            kw in other.location.lower()
            for kw in NOT_ALPHANUMERIC.split(self.location.lower())
        )

    def get_score_summary(self, other: "User") -> str:
        """Returns a summary of the scores of the user and the other user."""
        lang = self.get_language_score(other)
        q = self.get_question_score(other)
        kw = self.get_keywords_score(other)
        j = self.get_job_score(other)
        c = self.get_company_score(other)
        loc = self.get_location_distance(other)
        total = lang + q + kw + j + c + loc
        return (
            f"\n[SCORE: **{total}** = (Languages: {lang}) + (Questions: {q})"
            f" + (Keywords: {kw}) + (Job: {j}) + (Company: {c}) + (Location: {loc})]"
        )

    def get_search_status(self) -> str:
        return (
            "?"
            if self.status == Status.ANY
            else f"{STATUS_EMOJI[self.status]} " f"({self.status.value})"
        )

    def additional_info_with_side_effects(self) -> str:
        if not self.is_complete() and self.status != Status.INVISIBLE:
            self.status = Status.INVISIBLE
            return INCOMPLETE_PROFILE_WARNING
        elif self.is_complete() and self.status == Status.INVISIBLE:
            return COMPLETE_PROFILE_HINT
        return ""

    def paged_list_of(self, lst: list[T]) -> list[T]:
        return lst[self.page * PAGE_STEP : (self.page + 1) * PAGE_STEP]

    def paged_list_of_results(self) -> list[Any]:
        return self.paged_list_of(self.results)

    def get_page_reference(self) -> str:
        page_total = len(self.results)
        if page_total == 0:
            return "**(0 - 0) from total 0**"
        page_from = self.page * PAGE_STEP + 1
        page_to = min((self.page + 1) * PAGE_STEP, len(self.results))
        return f"**({page_from} - {page_to}) from total {page_total}**"

    def selected_meeting_time(self) -> str:
        if not self.selected_meeting:
            return "**No meeting selected.**"
        return str(self.selected_meeting.date)

    def send_interest_to_selected(self):
        assert self.selected_user is not None, "(Error #10) No selected user"
        self.send_interest_to(self.selected_user)
        self.selected_user.save()
        self.save()

    def send_interest_to(self, user: "User"):
        self.interests.send_to(user.id)
        user.interests.receive_from(self.id)

    def cancel_interest_to_selected(self):
        assert self.selected_user is not None, "(Error #11) No selected user"
        self.cancel_interest_to(self.selected_user)
        self.selected_user.save()
        self.save()

    def cancel_interest_to(self, user: "User"):
        self.interests.unsend_to(user.id)
        user.interests.unreceive_from(self.id)

    def request_meeting_with_selected(self, date: Date):
        assert self.selected_user is not None, "(Error #12) No selected user"
        self.meetings.request(self.selected_user.id, date)
        self.selected_user.meetings.request(self.id, date)
        self.selected_user.save()
        self.save()

    def cancel_meeting_with_selected(self):
        assert (
            self.selected_user and self.selected_meeting
        ), "(Error #13) No selected user or meeting"
        self.meetings.cancel(self.selected_user.id, self.selected_meeting)
        self.selected_user.meetings.cancel(self.id, self.selected_meeting)
        self.selected_user.save()
        self.save()

    async def start_video_call_with_selected(self, client: DcClient):
        """Assigns a Discord voice room to the user and the selected user
        to start a video call."""
        assert self.selected_user is not None, "(Error #14) No selected user"
        myself, partner, role, channel = self.get_members_role_and_channel(client)
        if not (myself and partner and role and channel):
            return
        await myself.add_roles(role)
        await partner.add_roles(role)
        self.call_channel_id = channel.id
        self.selected_user.call_channel_id = channel.id

    async def cancel_video_call_with_selected(self, client: DcClient):
        """Removes the Discord voice room assigned to the user and the selected user
        to cancel a video call."""
        assert self.selected_user is not None, "(Error #15) No selected user"
        myself, partner, role, _ = self.get_members_role_and_channel(client)
        if not (myself and partner and role):
            return
        await myself.remove_roles(role)
        await partner.remove_roles(role)
        self.call_channel_id = 0
        self.selected_user.call_channel_id = 0

    def cancel_selected_recommendation(self):
        assert self.selected_user is not None, "(Error #16) No selected user"
        assert self.selected_recommendation, "(Error #17)"
        self.remove_recommendation(self.selected_recommendation)
        self.selected_user.remove_recommendation(self.selected_recommendation)

    def remove_recommendation(self, recommendation: Recommendation):
        self.recommendations.remove(recommendation)
        self.save()

    def get_members_role_and_channel(self, client: DcClient):
        assert self.selected_user is not None, "(Error #18) No selected user"
        guild = get_guild(client)
        myself = guild.get_member(self.id)
        partner = guild.get_member(self.selected_user.id)
        if not CHANNELS:
            i = 1
            CHANNELS.append(i)
        elif len(CHANNELS) < 248:
            i = max(CHANNELS) + 1
            CHANNELS.append(i)
        else:
            self.call_channel_id = -1
            self.selected_user.call_channel_id = -1
            return None, None, None, None
        role = discord.utils.get(guild.roles, name=f"channel-{i}-role")
        channel = discord.utils.get(guild.voice_channels, name=f"channel-{i}")
        return myself, partner, role, channel

    @property
    def interests_sent_not_received(self) -> list[int]:
        return subtract(self.interests.sent, self.interests.received)

    @property
    def interests_received_not_sent(self) -> list[int]:
        return subtract(self.interests.received, self.interests.sent)

    @property
    def mutual_interests(self) -> list[int]:
        return intersect(self.interests.sent, self.interests.received)

    @property
    def recommendables(self) -> list[int]:
        return [
            user_id
            for user_id in self.mutual_interests
            if not (self.selected_user and user_id == self.selected_user.id)
        ]

    @property
    def interest_sent_to_selected(self) -> bool:
        if not self.selected_user:
            return False
        sent = self.selected_user.id in self.interests.sent
        received = self.id in self.selected_user.interests.received
        return sent and received

    @property
    def interest_received_from_selected(self) -> bool:
        if not self.selected_user:
            return False
        received = self.selected_user.id in self.interests.received
        sent = self.id in self.selected_user.interests.sent
        return received and sent

    @property
    def mutual_interests_with_selected(self) -> bool:
        return self.interest_sent_to_selected and self.interest_received_from_selected

    @property
    def recommendations_sent(self) -> list[Recommendation]:
        return self.recommendations.sent(self.id)

    @property
    def recommendations_received(self) -> list[Recommendation]:
        return self.recommendations.received(self.id)

    @property
    def started_call_with_selected(self) -> bool:
        if not self.selected_user:
            return False
        not_zero = self.call_channel_id > 0 and self.selected_user.call_channel_id > 0
        identical = self.call_channel_id == self.selected_user.call_channel_id
        return not_zero and identical

    @property
    def has_meetings_with_selected(self) -> bool:
        if not self.selected_user:
            return False
        return self.selected_user.id in [
            meeting.partner_id for meeting in self.meetings.all
        ]

    @property
    def selected_meeting_is_future(self) -> bool:
        mtg = self.selected_meeting
        return mtg is not None and mtg.is_future()

    @property
    def selected_meeting_is_past(self) -> bool:
        mtg = self.selected_meeting
        return mtg is not None and mtg.is_past()

    def get_interest_status(self) -> str:
        if self.mutual_interests_with_selected:
            return "✅ You have mutual interests with this user."
        if self.interest_sent_to_selected:
            return "⬆️ You have sent an interest to this user."
        if self.interest_received_from_selected:
            return "⬇️ This user has sent you an interest."
        return "No interest sent or received."

    def button_condition_applies(self, condition: ButtonCond) -> bool:
        interest_sent = self.interest_sent_to_selected
        interest_received = self.interest_received_from_selected
        mutual_interest = interest_sent and interest_received
        has_started_call = self.started_call_with_selected
        has_meetings = self.has_meetings_with_selected
        future_meeting = self.selected_meeting_is_future
        past_meeting = self.selected_meeting_is_past
        match condition:
            case ButtonCond.CAN_SEND_INTEREST:
                return not interest_sent and not interest_received
            case ButtonCond.CAN_CANCEL_INTEREST:
                return interest_sent
            case ButtonCond.CAN_CONFIRM_INTEREST:
                return interest_received and not interest_sent
            case ButtonCond.CAN_REQUEST_MEETING:
                return mutual_interest
            case ButtonCond.HAS_MEETINGS:
                return has_meetings
            case ButtonCond.CAN_CANCEL_MEETING | ButtonCond.CAN_CHANGE_MEETING_DATE:
                return has_meetings and future_meeting
            case ButtonCond.CAN_DELETE_MEETING:
                return has_meetings and past_meeting
            case ButtonCond.CAN_START_CALL:
                return mutual_interest and not has_started_call
            case ButtonCond.CAN_CANCEL_CALL:
                return mutual_interest and has_started_call
            case ButtonCond.HAS_PREVIOUS_PAGE:
                return self.page > 0
            case ButtonCond.HAS_NEXT_PAGE:
                return self.page < (len(self.results) - 1) // PAGE_STEP
            case ButtonCond.PRIO_ORDER_FULL:
                return len(self.best_match_prio_order_new) == PRIO_LIST_LENGTH
            case ButtonCond.CAN_SAVE:
                return len(self.best_match_prio_order_new) != 0
            case ButtonCond.SCREEN_NOT_OPENED_FROM_HOME:
                return len(self.screen_stack) > 2
        print(f"(Error #19) Invalid condition: {condition}")
        return False

    def replace_placeholders(self, text: str) -> str:
        sent = self.interests_sent_not_received
        received = self.interests_received_not_sent
        text = (
            text.replace("<id>", str(self.id))
            .replace("<date_joined>", str(self.date_joined))
            .replace("<status>", str(self.status))
            .replace("<number_of_results>", str(len(self.results)))
            .replace("<prio_order_new>", self.format_priority_order("new"))
            .replace("<prio_order>", self.format_priority_order())
            .replace("<prio_order_omitted>", self.format_priority_order("omitted"))
            .replace("<num_of_interests_sent>", str(len(sent)))
            .replace("<num_of_interests_received>", str(len(received)))
            .replace("<num_of_mutual_interests>", str(len(self.mutual_interests)))
            .replace("<interest_status>", self.get_interest_status())
            .replace("<num_of_future_meetings>", str(len(self.future_meetings)))
            .replace("<num_of_past_meetings>", str(len(self.past_meetings)))
            .replace("<page_reference>", self.get_page_reference())
            .replace("<selected_meeting_time>", self.selected_meeting_time())
            .replace("<video_call_link>", self.call_text())
            .replace("<next_year>", str(datetime.now().year + 1))
            .replace(
                "<user_to_recommend>",
                self.selected_user.name if self.selected_user else "",
            )
            .replace(
                "<num_of_recommendations_sent>",
                str(len(self.recommendations.sent(self.id))),
            )
            .replace(
                "<num_of_recommendations_received>",
                str(len(self.recommendations.received(self.id))),
            )
        )
        prefixes: dict[str, User | None] = {
            "": self,
            "selected_": self.selected_user,
        }
        if _filter := self.search_filter:
            prefixes["search_"] = _filter
            text = text.replace("<search_status>", _filter.get_search_status())
        for prefix, user in prefixes.items():
            if not user:
                continue
            for q in QUESTION_PROPS:
                subtext = user.questions[q]
                text = text.replace(f"<{prefix}{q}_peek>", peek(subtext))
                text = text.replace(f"<{prefix}{q}>", subtext)
            for prop in VISIBLE_SIMPLE_USER_PROPS:
                subtext = getattr(user, prop.to_str)
                text = text.replace(f"<{prefix}{prop}_peek>", peek(subtext))
                text = text.replace(f"<{prefix}{prop}>", subtext)
        if self.replace:
            for key, value in self.replace.items():
                text = text.replace(key, value)
        return text

    def call_text(self) -> str:
        call = "\n\n☎️ Call:\n"
        if self.call_channel_id == 0:
            return f"{call}***No call has been started.***"
        if self.call_channel_id == -1:
            return f"{call}All channels are ***occupied...*** Please try again later."
        return (
            f"{call}***Click here to join:*** "
            f"https://discord.com/channels/{GUILD_ID}/{self.call_channel_id}"
        )

    def btn_conditions_apply_for(self, button: Button):
        for condition in button.conditions:
            if not self.button_condition_applies(condition):
                return False
        return True

    def stack(self, screen: Screen) -> None:
        if screen.id == ScreenId.HOME:
            self.screen_stack = [screen]
        elif screen in self.screen_stack:
            screen_index = self.screen_stack.index(screen)
            self.screen_stack = self.screen_stack[: screen_index + 1]
        elif not (self.screen_stack and self.screen_stack[-1].id == screen.id):
            self.screen_stack.append(screen)

    async def add_selection_reactions(self) -> None:
        for i in range(min(PAGE_STEP, len(self.results) - self.page * PAGE_STEP)):
            await self.msg_bundle.add_reaction(NUM_EMOJI[i])

    def page_prefix(self, i: int) -> str:
        if i < PAGE_STEP:
            return "   "
        num = (i + self.page * PAGE_STEP) // PAGE_STEP
        return f"**{num}** "

    def get_result_by_number(self, num: int) -> Any:
        return self.results[self.page * PAGE_STEP + num - 1]

    def get_item_by_number(self, lst: list, num: int) -> Any:
        return lst[self.page * PAGE_STEP + num - 1]

    def set_question(self, question: Property, new_value: str):
        self.questions[question] = new_value

    async def send_message(
        self,
        receiver_future: Optional[ReceiverFuture] = None,
        receiver: Optional[Receiver] = None,
    ) -> None:
        if receiver and receiver_future:
            receiver_future.close()
        elif receiver_future:
            receiver = await receiver_future
        assert receiver, "(Error #20) receiver is None"

        await self.msg_bundle.send_to(receiver)

    @property
    def dc_message(self) -> DcMessage | None:
        return self.msg_bundle.body.dc_message

    def can_delete(self, msg_id: int) -> bool:
        spacer_msg = self.msg_bundle.spacer.dc_message
        body_msg = self.msg_bundle.body.dc_message
        if not (spacer_msg and body_msg):
            return True
        return msg_id not in [spacer_msg.id, body_msg.id]

    async def delete_message(self, spacer_too: bool = False) -> None:
        await self.msg_bundle.delete(spacer_too)

    def add_button_to_message(self, button: DcButton) -> None:
        self.msg_bundle.add_button(button)

    def remove_button_from_message(self, button: DcButton) -> None:
        self.msg_bundle.remove_button(button)

    def update_message(
        self,
        message_text: str,
        dc_view: Optional[DcView] = None,
        dc_message: Optional[DcMessage] = None,
    ) -> None:
        self.msg_bundle.update_body(message_text, dc_view, dc_message)

    def add_notification(
        self, msg_text: str, dc_view: Optional[DcView] = None
    ) -> Message:
        message = Message(msg_text=msg_text, dc_view=dc_view)
        self.msg_bundle.add_notification(message)
        return message

    async def remove_notification(self, msg_id: int):
        await self.msg_bundle.remove_notification(msg_id)

    async def add_reaction_to_message(self, reaction: DcEmoji | str) -> None:
        await self.msg_bundle.add_reaction(reaction)

    @property
    def future_meetings(self) -> list[Meeting]:
        return self.meetings.future

    @property
    def past_meetings(self) -> list[Meeting]:
        return self.meetings.past

    @property
    def sleeping(self) -> bool:
        return self.msg_bundle.sleeping

    def set_new_question_val(
        self, q_to_change: Property, new_val: str, searching: bool
    ) -> None:
        change_user = self
        if searching:
            assert self.search_filter, "(Error #21) No search filter found!"
            change_user = self.search_filter
        change_user.set_question(q_to_change, new_val)
