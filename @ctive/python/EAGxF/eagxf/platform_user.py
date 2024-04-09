from dataclasses import dataclass, field

import discord

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
    title: str = "?"  # max 100 chars
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
            getattr(self, attr) not in ["?", ""]
            for attr in ["name", "title", "location", "languages", "keywords"]
        )
        questions_filled = all(
            self.questions[question] not in ["?", ""]
            for question in ["need_help", "can_help"]
        )
        return basic_filled and questions_filled

    def incomplete_msg(self) -> str:
        return (
            "*Your profile must be complete before you can "
            "change your status ;-)*"
            "\n*Fill out all details and try again!*"
        )

    def search_applicable_for(self, other: "PlatformUser") -> bool:
        if other.search_filter is None:
            return False
        return (
            (
                other.search_filter.name.lower() in self.name.lower()
                or other.search_filter.name == "?"
            )
            and (
                other.search_filter.title.lower() in self.title.lower()
                or other.search_filter.title == "?"
            )
            and (
                other.search_filter.location.lower() in self.location.lower()
                or other.search_filter.location == "?"
            )
            and comma_and_search(self.languages, other.search_filter.languages)
            and comma_and_search(self.keywords, other.search_filter.keywords)
            and (
                self.status != Status.INVISIBLE
                and (
                    other.search_filter.status == self.status
                    or other.search_filter.status == Status.ANY
                )
            )
            and comma_and_search(
                self.questions["need_help"],
                other.search_filter.questions["need_help"],
            )
            and comma_and_search(
                self.questions["can_help"],
                other.search_filter.questions["can_help"],
            )
        )
