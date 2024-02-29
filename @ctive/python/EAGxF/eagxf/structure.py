from dataclasses import dataclass, field

from eagxf.button import Button


@dataclass
class Structure:
    id: str = field(default_factory=str)
    message: str = field(default_factory=str)
    buttons: list[Button] = field(default_factory=list)
    reactions: list[str] = field(default_factory=list)
    changes_property: str | None = None
    comma_separated: bool = False
    condition: str = ""
