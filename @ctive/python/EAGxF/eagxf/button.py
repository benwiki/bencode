from discord.ui import Button as DCButton


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
        **kwargs
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
