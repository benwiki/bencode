from discord.ui import Button as DCButton


class Button(DCButton):
    takes_to: str = ""

    def __init__(
        self,
        *args,
        takes_to: str = "",
        **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.takes_to = takes_to