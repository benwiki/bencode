from dataclasses import dataclass, field
from typing import Optional

from eagxf.message import Message
from eagxf.typedefs import (
    DcButton,
    DcEmoji,
    DcMessage,
    DcView,
    Receiver,
)


@dataclass
class MessageBundle:
    spacer: Message = field(default_factory=Message.spacer)
    front_spacer: Message = field(default_factory=Message.spacer)
    body: Message = field(default_factory=Message)
    notifications: list[Message] = field(default_factory=list)

    async def add_reaction(self, emoji: DcEmoji | str):
        await self.body.add_reaction(emoji)

    async def send_front_spacer(self, receiver: Receiver) -> None:
        await self.front_spacer.send(receiver)

    async def delete_front_spacer(self) -> None:
        await self.front_spacer.delete()

    async def send(self, receiver: Receiver) -> None:
        await self.spacer.send(receiver)
        await self.body.send(receiver)
        for noti in self.notifications:
            await noti.send(receiver)

    async def delete(self, spacer_too: bool) -> None:
        if spacer_too:
            await self.spacer.delete()
        await self.body.delete()
        for noti in self.notifications:
            await noti.delete()

    def add_button(self, button: DcButton) -> None:
        self.body.add_button(button)

    def remove_button(self, button: DcButton) -> None:
        self.body.remove_button(button)

    def update(
        self,
        dc_view: Optional[DcView] = None,
        dc_message: Optional[DcMessage] = None,
        message_text: Optional[str] = None,
    ) -> None:
        self.body.update(dc_view, dc_message, message_text)

    @property
    def sleeping(self) -> bool:
        return (
            self.spacer.sleeping
            and self.body.sleeping
            and all(noti.sleeping for noti in self.notifications)
        )
