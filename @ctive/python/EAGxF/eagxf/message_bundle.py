from dataclasses import dataclass, field
from typing import Optional

from eagxf.message import Message
from eagxf.typedefs import DcButton, DcEmoji, DcMessage, DcView, Receiver


@dataclass
class MessageBundle:
    spacer: Message = field(default_factory=Message.spacer)
    front_spacer: Message = field(default_factory=Message.spacer)
    body: Message = field(default_factory=Message)
    notifications: list[Message] = field(default_factory=list)

    async def add_reaction(self, emoji: DcEmoji | str):
        await self.body.add_reaction(emoji)

    async def send_front_spacer(self, receiver: Receiver) -> None:
        await self.front_spacer.send_to(receiver)

    async def delete_front_spacer(self) -> None:
        await self.front_spacer.delete()

    async def send_to(self, receiver: Receiver) -> None:
        await self.spacer.send_to(receiver)
        await self.body.send_to(receiver)
        for noti in self.notifications:
            await noti.send_to(receiver)

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

    def update_body(
        self,
        message_text: str,
        dc_view: Optional[DcView] = None,
        dc_message: Optional[DcMessage] = None,
    ) -> None:
        self.body.update(message_text, dc_view, dc_message)

    def add_notification(self, noti_message: Message):
        self.notifications.append(noti_message)

    async def remove_notification(self, msg_id: int):
        for noti in self.notifications:
            if noti.dc_message and noti.dc_message.id == msg_id:
                await noti.delete()
                self.notifications.remove(noti)
                return
        raise RuntimeError(f"(Error #1) No notification '{msg_id}' found")

    @property
    def sleeping(self) -> bool:
        return (
            self.spacer.inactive
            and self.body.inactive
            and all(noti.inactive for noti in self.notifications)
        )
