import asyncio
from typing import Callable, Iterable, Iterator

import discord

from eagxf.button import Button
from eagxf.constant_functions import PROFILE
from eagxf.constants import (
    ADMINS,
    DEBUGGING,
    NUM_EMOJI,
    QUESTION_NAMES,
    SPACER,
    SPECIAL_DESTINATIONS,
    VISIBLE_SIMPLE_USER_PROPS,
)
from eagxf.enums.meeting_time import MtgTime
from eagxf.enums.screen_id import ScreenId
from eagxf.managers.user_manager import UserManager
from eagxf.message import Message
from eagxf.screen import Screen
from eagxf.screens import SCREENS
from eagxf.status import STATUS_EMOJI
from eagxf.typedefs import DcButton, DcView
from eagxf.user import User
from eagxf.util import peek, to_emojis


class OutputManager:
    def __init__(self, um: UserManager) -> None:
        self.um = um
        self.users = um.users

        self.replace_funcs: dict[str, Callable[[User], str]] = {
            "<search_results>": self.get_formatted_results_for,
            "<best_matches>": self.get_formatted_results_for,
            # lambda u: self.get_formatted_results_for(
            #     u, additional=u.get_score_summary
            # ),
            "<interests_sent>": self.get_interests,
            "<interests_received>": self.get_interests,
            "<mutual_interests>": self.get_interests,
            "<selected_user_name>": lambda u: self.get_name_of(u.selected_user),
            "<selected_user_profile>": self.selected_user_profile,
            "<selected_user_meetings>": lambda u: self.um.get_meetings(
                u, MtgTime.FUTURE, selected=True, peek=True
            ),
            "<future_meetings_peek>": lambda u: self.um.get_meetings(
                u, MtgTime.FUTURE, peek=True
            ),
            "<past_meetings_peek>": lambda u: self.um.get_meetings(
                u, MtgTime.PAST, peek=True
            ),
            "<future_meetings>": lambda u: self.um.get_meetings(u, MtgTime.FUTURE),
            "<past_meetings>": lambda u: self.um.get_meetings(u, MtgTime.PAST),
        }

    def start(self) -> None:
        self.init_screens()
        for user in self.users.values():
            asyncio.create_task(self.send_starting_message_to(user))
        asyncio.create_task(self.refresh())

    async def send_starting_message_to(self, user: User) -> None:
        # await self.send_screen(ScreenId.DELETING_OLD_MESSAGES, user)
        # await self.remove_past_messages(user)
        await self.send_screen(ScreenId.HOME, user)

    async def remove_past_messages(self, user: User) -> None:
        if dc_user := self.um.get_user(user.id):
            async for msg in dc_user.history(limit=None):
                if msg.author.id != dc_user.id and not (
                    user.dc_message and msg.id == user.dc_message.id
                ):
                    await msg.delete()

    def init_screens(self) -> None:
        for screen_id, screen in SCREENS.items():
            screen.id = screen_id
            if screen.paged:
                screen.init_pagination()
            for button in screen.buttons:
                self.init_button_with(button, screen)

    def init_button_with(self, button: Button, screen: Screen) -> None:
        go_to_screen = SCREENS.get(button.takes_to)
        if go_to_screen is None and button.takes_to not in SPECIAL_DESTINATIONS:
            print(f"(Error 4) Screen with id {button.takes_to} not found!")
        button.callback = self.get_callback_to_screen(  # type: ignore
            go_to_screen, button=button
        )
        if screen.after_button_effects:
            button.effects += screen.after_button_effects

    def get_callback_to_screen(
        self, screen: Screen | ScreenId | None, button: Button | None = None
    ):
        async def callback(interaction: discord.Interaction) -> None:
            await interaction.response.defer()

            user = self.users[interaction.user.id]
            if button and button.effects:
                for effect in button.effects:
                    await user.apply_effect(effect, self.um.client)
            if button and button.takes_to in SPECIAL_DESTINATIONS:
                await self.send_special_screen(user, button)
            elif screen:
                await self.send_screen(screen, user)
            else:
                print(f"(Error 3) No screen found for the button '{button}'!")

        return callback

    async def send_special_screen(self, user: User, button: Button) -> None:
        match button.takes_to:
            case ScreenId.BACK__ if user.last_screen:
                if user.can_go_back:
                    user.remove_last_screen()
                await self.send_screen(user.last_screen, user)
            case ScreenId.MEETINGS_AT_TIME__:
                user.remove_screens_until_stop()
                ascreen = user.last_screen
                assert ascreen is not None, "(Error 23) No screen found for the button!"
                await self.send_screen(ascreen, user)

    async def refresh(self) -> None:
        while True:
            await asyncio.sleep(30)
            for user in self.um.users.values():
                if user.last_screen:
                    await self.send_screen(user.last_screen, user)

    async def send_screen(self, screen: Screen | ScreenId, user: User) -> None:
        if isinstance(screen, ScreenId):
            screen = SCREENS[screen]
        user.stack(screen)
        user.results = self.screen_to_data(user, screen.id)

        user.set_message(await self.get_message_for(user, screen))
        receiver_future = self.um.fetch_user(user.id)
        await user.send_message(receiver_future=receiver_future)

        if screen.changed_property:
            user.change = screen.changed_property

        if user.add_reactions:
            if screen.reactions:
                for emoji in screen.reactions:
                    await user.add_reaction_to_message(emoji)
            if screen.paged:
                await user.add_selection_reactions()

    def screen_to_data(self, user: User, screen_id: ScreenId) -> list:
        match screen_id:
            case ScreenId.SEARCH | ScreenId.SHOW_SEARCH_RESULTS:
                return self.um.search_users_for(user)
            case ScreenId.BEST_MATCHES:
                return self.um.search_best_matches_for(user)
            case ScreenId.INTERESTS_SENT:
                return user.interests_sent_not_received
            case ScreenId.INTERESTS_RECEIVED:
                return user.interests_received_not_sent
            case ScreenId.MUTUAL_INTERESTS:
                return user.mutual_interests
            case ScreenId.FUTURE_MEETINGS:
                return user.future_meetings
            case ScreenId.PAST_MEETINGS:
                return user.past_meetings
            case _:
                return []

    async def get_message_for(self, user: User, screen: Screen) -> Message:
        if not user.screen_conditions_apply_for(screen):
            ok_button = Button.ok()
            ok_button.callback = self.get_callback_to_screen(None, ok_button)  # type: ignore
            dc_view = self.get_dc_view([ok_button])
            message = screen.condition_message
            user.add_reactions = False
        else:
            buttons: Iterator[Button] = filter(
                user.btn_conditions_apply_for, screen.buttons
            )
            dc_view = self.get_dc_view(buttons)
            message = self.replace_placeholders(screen.message, user)
            user.add_reactions = True

        message_text = SPACER + message if screen.spacer else message
        return user.update_message(dc_view=dc_view, message_text=message_text)

    def get_dc_view(self, buttons: Iterable[Button | DcButton]) -> DcView:
        dc_view = DcView()
        for button in buttons:
            dc_view.add_item(button)
        if DEBUGGING:
            stop_btn = Button(label="STOP", style=discord.ButtonStyle.red)
            stop_btn.callback = self.stop_callback  # type: ignore
            dc_view.add_item(stop_btn)
        return dc_view

    async def stop_callback(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()
        await self.stop_request_by(interaction.user.id)

    async def stop_request_by(self, user_id: int) -> None:
        if user_id not in ADMINS:
            print(f"(Error 2) Unauthorized user (id: {user_id}) tried to stop the bot.")
            return
        await self.um.stop()

    def replace_placeholders(self, msg: str, user: User | None) -> str:
        if user:
            msg = user.replace_placeholders(msg)
            for placeholder, function in self.replace_funcs.items():
                if placeholder in msg:
                    msg = msg.replace(placeholder, function(user))
        return msg

    def get_formatted_results_for(
        self,
        user: User,
        additional: Callable[[User], str] | None = None,
    ) -> str:
        if not user.results:
            return "***No results to show.***"
        separator = "***========================***\n"
        return separator + f"\n\n{separator}".join(
            f"{to_emojis(i+1)} .: ***{u.name}*** :. "
            f"(Status: {STATUS_EMOJI[u.status]} "
            f"({u.status.value}))"
            f"{additional(u) if additional else ''}"
            + "".join(
                f"\n- *{p['label']}:* {getattr(u, p_id.to_str)}"
                for p_id, p in VISIBLE_SIMPLE_USER_PROPS.items()
                if p_id != "name"
            )
            + "\n***------❓Questions ------***"
            + "".join(
                f"\n- *{q['label']}:* {peek(u.questions[q_id])}"
                for q_id, q in QUESTION_NAMES.items()
            )
            for i, u in enumerate(self.um.get_results_for(user))
        )

    def get_interests(self, user: User) -> str:
        if not user.results:
            return "***No interests to show.***"
        return "\n".join(
            f"{user.page_prefix(i+1)}{NUM_EMOJI[i]} "
            f".: ***{u.name}*** :. (Job: *{u.job}*, Company: *{u.company}*)"
            for i, u in enumerate(self.um.get_results_for(user))
        )

    def get_name_of(self, user: User | None) -> str:
        return user.name if user else "(no user selected)"

    def selected_user_profile(self, user: User) -> str:
        if not user.selected_user:
            return ""
        return user.selected_user.replace_placeholders(
            PROFILE(name=self.get_name_of(user.selected_user) + "'s")
        )
