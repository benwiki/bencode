from dataclasses import dataclass, field

from eagxf.button import Button


@dataclass
class Structure:
    id: str = field(default_factory=str)
    message: str = field(default_factory=str)
    buttons: list[Button] = field(default_factory=list)
    reactions: list[str] = field(default_factory=list)
    changes_property: str | None = None
    comma_separated: bool = field(default_factory=bool)
    condition: str = ""
    button_effects: str = ""  # these effects will run AFTER the button's own effects
    paged: bool = field(default_factory=bool)
