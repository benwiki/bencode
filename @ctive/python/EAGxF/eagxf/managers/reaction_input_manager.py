from typing import Callable

import discord

from eagxf.button import Button
from eagxf.constants import NUM_EMOJI, PAGE_STEP, REACTION_PROPERTIES
from eagxf.enums.effect import Effect
from eagxf.enums.property import Property
from eagxf.enums.screen_id import ScreenId
from eagxf.managers.output_manager import OutputManager
from eagxf.meetings import Meeting
from eagxf.status import EMOJI_STATUS, Status
from eagxf.user import User


class ReactionInputManager:
    def __init__(self, opm: OutputManager) -> None:
        self.opm = opm
        self.users = opm.users

        self.reaction_func_list: list[Callable[[User, str]]] = [
            self.handle_status_change,
            self.handle_best_match_prio_order,
            self.handle_selected_user,
            self.handle_meeting,
        ]
        self.reaction_funcs = dict(zip(REACTION_PROPERTIES, self.reaction_func_list))

        self.save_btn = Button(
            label="💾 Save",
            takes_to=ScreenId.BEST_MATCHES,
            effects=[
                Effect.SAVE_BEST_MATCHES,
                Effect.DELETE_MESSAGE,
                Effect.RESET_NEW_PRIO_ORDER,
            ],
            style=discord.ButtonStyle.green,
        )
        self.save_btn.callback = self.opm.get_callback_to_screen(  # type: ignore
            ScreenId.BEST_MATCHES, button=self.save_btn
        )

    async def handle_added_reaction(
        self, reaction: discord.RawReactionActionEvent
    ) -> None:
        user = self.users.get(reaction.user_id)
        if not user or not user.change:
            return
        prop_to_change = user.change
        if prop_to_change.is_search():
            prop_to_change = prop_to_change.from_search()

        if user.dc_message and reaction.message_id == user.dc_message.id:
            if handle_reaction := self.reaction_funcs.get(prop_to_change):
                await handle_reaction(user, reaction.emoji.name)
                user.change = None

    async def handle_removed_reaction(
        self, reaction: discord.RawReactionActionEvent
    ) -> None:
        user = self.users.get(reaction.user_id)
        if not user:
            return

        if user.dc_message and reaction.message_id == user.dc_message.id:
            if user.change == Property.BEST_MATCH_PRIO_ORDER:
                await self.handle_best_match_prio_order(
                    user, reaction.emoji.name, remove=True
                )

    # ====================================================================== #
    async def handle_status_change(self, user: User, emoji: str) -> None:
        if not user.search_filter or not user.change:
            return  # only because of type hinting
        search = user.change.is_search()
        changed_user = user.search_filter if search else user
        pronome = "your" if not search else "the filter's"

        if not (status := EMOJI_STATUS.get(emoji)):
            if not (emoji == "❓" and search):
                return
            status = Status.ANY
        changed_user.status = status

        await user.delete_message()
        user.remove_screens_until_stop()
        user.replace = {
            "<changed_prop>": f"changed {pronome} status",
            "<new_value>": f"{emoji} (**{status.value}**)",
            "<plus_info>": "",
        }
        await self.opm.send_screen(ScreenId.SUCCESSFUL_PROP_CHANGE, user)
        user.save()

    # ====================================================================== #
    async def handle_best_match_prio_order(
        self, user: User, emoji: str, remove: bool = False
    ) -> None:
        if not (num := self.validate_number_reaction(emoji, user)):
            return

        if remove:
            user.best_match_prio_order_new.remove(num - 1)
        else:
            user.best_match_prio_order_new.append(num - 1)

        none_selected = user.best_match_prio_order_new == []

        if remove and none_selected:
            user.remove_button_from_message(self.save_btn)
            user.has_save_btn = False
        elif not remove and not user.has_save_btn:
            user.add_button_to_message(self.save_btn)
            user.has_save_btn = True

        await self.opm.send_screen(ScreenId.CHANGE_BEST_MATCHES_PRIORITY, user)

    def validate_number_reaction(self, emoji_name: str, user: User) -> int | None:
        if emoji_name not in NUM_EMOJI:
            return None
        num = NUM_EMOJI.index(emoji_name) + 1
        if not (1 <= num <= PAGE_STEP) or not user.dc_message:
            return None
        return num

    # ====================================================================== #
    async def handle_selected_user(self, user: User, emoji: str) -> None:
        if not (num := self.validate_number_reaction(emoji, user)):
            return
        selected_user_id = user.get_result_by_number(num)
        user.selected_user = self.users[selected_user_id]
        await user.delete_message()
        await self.opm.send_screen(ScreenId.SELECTED_USER, user)

    # ====================================================================== #
    async def handle_meeting(self, user: User, emoji: str) -> None:
        last_screen = user.last_screen
        if not (num := self.validate_number_reaction(emoji, user)) or not last_screen:
            return
        selected_meeting: Meeting = user.get_result_by_number(num)
        user.selected_meeting = selected_meeting
        user.selected_user = self.users[selected_meeting.partner_id]
        await user.delete_message()
        await self.opm.send_screen(ScreenId.EDIT_MEETING, user)
