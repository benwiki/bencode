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
    results: list[int] = field(default_factory=list)
    page: int = 0
    best_match_prio_order_new: list[int] = field(default_factory=list)
    show_save_btn: bool = field(default_factory=bool)
    change: str = ""
