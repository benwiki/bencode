import json
from dataclasses import dataclass, field
from typing import Any, Callable

from eagxf.button import Button
from eagxf.constants import (
    DEFAULT_PRIO_ORDER,
    NOT_ALNUM,
    PAGE_STEP,
    PRIO_LIST_LENGTH,
    QUESTION_NAMES,
    STATUS_EMOJI,
    USERS_PATH,
    VISIBLE_SIMPLE_USER_PROPS,
)
from eagxf.date import Date
from eagxf.interests import Interests
from eagxf.meetings import Meetings
from eagxf.questions import Questions
from eagxf.status import Status
from eagxf.structure import Structure
from eagxf.typedefs import DcUser
from eagxf.util import comma_and_search, intersect, subtract
from eagxf.view_msg import ViewMsg


@dataclass
class User:
    # Properties to save
    id: int = 0
    date_joined: Date = field(default_factory=Date.current)
    name: str = "?"  # max 50 chars
    headline: str = "?"  # max 100 chars
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
    view_msg: ViewMsg = field(default_factory=ViewMsg)
    results: list[int] = field(default_factory=list)
    selected_user: "User | None" = None
    search_filter: "User | None" = None
    structure_stack: list[Structure] = field(default_factory=list)
    has_save_btn: bool = False
    add_reactions: bool = True
    change: str = ""
    page: int = 0

    @staticmethod
    def search_profile() -> "User":
        return User(status=Status.ANY)

    @property
    def back_to_structure(self) -> Structure | None:
        if len(self.structure_stack) < 2:
            return None
        self.structure_stack.pop()
        return self.structure_stack[-1]

    def is_complete(self) -> bool:
        basic_filled = all(
            getattr(self, attr) not in ("?", "") for attr in VISIBLE_SIMPLE_USER_PROPS
        )
        return basic_filled and self.questions.is_complete()

    def is_selected_by(self, searcher: "User") -> bool:
        if searcher.search_filter is None:
            return False
        return (
            searcher.id != self.id
            and all(
                comma_and_search(
                    getattr(self, prop_id), getattr(searcher.search_filter, prop_id)
                )
                for prop_id, prop in VISIBLE_SIMPLE_USER_PROPS.items()
                if prop["comma_separated"]
            )
            and all(
                getattr(searcher.search_filter, prop_id).lower()
                in getattr(self, prop_id).lower()
                or getattr(searcher.search_filter, prop_id) == "?"
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
                    self.questions.to_dict()[q_id],
                    searcher.search_filter.questions.to_dict()[q_id],
                )
                for q_id in QUESTION_NAMES
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
                **{attr: getattr(user, attr) for attr in VISIBLE_SIMPLE_USER_PROPS},
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
            **{attr: user_data[attr] for attr in VISIBLE_SIMPLE_USER_PROPS},
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

    def valid_condition(self, condition: str) -> bool:
        if condition == "profile_complete":
            return self.is_complete()
        return False

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

    def get_headline_score(self, other: "User") -> int:
        """Returns the number of matching words in the headline of the user
        and the other user."""
        return sum(
            NOT_ALNUM.sub("", kw.strip().lower()) in other.headline.lower()
            for kw in self.headline.split(" ")
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
        return (
            f"\n[SCORE: "
            f"(Lang: {self.get_language_score(other)}) "
            f"(Q: {self.get_question_score(other)}) "
            f"(Kw: {self.get_keywords_score(other)}) "
            f"(H.line: {self.get_headline_score(other)}) "
            f"(Loc: {self.get_location_distance(other)}) "
            "]"
        )

    def get_search_status(self) -> str:
        return (
            "?"
            if self.status == Status.ANY
            else f"{STATUS_EMOJI[self.status]} " f"({self.status.value})"
        )

    def send_interest_to_selected(self):
        self.manage_interest(list.append)

    def cancel_interest_to_selected(self):
        self.manage_interest(list.remove)

    def manage_interest(self, action: Callable[[list, Any], None]):
        assert self.selected_user is not None
        action(self.interests.sent, self.selected_user.id)
        action(self.selected_user.interests.received, self.id)
        self.selected_user.save()
        self.save()

    def cancel_meeting_with_selected(self):
        assert self.selected_user is not None
        self.meetings.upcoming = [
            meeting
            for meeting in self.meetings.upcoming
            if meeting.partner_id != self.selected_user.id
        ]
        self.selected_user.meetings.upcoming = [
            meeting
            for meeting in self.selected_user.meetings.upcoming
            if meeting.partner_id != self.id
        ]
        self.selected_user.save()
        self.save()

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
    def has_meeting_with_selected(self) -> bool:
        if not self.selected_user:
            return False
        return self.selected_user.id in map(
            lambda meeting: meeting.partner_id, self.meetings.upcoming
        )

    def get_interest_status(self) -> str:
        if self.mutual_interests_with_selected:
            return "✅ You have mutual interests with this user."
        if self.interest_sent_to_selected:
            return "⬆️ You have sent an interest to this user."
        if self.interest_received_from_selected:
            return "⬇️ This user has sent you an interest."
        return "No interest sent or received..."

    async def apply_effect(self, effect: str) -> None:
        match effect:
            case "go_to_previous_page":
                self.page -= 1
            case "go_to_next_page":
                self.page += 1
            case "delete_message":
                await self.view_msg.delete()
            case "save_best_matches":
                self.save_priority_order()
            case "reset_new_prio_order":
                self.best_match_prio_order_new = []
            case "default_best_matches":
                self.update_priority_order(list(range(PRIO_LIST_LENGTH)))
            case "reset_user_property_change":
                self.change = ""
            case "empty_results":
                self.results = []
                self.page = 0
            case "send_interest":
                self.send_interest_to_selected()
            case "cancel_interest":
                self.cancel_interest_to_selected()
            case "cancel_meeting":
                self.cancel_meeting_with_selected()

    def button_condition_applies(self, condition: str) -> bool:
        if not condition:
            return True
        if condition == "has_previous_page":
            return self.page > 0
        if condition == "has_next_page":
            return self.page < (len(self.results) - 1) // PAGE_STEP
        if condition == "prio_order_full":
            return len(self.best_match_prio_order_new) == PRIO_LIST_LENGTH
        if condition.startswith("can_"):
            interest_sent = self.interest_sent_to_selected
            interest_received = self.interest_received_from_selected
            has_meeting = self.has_meeting_with_selected
            if condition == "can_send_interest":
                return not interest_sent and not interest_received
            if condition == "can_cancel_interest":
                return interest_sent
            if condition == "can_confirm_interest":
                return interest_received and not interest_sent
            if condition == "can_request_meeting":
                return interest_sent and interest_received and not has_meeting
            if condition == "can_cancel_meeting":
                return interest_sent and interest_received and has_meeting
        print(f"Invalid condition: {condition}")
        return False

    def replace_placeholders(self, text: str) -> str:
        sent = self.interests_sent_not_received
        received = self.interests_received_not_sent
        return (
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
            .replace("<num_of_upcoming_meetings>", str(len(self.meetings.upcoming)))
            .replace("<num_of_past_meetings>", str(len(self.meetings.past)))
        )

    def conditions_apply_for(self, button: Button):
        for condition in button.conditions.split(","):
            if not self.button_condition_applies(condition):
                return False
        return True
