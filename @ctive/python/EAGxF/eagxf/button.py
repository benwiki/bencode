from discord.ui import Button as DCButton


class Button(DCButton):
    def __init__(
        self,
        *args,
        takes_to: str = "",
        condition: str = "",
        **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.takes_to = takes_to
        self.condition = condition
