from typing import Optional
import discord

from eagxf.typedefs import DcButton, DcMessage, DcView, Receiver, ReceiverFuture


class ViewMsg:
    def __init__(
        self,
        view: DcView | None = None,
        message: DcMessage | None = None,
        raw_message: str | None = None,
    ) -> None:
        self.view = view
        self.message = message
        self.raw_message = raw_message

    async def send(
        self,
        receiver_future: Optional[ReceiverFuture] = None,
        receiver: Optional[Receiver] = None,
    ) -> None:
        assert (
            self.message or self.raw_message and self.view
        ), "(Error 16) No message content or view to send"
        assert (
            self.message or receiver or receiver_future
        ), "(Error 17) No receiver to send to"
        if (self.message or receiver) and receiver_future:
            receiver_future.close()
        if self.message:
            await self.edit()
        elif self.raw_message and self.view:
            if receiver:
                await self.deliver_to(receiver)
            elif receiver_future:
                await self.deliver_to(await receiver_future)

    async def deliver_to(self, receiver: Receiver) -> None:
        assert (
            self.raw_message and self.view
        ), "(Error 18) No message content or view to send"
        self.message = await receiver.send(content=self.raw_message, view=self.view)

    async def edit(self) -> None:
        assert (
            self.message and self.raw_message and self.view
        ), "(Error 19) No message, message content or view to edit"
        await self.message.edit(content=self.raw_message, view=self.view)

    def update(
        self,
        view: DcView | None = None,
        message: DcMessage | None = None,
        raw_message: str | None = None,
    ) -> "ViewMsg":
        self.view = view or self.view
        self.message = message or self.message
        self.raw_message = raw_message or self.raw_message
        return self

    async def add_reaction(self, reaction: discord.Emoji | str) -> None:
        if not self.message:
            print("(Error 6) No message to add reaction to")
            return
        await self.message.add_reaction(reaction)

    async def delete(self) -> None:
        if not self.message:
            print("(Error 7) No message to delete")
            return
        await self.message.delete()
        self.message = None

    def add_button(self, button: DcButton) -> None:
        assert self.view, "(Error 20) No view to add button to"
        self.view.add_item(button)

    def remove_button(self, button: DcButton) -> None:
        assert self.view, "(Error 21) No view to remove button from"
        self.view.remove_item(button)
