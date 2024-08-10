from typing import Optional

import discord

from eagxf.typedefs import DcButton, DcMessage, DcView, Receiver, ReceiverFuture


class Message:
    def __init__(
        self,
        dc_view: DcView | None = None,
        dc_message: DcMessage | None = None,
        msg_text: str | None = None,
    ) -> None:
        self.dc_view = dc_view
        self.dc_message = dc_message
        self.msg_text = msg_text

    async def send(
        self,
        receiver_future: Optional[ReceiverFuture] = None,
        receiver: Optional[Receiver] = None,
    ) -> None:
        assert (
            self.dc_message or self.msg_text and self.dc_view
        ), "(Error 16) No message content or view to send"
        assert (
            self.dc_message or receiver or receiver_future
        ), "(Error 17) No receiver to send to"
        if (self.dc_message or receiver) and receiver_future:
            receiver_future.close()
        if self.dc_message:
            await self.edit()
        elif self.msg_text and self.dc_view:
            if receiver:
                await self.deliver_to(receiver)
            elif receiver_future:
                await self.deliver_to(await receiver_future)

    async def deliver_to(self, receiver: Receiver) -> None:
        assert (
            self.msg_text and self.dc_view
        ), "(Error 18) No message content or view to send"
        self.dc_message = await receiver.send(content=self.msg_text, view=self.dc_view)

    async def edit(self) -> None:
        assert (
            self.dc_message and self.msg_text and self.dc_view
        ), "(Error 19) No message, message content or view to edit"
        self.dc_message = await self.dc_message.edit(
            content=self.msg_text, view=self.dc_view
        )

    def update(
        self,
        dc_view: DcView | None = None,
        dc_message: DcMessage | None = None,
        message_text: str | None = None,
    ) -> "Message":
        self.dc_view = dc_view or self.dc_view
        self.dc_message = dc_message or self.dc_message
        self.msg_text = message_text or self.msg_text
        return self

    async def add_reaction(self, reaction: discord.Emoji | str) -> None:
        if not self.dc_message:
            print("(Error 6) No message to add reaction to")
            return
        await self.dc_message.add_reaction(reaction)

    async def delete(self) -> None:
        if not self.dc_message:
            print("(Error 7) No message to delete")
            return
        await self.dc_message.delete()
        self.dc_message = None

    def add_button(self, button: DcButton) -> None:
        assert self.dc_view, "(Error 20) No view to add button to"
        self.dc_view.add_item(button)

    def remove_button(self, button: DcButton) -> None:
        assert self.dc_view, "(Error 21) No view to remove button from"
        self.dc_view.remove_item(button)
