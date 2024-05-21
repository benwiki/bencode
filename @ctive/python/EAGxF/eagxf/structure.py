from dataclasses import dataclass, field

from eagxf.button import Button


@dataclass
class Structure:
    id: str = field(default_factory=str)
    message: str = field(default_factory=str)
    buttons: list[Button] = field(default_factory=list)
    reactions: list[str] = field(default_factory=list)
    changed_property: str | None = None
    condition: str = ""
    # these effects will run AFTER the button's own effects
    after_button_effects: str = ""
    paged: bool = field(default_factory=bool)
    stacked: bool = field(default_factory=lambda: True)
