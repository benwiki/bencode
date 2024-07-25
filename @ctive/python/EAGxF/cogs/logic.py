import asyncio
import os
from operator import is_
from typing import Callable, Iterable, Iterator

import discord
from discord import ButtonStyle
from discord.ext import commands

from eagxf.button import Button
from eagxf.constant_functions import PROFILE
from eagxf.constants import (
    ADMINS,
    EMOJI_STATUS,
    NUM_EMOJI,
    PAGE_STEP,
    QUESTION_NAMES,
    SPACER,
    SPECIAL_DESTINATIONS,
    STATUS_EMOJI,
    VISIBLE_SIMPLE_USER_PROPS,
)
from eagxf.date import Date
from eagxf.enums.effect import Effect
from eagxf.enums.meeting_time import MtgTime
from eagxf.enums.screen_id import ScreenId
from eagxf.enums.property import Property
from eagxf.meetings import Meeting
from eagxf.status import Status
from eagxf.screen import Screen
from eagxf.screens import PRIORITY_MESSAGE, SCREENS
from eagxf.typedefs import DcButton, DcMessage, DcUser, DcView
from eagxf.user import User
from eagxf.util import to_emojis
from eagxf.view_msg import ViewMsg
from main import USERS_PATH


class Logic(commands.Cog):
    def __init__(self, client: discord.Client) -> None:
        self.client = client
        self.init_users()
        self.init_screens()
        self.init_other_stuff()

    def init_users(self) -> None:
        self.users: dict[int, User] = self.load_users()
        for user in self.users.values():
            asyncio.create_task(self.send_starting_message_to(user))

    async def send_starting_message_to(self, user: User) -> None:
        await self.send_screen(SCREENS[ScreenId.HOME], user)  # type: ignore

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
            print(f"Screen with id {button.takes_to} not found!")
        button.callback = self.get_callback_to_screen(  # type: ignore
            go_to_screen, button=button
        )
        if screen.after_button_effects:
            button.effects += screen.after_button_effects

    def init_other_stuff(self) -> None:
        self.home_btn: DcButton = DcButton(label="🏠 Home", style=ButtonStyle.primary)
        self.home_btn.callback = self.get_callback_to_screen(SCREENS["home"])  # type: ignore
        self.save_btn = Button(
            label="💾 Save",
            takes_to=ScreenId.BEST_MATCHES,
            effects=[
                Effect.SAVE_BEST_MATCHES,
                Effect.DELETE_MESSAGE,
                Effect.RESET_NEW_PRIO_ORDER,
            ],
            style=ButtonStyle.green,
        )
        self.save_btn.callback = self.get_callback_to_screen(  # type: ignore
            SCREENS[ScreenId.BEST_MATCHES], button=self.save_btn
        )
        self.prio_functions: list[Callable[[User, User], int | Status]] = [
            lambda u1, u2: u1.get_language_score(u2),
            lambda u1, u2: u1.get_question_score(u2),
            lambda u1, u2: u1.get_keywords_score(u2),
            lambda u1, u2: u1.get_location_distance(u2),
            lambda u1, u2: u1.get_status(u2),
            lambda u1, u2: u1.get_job_score(u2),
            lambda u1, u2: u1.get_company_score(u2),
        ]
        self.reaction_funcs: dict[Property, Callable] = {  # pylint: disable=C0103
            Property.STATUS: self.handle_status_change,
            Property.BEST_MATCH_PRIO_ORDER: self.handle_best_match_prio_order,
            Property.SELECTED_USER: self.handle_selected_user,
            Property.MEETING: self.handle_meeting,
        }
        self.add_reactions = True
        self.DEBUGGING = True  # pylint: disable=C0103
        asyncio.create_task(self.refresh())

    async def refresh(self) -> None:
        while True:
            await asyncio.sleep(60)
            for user in self.users.values():
                if user.last_screen:
                    await self.send_screen(user.last_screen, user)

    def get_callback_to_screen(
        self, screen: Screen | None, button: Button | None = None
    ):
        async def callback(interaction: discord.Interaction) -> None:
            await interaction.response.defer()

            user = self.users[interaction.user.id]
            if button and button.effects:
                for effect in button.effects:
                    await user.apply_effect(effect, self.client)
            if button and button.takes_to == "<back>" and len(user.screen_stack) > 1:
                await self.send_screen(user.back_to_screen, user)  # type: ignore
            elif screen:
                await self.send_screen(screen, user)
            else:
                print(f"No screen found for the button '{button}'!")

        return callback

    async def send_screen(self, screen: Screen, user: User) -> None:
        user.stack(screen)
        user.results = self.screen_to_data(user, screen.id)

        user.view_msg = await self.get_view_msg_for(user, screen)
        receiver_future = self.client.fetch_user(user.id)
        await user.view_msg.send(receiver_future=receiver_future)

        if screen.changed_property:
            user.change = screen.changed_property

        if user.add_reactions and screen.reactions:
            for emoji in screen.reactions:
                await user.view_msg.add_reaction(emoji)

        if screen.paged:
            await user.add_special_reactions()

    def screen_to_data(self, user: User, screen_id: ScreenId) -> list:
        match screen_id:
            case ScreenId.SEARCH:
                return self.search_users_for(user)
            case ScreenId.SHOW_SEARCH_RESULTS:
                return self.search_users_for(user)
            case ScreenId.BEST_MATCHES:
                return self.search_best_matches_for(user)
            case ScreenId.INTERESTS_SENT:
                return user.interests_sent_not_received
            case ScreenId.INTERESTS_RECEIVED:
                return user.interests_received_not_sent
            case ScreenId.MUTUAL_INTERESTS:
                return user.mutual_interests
            case ScreenId.FUTURE_MEETINGS:
                return user.meetings.future
            case ScreenId.PAST_MEETINGS:
                return user.meetings.past
            case _:
                return []

    async def get_view_msg_for(self, user: User, screen: Screen) -> ViewMsg:
        if not user.screen_conditions_apply_for(screen):
            ok_btn = self.get_ok_button_for(user, wanted_screen=ScreenId.EDIT_PROFILE)
            view = self.get_view([ok_btn])
            message = screen.condition_message
            user.add_reactions = False
        else:
            buttons: Iterator[Button] = filter(
                user.btn_conditions_apply_for, screen.buttons
            )
            view = self.get_view(buttons)
            message = self.replace_placeholders(screen.message, user)
            user.add_reactions = True

        return user.view_msg.update(view, raw_message=SPACER + message)

    def search_best_matches_for(self, user: User) -> list[int]:
        matches_list = sorted(
            filter(
                lambda u: u.id != user.id and u.status != Status.INVISIBLE,
                self.users.values(),
            ),
            key=lambda u: self.get_priority(user, u),
            reverse=True,
        )
        return [u.id for u in matches_list]

    def register_user(self, dc_user: DcUser) -> User:
        user = self.users[dc_user.id] = User.from_dc_user(dc_user)
        user.save()
        return user

    def search_users_for(self, user_searching: User) -> list[int]:
        return [
            user.id
            for user in self.users.values()
            if user.is_selected_by(user_searching)
        ]

    def replace_placeholders(self, msg: str, user: User | None) -> str:
        if not user:
            return msg

        msg = user.replace_placeholders(msg)
        functions: dict[str, Callable[[User], str]] = {
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
            "<selected_user_meetings>": lambda u: self.get_meetings(
                u, MtgTime.FUTURE, selected=True, peek=True
            ),
            "<future_meetings_peek>": lambda u: self.get_meetings(
                u, MtgTime.FUTURE, peek=True
            ),
            "<past_meetings_peek>": lambda u: self.get_meetings(
                u, MtgTime.PAST, peek=True
            ),
            "<future_meetings>": lambda u: self.get_meetings(u, MtgTime.FUTURE),
            "<past_meetings>": lambda u: self.get_meetings(u, MtgTime.PAST),
        }
        for placeholder, function in functions.items():
            if placeholder in msg:
                msg = msg.replace(placeholder, function(user))
        return msg

    def selected_user_profile(self, user: User) -> str:
        if not user.selected_user:
            return ""
        return user.selected_user.replace_placeholders(
            PROFILE(name=self.get_name_of(user.selected_user) + "'s")
        )

    def get_name_of(self, user: User | None) -> str:
        return user.name if user else "(no user selected)"

    def get_meetings(
        self, user: User, kind: MtgTime, selected=False, peek=False
    ) -> str:
        meetings = {
            MtgTime.FUTURE: user.meetings.future,
            MtgTime.PAST: user.meetings.past,
        }.get(kind, [])

        if selected and user.selected_user:
            meetings = [m for m in meetings if m.partner_id == user.selected_user.id]
        if not meetings:
            return "***No meetings to show.***"

        dots_needed = False
        if peek:
            dots_needed = len(meetings) > 5
            meetings = meetings[:5]

        return "\n".join(
            ("- " if peek else f"{user.page_prefix(i+1)}{NUM_EMOJI[i]} ")
            + f"**{m.date}**"
            + (f" with ***{self.users[m.partner_id].name}***" if not selected else "")
            for i, m in enumerate(meetings)
        ) + ("\n**...**" if dots_needed else "")

    def get_interests(self, user: User) -> str:
        return "\n".join(
            f"{user.page_prefix(i+1)}{NUM_EMOJI[i]} "
            f".: ***{u.name}*** :. (Job: *{u.job}*, Company: *{u.company}*)"
            for i, u in enumerate(self.get_results_for(user))
        )

    def get_formatted_results_for(
        self,
        user: User,
        additional: Callable[[User], str] | None = None,
    ) -> str:
        separator = "***========================***\n"
        return separator + f"\n\n{separator}".join(
            f"{to_emojis(i+1)} .: ***{u.name}*** :. "
            f"(Status: {STATUS_EMOJI[u.status]} "
            f"({u.status.value}))"
            f"{additional(u) if additional else ''}"
            + "".join(
                f"\n- *{p['label']}:* {getattr(u, p_id.low)}"
                for p_id, p in VISIBLE_SIMPLE_USER_PROPS.items()
                if p_id != "name"
            )
            + "\n***------❓Questions ------***"
            + "".join(
                f"\n- *{q['label']}:* {u.questions[q_id.low]}"
                for q_id, q in QUESTION_NAMES.items()
            )
            for i, u in enumerate(self.get_results_for(user))
        )

    def get_results_for(self, user: User) -> Iterator[User]:
        return self.users_by_ids(user.paged_list_of_results())

    def users_by_ids(self, user_ids: list[int]) -> Iterator[User]:
        return map(lambda x: self.users[x], user_ids)

    def get_priority(self, user: User, u: User) -> tuple:
        """This function takes into account the best match priority order of the user"""
        return tuple(
            self.prio_functions[i](user, u) for i in user.best_match_prio_order
        )

    @commands.command(name="enter")
    async def enter(self, ctx: commands.Context) -> None:
        """Registers the user."""
        if ctx.author.id not in self.users:
            user = self.register_user(ctx.author)
            await self.send_screen(SCREENS["home"], user)  # type: ignore
        else:
            user = self.users[ctx.author.id]
            await user.view_msg.delete()
            ok_btn = self.get_ok_button_for(user)
            view = self.get_view([ok_btn])
            message = "You're already in the platform!"
            user.view_msg.update(view=view, raw_message=SPACER + message)
            await user.view_msg.send(receiver=ctx)

    @commands.command(name="stop")
    async def stop(self, ctx: commands.Context) -> None:
        """Stops the bot."""
        await self.stop_request_by(ctx.author.id)

    @commands.command(name="reset")
    async def reset(self, ctx: commands.Context) -> None:
        """Resets the bot."""
        await self.hi(ctx)

    @commands.command(name="hi")
    async def hi(self, ctx: commands.Context) -> None:
        """Sends the user's last screen."""
        if ctx.author.id not in self.users:
            return
        await self.bye(ctx)
        user = self.users[ctx.author.id]
        user.best_match_prio_order_new = []
        await self.send_screen(user.last_screen or SCREENS["home"], user)  # type: ignore

    @commands.command(name="bye")
    async def bye(self, ctx: commands.Context) -> None:
        """Deletes the user's last message."""
        if ctx.author.id not in self.users:
            return
        user = self.users[ctx.author.id]
        await user.view_msg.delete()

    @commands.Cog.listener()
    async def on_message(self, msg: DcMessage) -> None:
        user = self.users.get(msg.author.id)
        if user is None or user.change is None or user.change in self.reaction_funcs:
            return

        ok_btn = self.get_ok_button_for(user)
        await user.view_msg.delete()

        prop_to_change = user.change
        search = prop_to_change.is_search()
        if search:  # chop off the "search_" prefix
            prop_to_change = prop_to_change.from_search()
        changed = prop_to_change.low

        change_user = user
        if search and user.search_filter is not None:
            change_user = user.search_filter
        elif search:
            return

        pronome = "Your" if not search else "The filter's"
        plural = prop_to_change in [Property.KEYWORDS, Property.LANGUAGES]
        kw_needed = plural or search and prop_to_change in QUESTION_NAMES
        has_have = "have" if plural else "has"
        new_prop_value = msg.content
        verb = "changed"

        if kw_needed:
            need_caps = prop_to_change == Property.LANGUAGES
            evenly_spaced_kws = self.evenly_space(msg.content, need_caps)
            new_prop_value = evenly_spaced_kws

        if prop_to_change in QUESTION_NAMES:
            changed = "answer"
            # TODO: better, but still terrible! GOTTA FIX
            change_user.questions.set(prop_to_change, new_prop_value)
        # TODO: goodness, terrible code! GOTTA FIX
        elif prop_to_change in [Property.MEETING_REQUEST, Property.MEETING_DATE]:
            assert user.selected_user, "(E1) No selected user for meeting!"
            if (
                Date.is_valid(new_prop_value)
                and Date.from_str(new_prop_value).is_future()
            ):
                if prop_to_change == Property.MEETING_DATE:
                    user.cancel_meeting_with_selected()
                user.request_meeting_with_selected(Date.from_str(new_prop_value))
                wanted_screen = {
                    Property.MEETING_REQUEST: ScreenId.SELECTED_USER,
                    Property.MEETING_DATE: ScreenId.FUTURE_MEETINGS,
                }[prop_to_change]
                ok_btn = self.get_ok_button_for(user, wanted_screen=wanted_screen)
                changed = f"meeting with ***{user.selected_user.name}***"
                verb = "set"
            else:
                await msg.add_reaction("❌")
                message = (
                    "Invalid date, try again!\nFormat should be: **dd.mm.yyyy hh:mm**"
                    "\nAnd it should be in the future!\n\nClick OK to proceed!"
                )
                wanted_screen = {
                    Property.MEETING_REQUEST: ScreenId.MEETING_REQUEST,
                    Property.MEETING_DATE: ScreenId.EDIT_MEETING,
                }[prop_to_change]
                ok_btn = self.get_ok_button_for(user, wanted_screen=wanted_screen)
                view = self.get_view([ok_btn, self.home_btn])
                user.view_msg.update(raw_message=SPACER + message, view=view)
                await user.view_msg.send(receiver=msg.author)
                return
        else:
            setattr(change_user, prop_to_change.low, new_prop_value)

        await msg.add_reaction("✅")
        message = (
            f'✅ {pronome} {changed} {has_have} been {verb} to "{new_prop_value}"!'
        )
        message += user.additional_info_with_side_effects()

        view = self.get_view([ok_btn, self.home_btn])
        user.view_msg.update(raw_message=SPACER + message, view=view)
        await user.view_msg.send(receiver=msg.author)
        user.change = None
        user.save()

    def evenly_space(self, text: str, capitalize: bool) -> str:
        return ", ".join(
            " & ".join(
                w.capitalize() if capitalize else w
                for w in map(str.strip, kw.split("&"))  # type: ignore
            )
            for kw in map(str.strip, text.split(","))  # type: ignore
        )

    @commands.Cog.listener()
    async def on_raw_reaction_add(
        self, payload: discord.RawReactionActionEvent
    ) -> None:
        user = self.users.get(payload.user_id)
        if not user or not user.change:
            return
        change = user.change
        if change.is_search():
            change = change.from_search()

        if user.view_msg.message and payload.message_id == user.view_msg.message.id:
            if handle_reaction := self.reaction_funcs.get(change):
                await handle_reaction(user, payload.emoji.name)

    # ====================================================================== #
    async def handle_status_change(self, user: User, emoji: str) -> None:
        if not user.search_filter or not user.change:
            return  # only because of type hinting
        search = user.change.is_search()
        changed_user = user.search_filter if search else user
        pronome = "Your" if not search else "The filter's"

        if not (status := EMOJI_STATUS.get(emoji)):
            if not (emoji == "❓" and search):
                return
            status = Status.ANY
        changed_user.status = status

        ok_btn = self.get_ok_button_for(user, wanted_screen=ScreenId.EDIT_PROFILE)
        view = self.get_view([ok_btn, self.home_btn])

        await user.view_msg.delete()
        message = f"✅ {pronome} status has been changed to {emoji} ({status.value})!"
        user.view_msg.update(raw_message=SPACER + message, view=view)
        receiver_future = self.client.fetch_user(user.id)
        await user.view_msg.send(receiver_future=receiver_future)
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
            user.view_msg.remove_button(self.save_btn)
            user.has_save_btn = False
        elif not remove and not user.has_save_btn:
            user.view_msg.add_button(self.save_btn)
            user.has_save_btn = True

        message = self.replace_placeholders(PRIORITY_MESSAGE, user)
        user.view_msg.update(raw_message=SPACER + message)
        await user.view_msg.send()

    def validate_number_reaction(self, emoji_name: str, user: User) -> int | None:
        if emoji_name not in NUM_EMOJI:
            return None
        num = NUM_EMOJI.index(emoji_name) + 1
        if not (1 <= num <= PAGE_STEP) or not user.view_msg.message:
            return None
        return num

    # ====================================================================== #
    async def handle_selected_user(self, user: User, emoji: str) -> None:
        if not (num := self.validate_number_reaction(emoji, user)):
            return
        selected_user_id = user.get_result_by_number(num)
        user.selected_user = self.users[selected_user_id]
        await user.view_msg.delete()
        await self.send_screen(SCREENS["selected_user"], user)  # type: ignore

    # ====================================================================== #
    async def handle_meeting(self, user: User, emoji: str) -> None:
        last_screen = user.last_screen
        if not (num := self.validate_number_reaction(emoji, user)) or not last_screen:
            return
        selected_meeting: Meeting = user.get_result_by_number(num)
        user.selected_meeting = selected_meeting
        user.selected_user = self.users[selected_meeting.partner_id]
        await user.view_msg.delete()
        await self.send_screen(SCREENS["edit_meeting"], user)  # type: ignore

    @commands.Cog.listener()
    async def on_raw_reaction_remove(
        self, payload: discord.RawReactionActionEvent
    ) -> None:
        user = self.users.get(payload.user_id)
        if not user or not user.search_filter:
            return

        if user.view_msg.message and payload.message_id == user.view_msg.message.id:
            if user.change == Property.BEST_MATCH_PRIO_ORDER:
                await self.handle_best_match_prio_order(
                    user, payload.emoji.name, remove=True
                )

    def get_ok_button_for(
        self,
        user: User,
        wanted_screen: ScreenId | None = None,
        default_screen: ScreenId = ScreenId.HOME,
    ) -> DcButton:
        button: DcButton = DcButton(label="OK", style=ButtonStyle.green)
        button.callback = self.get_callback_to_screen(  # type: ignore
            SCREENS.get(wanted_screen)
            if wanted_screen
            else user.back_to_screen or SCREENS[default_screen]
        )
        return button

    def get_view(self, buttons: Iterable[Button | DcButton]) -> DcView:
        view = DcView()
        for button in buttons:
            view.add_item(button)
        if self.DEBUGGING:
            stop_btn = Button(label="STOP", style=ButtonStyle.red)
            stop_btn.callback = self.stop_callback  # type: ignore
            view.add_item(stop_btn)
        return view

    async def stop_callback(self, interaction: discord.Interaction) -> None:
        await interaction.response.defer()
        await self.stop_request_by(interaction.user.id)

    async def stop_request_by(self, user_id: int) -> None:
        if user_id not in ADMINS:
            print(f"Unauthorized user (id: {user_id}) tried to stop the bot.")
            return
        for user in self.users.values():
            await user.view_msg.delete()
        await self.client.close()

    def is_valid_date(self, date: str) -> bool:
        return (
            len(date) == 10
            and date[2] == date[5] == "."
            and date.replace(".", "").isnumeric()
        )

    def load_users(self) -> dict[int, User]:
        return {
            int(id_str): User.load_by_id(id_str)
            for filename in os.listdir(USERS_PATH)
            if (id_str := self.valid_file_name(filename))
        }

    def valid_file_name(self, name: str) -> str:
        if name.endswith(".json") and (id_str := name[:-5]).isdecimal():
            return id_str
        return ""


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Logic(bot))
