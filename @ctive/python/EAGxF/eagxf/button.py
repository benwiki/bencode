from typing import Iterable

import discord
from discord.ui import Button as DCButton

from eagxf.constants import QUESTION_NAMES, VISIBLE_SIMPLE_USER_PROPS
from eagxf.enums.button_condition import ButtonCond
from eagxf.enums.effect import Effect
from eagxf.enums.screen_id import ScreenId


class Button(DCButton):
    takes_to: ScreenId
    effects: list[Effect]
    conditions: list[ButtonCond]

    def __init__(
        self,
        *args,
        takes_to: ScreenId = ScreenId.HOME,
        effects: list[Effect] | None = None,
        conditions: list[ButtonCond] | None = None,
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.takes_to = takes_to
        self.effects = effects or []
        self.conditions = conditions or []

    @staticmethod
    def get_navigation_buttons(screen_id: ScreenId) -> list["Button"]:
        return [
            Button(
                label="◀️ Previous",
                takes_to=screen_id,
                conditions=[ButtonCond.HAS_PREVIOUS_PAGE],
                effects=[Effect.GO_TO_PREVIOUS_PAGE],
                row=0,
            ),
            Button(
                label="Next ▶️",
                takes_to=screen_id,
                conditions=[ButtonCond.HAS_NEXT_PAGE],
                effects=[Effect.GO_TO_NEXT_PAGE],
                row=0,
            ),
        ]

    @staticmethod
    def simple_prop_buttons(action: str, before_questions=True) -> Iterable["Button"]:
        """Returns a list of buttons for [simple properties]"""
        return (
            Button(
                label=prop["label"],
                emoji=prop["emoji"],
                takes_to=ScreenId.action(action, prop_id.to_str),
                # row=prop["row"],
            )
            for prop_id, prop in VISIBLE_SIMPLE_USER_PROPS.items()
            if before_questions == prop["before_questions"]
        )

    @staticmethod
    def question_buttons(action: str, row=None) -> Iterable["Button"]:
        """Returns a list of buttons for [questions]"""
        return (
            Button(
                label=question["label"],
                emoji=question["emoji"],
                takes_to=ScreenId.action(action, q_id.to_str),
                row=row,
            )
            for q_id, question in QUESTION_NAMES.items()
        )

    @staticmethod
    def back(row=None):
        return Button(label="⬅️ Back", takes_to=ScreenId.BACK__, row=row)

    @staticmethod
    def ok(row=None):
        return Button(
            label="OK",
            style=discord.ButtonStyle.green,
            takes_to=ScreenId.BACK__,
            row=row,
        )

    @staticmethod
    def home(row=None):
        return Button(
            label="🏠 Home",
            style=discord.ButtonStyle.primary,
            takes_to=ScreenId.HOME,
            row=row,
        )

    @staticmethod
    def back_home(row=None):
        return [Button.back(row=row), Button.home(row=row)]

    @staticmethod
    def ok_home(row=None):
        return [Button.ok(row=row), Button.home(row=row)]
