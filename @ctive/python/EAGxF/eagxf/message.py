from dataclasses import dataclass
from typing import Optional

from eagxf.constants import SPACER
from eagxf.typedefs import (
    DcButton,
    DcEmoji,
    DcMessage,
    DcView,
    Receiver,
)


@dataclass
class Message:
    dc_view: Optional[DcView] = None
    dc_message: Optional[DcMessage] = None
    msg_text: Optional[str] = None

    @staticmethod
    def spacer():
        return Message(dc_view=DcView(), msg_text=SPACER + "\\_" * 50)

    async def send(self, receiver: Receiver) -> None:
        assert (
            self.dc_message or self.msg_text and self.dc_view
        ), "(Error #1) No message content or view to send"
        if self.dc_message:
            await self.edit()
        elif self.msg_text and self.dc_view:
            await self.deliver_to(receiver)

    async def deliver_to(self, receiver: Receiver) -> None:
        assert (
            self.msg_text and self.dc_view
        ), "(Error #2) No message content or view to send"
        self.dc_message = await receiver.send(content=self.msg_text, view=self.dc_view)

    async def edit(self) -> None:
        assert (
            self.dc_message and self.msg_text and self.dc_view
        ), "(Error #3) No message, message content or view to edit"
        self.dc_message = await self.dc_message.edit(
            content=self.msg_text, view=self.dc_view
        )

    def update(
        self,
        dc_view: Optional[DcView] = None,
        dc_message: Optional[DcMessage] = None,
        message_text: Optional[str] = None,
    ) -> "Message":
        self.dc_view = dc_view or self.dc_view
        self.dc_message = dc_message or self.dc_message
        self.msg_text = message_text or self.msg_text
        return self

    async def add_reaction(self, reaction: DcEmoji | str) -> None:
        if not self.dc_message:
            print("(Error #4) No message to add reaction to")
            return
        await self.dc_message.add_reaction(reaction)

    async def delete(self) -> None:
        if not self.dc_message:
            # print("(Error #5) No message to delete")
            return
        await self.dc_message.delete()
        self.dc_message = None

    def add_button(self, button: DcButton) -> None:
        assert self.dc_view, "(Error #6) No view to add button to"
        self.dc_view.add_item(button)
        print("Button added:", button)

    def remove_button(self, button: DcButton) -> None:
        assert self.dc_view, "(Error #7) No view to remove button from"
        self.dc_view.remove_item(button)

    @property
    def sleeping(self) -> bool:
        return not self.dc_message
