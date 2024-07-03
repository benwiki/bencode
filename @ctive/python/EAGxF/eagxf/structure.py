from dataclasses import dataclass, field

from eagxf.button import Button
from eagxf.constants import INCOMPLETE_PROFILE_MSG
from eagxf.enums.effect import Effect
from eagxf.enums.property import Property
from eagxf.enums.structure_condition import StructCond


@dataclass
class Structure:
    id: str = field(default_factory=str)
    message: str = field(default_factory=str)
    buttons: list[Button] = field(default_factory=list)
    reactions: list[str] = field(default_factory=list)
    changed_property: Property | None = None
    conditions: list[StructCond] = field(default_factory=list)
    # ⏬ These effects will run AFTER the button's own effects
    after_button_effects: list[Effect] = field(default_factory=list)
    paged: bool = field(default_factory=lambda: False)

    @property
    def condition_message(self) -> str:
        messages = []
        for condition in self.conditions:
            if msg := self.get_message_for_condition(condition):
                messages.append(msg)
        return "\n\n".join(messages)

    def get_message_for_condition(self, condition: StructCond) -> str:
        return {
            StructCond.PROFILE_COMPLETE: INCOMPLETE_PROFILE_MSG,
        }.get(condition, "")

    def init_pagination(self) -> None:
        self.after_button_effects += [Effect.DELETE_MESSAGE]
        self.push_buttons_down()
        for button in self.buttons:
            button.effects += [Effect.EMPTY_RESULTS]
        self.buttons += Button.get_navigation_buttons(self.id)
        if not self.changed_property:
            self.changed_property = Property.SELECTED_USER

    def push_buttons_down(self) -> None:
        for button in self.buttons:
            if button.row:
                button.row += 1
            else:
                button.row = 1
