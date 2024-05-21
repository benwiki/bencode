from typing import Iterable

from discord.ui import Button as DCButton

from eagxf.constants import QUESTION_NAMES, VISIBLE_SIMPLE_USER_PROPS


class Button(DCButton):
    takes_to: str
    effects: str
    conditions: str

    def __init__(
        self,
        *args,
        takes_to: str = "",
        effects: str = "",
        conditions: str = "",
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.takes_to = takes_to
        self.effects = effects
        self.conditions = conditions

    @staticmethod
    def get_navigation_buttons(structure_name: str) -> list["Button"]:
        return [
            Button(
                label="◀️ Previous",
                takes_to=structure_name,
                conditions="has_previous_page",
                effects="go_to_previous_page",
                row=0,
            ),
            Button(
                label="Next ▶️",
                takes_to=structure_name,
                conditions="has_next_page",
                effects="go_to_next_page",
                row=0,
            ),
        ]

    @staticmethod
    def simple_prop_buttons(action, before_questions=True) -> Iterable["Button"]:
        """Returns a list of buttons for [simple properties]"""
        return (
            Button(
                label=prop["label"],
                emoji=prop["emoji"],
                takes_to=f"{action}_{prop_id}",
                row=prop["row"],
            )
            for prop_id, prop in VISIBLE_SIMPLE_USER_PROPS.items()
            if before_questions == prop["before_questions"]
        )

    @staticmethod
    def question_buttons(action) -> Iterable["Button"]:
        """Returns a list of buttons for [questions]"""
        return (
            Button(
                label=question["label"],
                emoji=question["emoji"],
                takes_to=f"{action}_{q_id}",
            )
            for q_id, question in QUESTION_NAMES.items()
        )
