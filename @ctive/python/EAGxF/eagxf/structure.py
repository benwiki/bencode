from dataclasses import dataclass, field

from eagxf.button import Button
from eagxf.constants import INCOMPLETE_PROFILE_MSG


@dataclass
class Structure:
    id: str = field(default_factory=str)
    message: str = field(default_factory=str)
    buttons: list[Button] = field(default_factory=list)
    reactions: list[str] = field(default_factory=list)
    changed_property: str | None = None
    conditions: str = ""
    # these effects will run AFTER the button's own effects
    after_button_effects: str = ""
    paged: bool = field(default_factory=bool)

    @property
    def condition_message(self) -> str:
        messages = []
        for condition in self.conditions.split(", "):
            if msg := self.get_message_for_condition(condition):
                messages.append(msg)
        return "\n\n".join(messages)

    def get_message_for_condition(self, condition: str) -> str:
        if condition == "profile_complete":
            return INCOMPLETE_PROFILE_MSG
        return ""
