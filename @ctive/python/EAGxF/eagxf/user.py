import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

import discord

from eagxf.button import Button
from eagxf.constants import (
    DEFAULT_PRIO_ORDER,
    INCOMPLETE_PROFILE_WARNING,
    NOT_ALNUM,
    NUM_EMOJI,
    PAGE_STEP,
    PRIO_LIST_LENGTH,
    QUESTION_NAMES,
    STATUS_EMOJI,
    VISIBLE_SIMPLE_USER_PROPS,
)
from eagxf.date import Date
from eagxf.enums.condition import ButtonCond
from eagxf.enums.effect import Effect
from eagxf.enums.property import Property
from eagxf.enums.structure_condition import ScreenCond
from eagxf.interests import Interests
from eagxf.meetings import Meeting, Meetings
from eagxf.questions import Questions
from eagxf.status import Status
from eagxf.structure import Screen
from eagxf.typedefs import DcClient, DcUser
from eagxf.util import (
    CHANNELS,
    GUILD_ID,
    comma_and_search,
    get_guild,
    intersect,
    peek,
    subtract,
)
from eagxf.view_msg import ViewMsg
from main import USERS_PATH


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
    meetings: Meetings = field(default_factory=Meetings)

    # Properties to use only in runtime
    best_match_prio_order_new: list[int] = field(default_factory=list)
    screen_stack: list[Screen] = field(default_factory=list)
    view_msg: ViewMsg = field(default_factory=ViewMsg)
    results: list[int] = field(default_factory=list)
    selected_meeting: Meeting | None = None
    selected_user: "User | None" = None
    search_filter: "User | None" = None
    change: Property | None = None
    has_save_btn: bool = False
    add_reactions: bool = True
    feedback_message: str = ""
    call_channel_id: int = 0
    page: int = 0

    @staticmethod
    def search_profile() -> "User":
        return User(status=Status.ANY)

    @property
    def last_screen(self) -> Screen | None:
        if not self.screen_stack:
            return None
        return self.screen_stack[-1]

    @property
    def back_to_screen(self) -> Screen | None:
        if len(self.screen_stack) < 2:
            return None
        self.screen_stack.pop()
        return self.screen_stack[-1]

    def is_complete(self) -> bool:
        basic_filled = all(
            getattr(self, attr.low) not in ("?", "")
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
                    getattr(self, prop_id.low),
                    getattr(searcher.search_filter, prop_id.low),
                )
                for prop_id, prop in VISIBLE_SIMPLE_USER_PROPS.items()
                if prop["comma_separated"]
            )
            and all(
                getattr(searcher.search_filter, prop_id.low).lower()
                in getattr(self, prop_id.low).lower()
                or getattr(searcher.search_filter, prop_id.low) == "?"
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
                    self.questions.to_dict()[q.low],
                    searcher.search_filter.questions.to_dict()[q.low],
                )
                for q in QUESTION_NAMES
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
                **{
                    attr.low: getattr(user, attr.low)
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
        return User(
            id=user_data["id"],
            date_joined=Date.from_str(user_data["date_joined"]),
            questions=Questions.from_dict(user_data["questions"]),
            status=Status(user_data["status"]),
            best_match_prio_order=user_data["best_match_prio_order"],
            interests=Interests.from_dict(user_data["interests"]),
            search_filter=User.search_profile(),
            meetings=Meetings.from_dict(user_data["meetings"]),
            **{attr.low: user_data[attr.low] for attr in VISIBLE_SIMPLE_USER_PROPS},
        )

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

    def format_priority_order(self, new: bool = False) -> str:
        """Returns the best match priority order of the user in a formatted way."""
        order = self.best_match_prio_order_new if new else self.best_match_prio_order
        things = range(2, PRIO_LIST_LENGTH + 1)
        return ("1. " if order else "") + "\n{}. ".join(
            DEFAULT_PRIO_ORDER[i] for i in order
        ).format(*things)

    def get_status(self, u: "User") -> Status:
        """Returns the status of the user."""
        return u.status

    def get_language_score(self, other: "User") -> int:
        """Returns 1 if the user and the other user have at least one matching language,
        0 otherwise."""
        return int(
            any(
                kw.strip().lower() in other.languages.lower()
                for kw in self.languages.split(",")
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
            kw.strip().lower() in other.keywords.lower()
            for kw in self.keywords.split(",")
        )

    def get_job_score(self, other: "User") -> int:
        """Returns the number of matching words in the job of the user
        and the other user."""
        return sum(
            NOT_ALNUM.sub("", kw.strip().lower()) in other.job.lower()
            for kw in self.job.split(" ")
        )

    def get_company_score(self, other: "User") -> int:
        """Returns the number of matching words in the company of the user
        and the other user."""
        return sum(
            NOT_ALNUM.sub("", kw.strip().lower()) in other.company.lower()
            for kw in self.company.split(" ")
        )

    def get_location_distance(self, other: "User") -> int:
        """Should return the distance between the location of the user and the other user.
        For now it just returns the number of matching words in the location of the user
        and the other user.
        """
        return sum(
            NOT_ALNUM.sub("", kw.strip().lower()) in other.location.lower()
            for kw in self.location.split(" ")
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
        return ""

    def paged_list_of(self, lst: list) -> list[int]:
        return lst[self.page * PAGE_STEP : (self.page + 1) * PAGE_STEP]

    def paged_list_of_results(self) -> list[int]:
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
        assert self.selected_user is not None
        self.send_interest_to(self.selected_user)
        self.selected_user.save()
        self.save()

    def send_interest_to(self, user: "User"):
        self.interests.send_to(user.id)
        user.interests.receive_from(self.id)

    def cancel_interest_to_selected(self):
        assert self.selected_user is not None
        self.cancel_interest_to(self.selected_user)
        self.selected_user.save()
        self.save()

    def cancel_interest_to(self, user: "User"):
        self.interests.unsend_to(user.id)
        user.interests.unreceive_from(self.id)

    def request_meeting_with_selected(self, date: Date):
        assert self.selected_user is not None
        self.meetings.request(self.selected_user.id, date)
        self.selected_user.meetings.request(self.id, date)
        self.selected_user.save()
        self.save()

    def cancel_meeting_with_selected(self):
        assert self.selected_user and self.selected_meeting
        self.meetings.cancel(self.selected_user.id, self.selected_meeting)
        self.selected_user.meetings.cancel(self.id, self.selected_meeting)
        self.selected_user.save()
        self.save()

    async def start_video_call_with_selected(self, client: DcClient):
        """Assigns a Discord voice room to the user and the selected user
        to start a video call."""
        assert self.selected_user is not None
        me, partner, role, channel = self.get_members_role_and_channel(client)
        if not (me and partner and role and channel):
            return
        await me.add_roles(role)
        await partner.add_roles(role)
        self.call_channel_id = channel.id
        self.selected_user.call_channel_id = channel.id

    async def cancel_video_call_with_selected(self, client: DcClient):
        """Removes the Discord voice room assigned to the user and the selected user
        to cancel a video call."""
        assert self.selected_user is not None
        me, partner, role, _ = self.get_members_role_and_channel(client)
        if not (me and partner and role):
            return
        await me.remove_roles(role)
        await partner.remove_roles(role)
        self.call_channel_id = 0
        self.selected_user.call_channel_id = 0

    def get_members_role_and_channel(self, client: DcClient):
        assert self.selected_user is not None
        guild = get_guild(client)
        me = guild.get_member(self.id)
        partner = guild.get_member(self.selected_user.id)
        if not CHANNELS:
            i = 1
        elif len(CHANNELS) < 248:
            i = max(CHANNELS) + 1
            CHANNELS.append(i)
        else:
            self.call_channel_id = -1
            self.selected_user.call_channel_id = -1
            return None, None, None, None
        role = discord.utils.get(guild.roles, name=f"channel-{i}-role")
        channel = discord.utils.get(guild.voice_channels, name=f"channel-{i}")
        return me, partner, role, channel

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

    async def apply_effect(self, effect: Effect, client: DcClient) -> None:
        match effect:
            case Effect.GO_TO_PREVIOUS_PAGE:
                self.page -= 1
            case Effect.GO_TO_NEXT_PAGE:
                self.page += 1
            case Effect.DELETE_MESSAGE:
                await self.view_msg.delete()
            case Effect.SAVE_BEST_MATCHES:
                self.save_priority_order()
            case Effect.RESET_NEW_PRIO_ORDER:
                self.best_match_prio_order_new = []
            case Effect.DEFAULT_BEST_MATCHES:
                self.update_priority_order(list(range(PRIO_LIST_LENGTH)))
            case Effect.RESET_USER_PROPERTY_CHANGE:
                self.change = None
            case Effect.EMPTY_RESULTS:
                self.results = []
                self.page = 0
            case Effect.SEND_INTEREST:
                self.send_interest_to_selected()
            case Effect.CANCEL_INTEREST:
                self.cancel_interest_to_selected()
            case Effect.CANCEL_MEETING:
                self.cancel_meeting_with_selected()
            case Effect.START_CALL:
                await self.start_video_call_with_selected(client)
            case Effect.CANCEL_CALL:
                await self.cancel_video_call_with_selected(client)

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
        print(f"Invalid condition: {condition}")
        return False

    def replace_placeholders(self, text: str) -> str:
        sent = self.interests_sent_not_received
        received = self.interests_received_not_sent
        text = (
            text.replace("<id>", str(self.id))
            .replace("<date_joined>", str(self.date_joined))
            .replace("<status>", str(self.status))
            .replace("<number_of_results>", str(len(self.results)))
            .replace("<prio_order_new>", self.format_priority_order(new=True))
            .replace("<prio_order>", self.format_priority_order())
            .replace("<num_of_interests_sent>", str(len(sent)))
            .replace("<num_of_interests_received>", str(len(received)))
            .replace("<num_of_mutual_interests>", str(len(self.mutual_interests)))
            .replace("<interest_status>", self.get_interest_status())
            .replace("<num_of_future_meetings>", str(len(self.meetings.future)))
            .replace("<num_of_past_meetings>", str(len(self.meetings.past)))
            .replace("<page_reference>", self.get_page_reference())
            .replace("<selected_meeting_time>", self.selected_meeting_time())
            .replace("<video_call_link>", self.call_text())
            .replace("<next_year>", str(datetime.now().year + 1))
        )
        prefixes: dict[str, User] = {"": self}
        if _filter := self.search_filter:
            prefixes["search_"] = _filter
            text = text.replace("<search_status>", _filter.get_search_status())
        for prefix, user in prefixes.items():
            for q in QUESTION_NAMES:
                subtext = user.questions[q.low]
                text = text.replace(f"<{prefix}{q}>_peek", peek(subtext))
                text = text.replace(f"<{prefix}{q}>", subtext)
            for prop in VISIBLE_SIMPLE_USER_PROPS:
                subtext = getattr(user, prop.low)
                text = text.replace(f"<{prefix}{prop}>_peek", peek(subtext))
                text = text.replace(f"<{prefix}{prop}>", subtext)
        return text

    def call_text(self) -> str:
        if self.call_channel_id == 0:
            return "\n\n☎️ **Call:**  No call has been started."
        if self.call_channel_id == -1:
            return "\n\n☎️ **Call:**  All channels are ***occupied...*** Please try again later."
        return (
            "\n\n☎️ **Call:**  Click here to join: "
            f"https://discord.com/channels/{GUILD_ID}/{self.call_channel_id}"
        )

    def btn_conditions_apply_for(self, button: Button):
        for condition in button.conditions:
            if not self.button_condition_applies(condition):
                return False
        return True

    def stack(self, screen: Screen) -> None:
        if screen.id == "home":
            self.screen_stack = [screen]
        elif screen.id in self.screen_stack:
            screen_index = self.screen_stack.index(screen)
            self.screen_stack = self.screen_stack[: screen_index + 1]
        elif not (self.screen_stack and self.screen_stack[-1].id == screen.id):
            self.screen_stack.append(screen)

    async def add_special_reactions(self) -> None:
        for i in range(min(PAGE_STEP, len(self.results) - self.page * PAGE_STEP)):
            await self.view_msg.add_reaction(NUM_EMOJI[i])

    def page_prefix(self, i: int) -> str:
        i = i + self.page * PAGE_STEP
        return f"**{i // PAGE_STEP}** " if i >= PAGE_STEP else "   "

    def get_result_by_number(self, num: int) -> Any:
        return self.results[self.page * PAGE_STEP + num - 1]

    def get_item_by_number(self, lst: list, num: int) -> Any:
        return lst[self.page * PAGE_STEP + num - 1]
