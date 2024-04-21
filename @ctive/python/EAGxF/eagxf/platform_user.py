from dataclasses import dataclass, field

import discord

from eagxf.constants import QUESTION_NAMES, VISIBLE_SIMPLE_USER_PROPS
from eagxf.date import Date
from eagxf.status import Status
from eagxf.structure import Structure
from eagxf.util import comma_and_search


@dataclass
class PlatformUser:

    # Properties to save
    id: int = 0
    date_joined: Date = field(default_factory=lambda: Date(1, 1, 2000))
    name: str = "?"  # max 50 chars
    headline: str = "?"  # max 100 chars
    location: str = "?"
    languages: str = "?"  # comma separated
    questions: dict[str, str] = field(default_factory=dict)
    keywords: str = "?"  # comma separated
    status: Status = Status.INVISIBLE
    best_match_prio_order: list[int] = field(default_factory=list)
    interests: dict[str, list[int]] = field(default_factory=dict)

    # Properties to use only in runtime
    best_match_prio_order_new: list[int] = field(default_factory=list)
    results: list[int] = field(default_factory=list)
    selected_user: "PlatformUser | None" = None
    search_filter: "PlatformUser | None" = None
    back_to_structure: Structure | None = None
    last_view: discord.ui.View | None = None
    last_msg: discord.Message | None = None
    last_structure: Structure | None = None
    added_save_btn: bool = False
    change: str = ""
    page: int = 0

    def is_complete(self) -> bool:
        basic_filled = all(
            getattr(self, attr) not in ["?", ""] for attr in VISIBLE_SIMPLE_USER_PROPS
        )
        questions_filled = all(
            self.questions[question] not in ["?", ""] for question in QUESTION_NAMES
        )
        return basic_filled and questions_filled

    def incomplete_msg(self) -> str:
        return (
            "*Your profile must be complete before you can "
            "change your status ;-)*"
            "\n*Fill out all details and try again!*"
        )

    def is_selected_by(self, searcher: "PlatformUser") -> bool:
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
            and all(
                comma_and_search(
                    self.questions[q_id],
                    searcher.search_filter.questions[q_id],
                )
                for q_id in QUESTION_NAMES
            )
        )
