from dataclasses import dataclass, field

import discord

from eagxf.date import Date
from eagxf.status import Status
from eagxf.structure import Structure


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

    # Properties to use only in runtime
    last_msg: discord.Message | None = None
    last_view: discord.ui.View | None = None
    last_structure: Structure | None = None
    back_to_structure: Structure | None = None
    search_filter: "PlatformUser | None" = None
    found_users: list[int] = field(default_factory=list)
    best_matches: list[int] = field(default_factory=list)
    matches_from: int = 1
    matches_to: int = 10
    best_match_prio_order_new: list[int] = field(default_factory=list)
    editing_prio_order: bool = False
    save_btn: discord.ui.Button | None = None
    change: str = ""
