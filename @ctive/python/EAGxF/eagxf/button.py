from discord.ui import Button as DCButton


class Button(DCButton):
    takes_to: str
    effects: str
    condition: str

    def __init__(
        self, *args, takes_to: str = "", effect: str = "", condition: str = "", **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.takes_to = takes_to
        self.effects = effect
        self.condition = condition
