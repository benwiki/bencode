import asyncio
import os
from typing import Callable, Iterable, Iterator

import discord
from discord import ButtonStyle
from discord.ext import commands

from eagxf.button import Button
from eagxf.constant_functions import PROFILE
from eagxf.constants import (
    ADMINS,
    EMOJI_STATUS,
    INCOMPLETE_PROFILE_WARNING,
    NUM_EMOJI,
    PAGE_STEP,
    QUESTION_NAMES,
    SPACER,
    SPECIAL_DESTINATIONS,
    STATUS_EMOJI,
    USERS_PATH,
    VISIBLE_SIMPLE_USER_PROPS,
)
from eagxf.date import Date
from eagxf.meetings import Meeting
from eagxf.status import Status
from eagxf.structure import Structure
from eagxf.structures import PRIORITY_MESSAGE, STRUCTURES
from eagxf.typedefs import DcButton, DcMessage, DcUser, DcView
from eagxf.user import User
from eagxf.util import to_emojis
from eagxf.view_msg import ViewMsg


class Logic(commands.Cog):
    def __init__(self, client: discord.Client) -> None:
        self.client = client
        self.init_users()
        self.init_structures()
        self.init_other_stuff()

    def init_users(self) -> None:
        self.users: dict[int, User] = self.load_users()
        for user in self.users.values():
            asyncio.create_task(self.send_starting_message_to(user))

    async def send_starting_message_to(self, user: User) -> None:
        await self.send_structure(STRUCTURES["home"], user)  # type: ignore

    def init_structures(self) -> None:
        for structure_id, structure in STRUCTURES.items():
            structure.id = structure_id
            if structure.paged:
                self.init_paged_structure(structure)
            for button in structure.buttons:
                self.init_button_with(button, structure)

    def init_paged_structure(self, structure: Structure) -> None:
        structure.after_button_effects = self.comma_add(
            structure.after_button_effects, "delete_message"
        )
        self.push_buttons_down_for(structure)
        for button in structure.buttons:
            button.effects = self.comma_add(button.effects, "empty_results")
        structure.buttons += Button.get_navigation_buttons(structure.id)
        structure.changed_property = "selected_user"

    def comma_add(self, original: str, additional: str) -> str:
        if original:
            return f"{original}, {additional}"
        return additional

    def push_buttons_down_for(self, structure: Structure) -> None:
        for button in structure.buttons:
            if button.row:
                button.row += 1
            else:
                button.row = 1

    def init_button_with(self, button: Button, structure: Structure) -> None:
        to_structure = STRUCTURES.get(button.takes_to)
        if to_structure is None and button.takes_to not in SPECIAL_DESTINATIONS:
            print(f"Structure with id {button.takes_to} not found!")
        button.callback = self.get_structure_callback(  # type: ignore
            to_structure, button=button
        )
        if structure.after_button_effects:
            button.effects = self.comma_add(
                button.effects, structure.after_button_effects
            )

    def init_other_stuff(self) -> None:
        self.home_btn: DcButton = DcButton(label="🏠 Home", style=ButtonStyle.primary)
        self.home_btn.callback = self.get_structure_callback(STRUCTURES["home"])  # type: ignore
        self.save_btn = Button(
            label="💾 Save",
            takes_to="best_matches",
            effects="save_best_matches, delete_message, reset_new_prio_order",
            style=ButtonStyle.green,
        )
        self.save_btn.callback = self.get_structure_callback(  # type: ignore
            STRUCTURES["best_matches"], button=self.save_btn
        )
        self.prio_functions: list[Callable[[User, User], int | Status]] = [
            lambda u1, u2: u1.get_language_score(u2),
            lambda u1, u2: u1.get_question_score(u2),
            lambda u1, u2: u1.get_keywords_score(u2),
            lambda u1, u2: u1.get_location_distance(u2),
            lambda u1, u2: u1.get_status(u2),
            lambda u1, u2: u1.get_headline_score(u2),
        ]
        self.reaction_funcs: dict[str, Callable] = {  # pylint: disable=C0103
            "status": self.handle_status_change,
            "best_match_prio_order": self.handle_best_match_prio_order,
            "selected_user": self.handle_selected_user,
        }
        self.add_reactions = True
        self.DEBUGGING = True  # pylint: disable=C0103
        asyncio.create_task(self.refresh())

    async def refresh(self) -> None:
        while True:
            await asyncio.sleep(60)
            for user in self.users.values():
                if user.structure_stack:
                    await self.send_structure(user.structure_stack[-1], user=user)

    def get_structure_callback(
        self, structure: Structure | None, button: Button | None = None
    ):
        async def callback(interaction: discord.Interaction) -> None:
            await interaction.response.defer()
            user = self.users[interaction.user.id]
            if button and button.effects:
                for effect in button.effects.split(", "):
                    await user.apply_effect(effect)
            if button and button.takes_to == "<back>" and len(user.structure_stack) > 1:
                await self.send_structure(user.back_to_structure, user)  # type: ignore
            elif structure:
                await self.send_structure(structure, user)
            else:
                print(f"No structure found for the button '{button}'!")

        return callback

    async def send_structure(self, structure: Structure, user: User) -> None:
        self.stack_structure(user, structure)
        self.collect_data_for(user, structure)

        user.view_msg = await self.get_view_msg_for(user, structure)
        receiver_future = self.client.fetch_user(user.id)
        await user.view_msg.send(receiver_future=receiver_future)

        if structure.changed_property:
            user.change = structure.changed_property

        if user.add_reactions and structure.reactions:
            for emoji in structure.reactions:
                await user.view_msg.add_reaction(emoji)

        if structure.paged and user.view_msg:
            await self.add_special_reactions_for(user)

    def stack_structure(self, user: User, structure: Structure) -> None:
        if structure.id == "home":
            user.structure_stack = [structure]
        elif structure.id in user.structure_stack:
            struct_index = user.structure_stack.index(structure)
            user.structure_stack = user.structure_stack[: struct_index + 1]
        elif user.structure_stack == [] or user.structure_stack[-1].id != structure.id:
            user.structure_stack.append(structure)

    def collect_data_for(self, user: User, structure: Structure) -> None:
        if structure.id in ["search", "show_search_results"]:
            user.results = self.search_users_for(user)
        if structure.id == "best_matches":
            user.results = self.search_best_matches_for(user)
        if structure.id == "interests_sent":
            user.results = user.interests_sent_not_received
        if structure.id == "interests_received":
            user.results = user.interests_received_not_sent
        if structure.id == "mutual_interests":
            user.results = user.mutual_interests

    async def get_view_msg_for(self, user: User, structure: Structure) -> ViewMsg:
        if not user.struct_conditions_apply_for(structure):
            ok_btn = self.get_ok_button_for(user, wanted_structure="edit_profile")
            view = self.get_view([ok_btn])
            message = structure.condition_message
            user.add_reactions = False
        else:
            buttons: Iterator[Button] = filter(
                user.btn_conditions_apply_for, structure.buttons
            )
            view = self.get_view(buttons)
            message = self.replace_placeholders(structure.message, user)
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

    async def add_special_reactions_for(self, user: User) -> None:
        for i in range(min(PAGE_STEP, len(user.results) - user.page * PAGE_STEP)):
            await user.view_msg.add_reaction(NUM_EMOJI[i])

    def search_users_for(self, user_searching: User) -> list[int]:
        return [
            user.id
            for user in self.users.values()
            if user.is_selected_by(user_searching)
        ]

    def additional_info_with_side_effects(self, user: User) -> str:
        if not user.is_complete() and user.status != Status.INVISIBLE:
            user.status = Status.INVISIBLE
            return INCOMPLETE_PROFILE_WARNING
        return ""

    def replace_placeholders(self, msg: str, user: User | None) -> str:
        if not user:
            return msg

        msg = user.replace_placeholders(msg)
        msg = (
            msg.replace("<search_results>", self.get_formatted_results_for(user))
            .replace(
                "<best_matches>",
                self.get_formatted_results_for(user, additional=user.get_score_summary),
            )
            .replace("<page_reference>", self.get_page_reference_for(user))
            .replace("<interests_sent>", self.get_interests(user))
            .replace("<interests_received>", self.get_interests(user))
            .replace("<mutual_interests>", self.get_interests(user))
            .replace("<selected_user_name>", self.get_name_of(user.selected_user))
            .replace(
                "<selected_user_profile>",
                (
                    user.selected_user.replace_placeholders(
                        PROFILE(name=self.get_name_of(user.selected_user) + "'s")
                    )
                    if user.selected_user
                    else ""
                ),
            )
            .replace(
                "<selected_user_meetings>",
                self.get_meetings(user, "upcoming", selected=True),
            )
            .replace("<upcoming_meetings>", self.get_meetings(user, "upcoming"))
            .replace("<past_meetings>", self.get_meetings(user, "past"))
        )
        return msg

    def get_name_of(self, user: User | None) -> str:
        return user.name if user else ""

    def get_meetings(self, user: User, kind: str, selected: bool = False) -> str:
        if kind == "upcoming":
            meetings = user.meetings.upcoming
        elif kind == "past":
            meetings = user.meetings.past
        else:
            return ""

        if selected and user.selected_user:
            meetings = [m for m in meetings if m.partner_id == user.selected_user.id]

        if not meetings:
            return "**No meetings yet.**"
        return "- " + "\n - ".join(
            f"**{m.date}**"
            + (f" with ***{self.users[m.partner_id].name}***" if not selected else "")
            for m in meetings
        )

    def get_interests(self, user: User) -> str:
        return "\n".join(
            f"{self.prefix(i+1, user)}{NUM_EMOJI[i]} "
            f".: ***{u.name}*** :. (Headline: *{u.headline}*)"
            for i, u in enumerate(self.get_results_for(user))
        )

    def prefix(self, i: int, user: User) -> str:
        i = i + user.page * PAGE_STEP
        return f"**{i // PAGE_STEP}** " if i >= PAGE_STEP else "   "

    def get_page_reference_for(self, user: User) -> str:
        page_from = user.page * PAGE_STEP + 1
        page_to = min((user.page + 1) * PAGE_STEP, len(user.results))
        page_total = len(user.results)
        return f"**({page_from} - {page_to}) from total {page_total}**"

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
                f"\n- *{p['label']}:* {getattr(u, p_id)}"
                for p_id, p in VISIBLE_SIMPLE_USER_PROPS.items()
                if p_id != "name"
            )
            + "\n***------❓Questions ------***"
            + "".join(
                f"\n- *{q['label']}:* {u.questions[q_id]}"
                for q_id, q in QUESTION_NAMES.items()
            )
            for i, u in enumerate(self.get_results_for(user))
        )

    def get_results_for(self, user: User) -> Iterator[User]:
        return self.users_by_ids(self.paged_list_of(user.results, user))

    def paged_list_of(self, lst: list, user: User) -> list[int]:
        return lst[user.page * PAGE_STEP : (user.page + 1) * PAGE_STEP]

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
            await self.send_structure(STRUCTURES["home"], user)  # type: ignore
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
        """Sends the user's home structure."""
        if ctx.author.id not in self.users:
            return
        await self.bye(ctx)
        user = self.users[ctx.author.id]
        user.best_match_prio_order_new = []
        await self.send_structure(user.last_structure or STRUCTURES["home"], user)  # type: ignore

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
        if (
            user is None
            or user.change in [*self.reaction_funcs, ""]
            or not user.search_filter
        ):
            return

        ok_btn = self.get_ok_button_for(user)

        await user.view_msg.delete()

        changed = change = user.change
        search = change.startswith("search_")
        if search:  # chop off the "search_" prefix
            change = changed = change[7:]

        change_user = user.search_filter if search else user
        pronome = "Your" if not search else "The filter's"
        plural = change in ["keywords", "languages"]
        kw_needed = plural or search and change in QUESTION_NAMES
        has_have = "have" if plural else "has"
        changed_to = msg.content
        verb = "changed"

        if kw_needed:
            need_caps = change == "languages"
            evenly_spaced_kws = self.evenly_space(msg.content, need_caps)
            changed_to = evenly_spaced_kws

        if change in QUESTION_NAMES:
            changed = "answer"
            # TODO: ratyi!
            change_user.questions[change] = changed_to
        # TODO: úristen de ratyi!
        elif change == "meeting_request":
            if Date.is_valid(changed_to) and user.selected_user:
                user.request_meeting_with_selected(Date.from_str(changed_to))
                ok_btn = self.get_ok_button_for(user)
                changed = f"meeting with ***{user.selected_user.name}***"
                verb = "set"
            else:
                await msg.add_reaction("❌")
                message = "Invalid date! Try again!\nFormat should be: dd.mm.yyyy hh:mm"
                ok_btn = self.get_ok_button_for(user)
                view = self.get_view([ok_btn, self.home_btn])
                user.view_msg.update(raw_message=SPACER + message, view=view)
                await user.view_msg.send(receiver=msg.author)
                return
        else:
            setattr(change_user, change, changed_to)

        await msg.add_reaction("✅")
        message = f'✅ {pronome} {changed} {has_have} been {verb} to "{changed_to}"!'
        message += self.additional_info_with_side_effects(user)

        view = self.get_view([ok_btn, self.home_btn])
        user.view_msg.update(raw_message=SPACER + message, view=view)
        await user.view_msg.send(receiver=msg.author)
        user.change = ""
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
        if not user:
            return
        change = user.change
        if change.startswith("search_"):
            change = change[7:]

        if user.view_msg.message and payload.message_id == user.view_msg.message.id:
            if handle_reaction := self.reaction_funcs.get(change):
                await handle_reaction(user, payload.emoji.name)

    async def handle_status_change(self, user: User, emoji: str) -> None:
        if not user.search_filter:
            return  # only because of type hinting
        search = user.change.startswith("search_")
        changed_user = user.search_filter if search else user
        pronome = "Your" if not search else "The filter's"

        if not (status := EMOJI_STATUS.get(emoji)):
            if not (emoji == "❓" and search):
                return
            status = Status.ANY
        changed_user.status = status

        ok_btn = self.get_ok_button_for(user, wanted_structure="edit_profile")
        view = self.get_view([ok_btn, self.home_btn])

        await user.view_msg.delete()
        message = f"✅ {pronome} status has been changed to {emoji} ({status.value})!"
        user.view_msg.update(raw_message=SPACER + message, view=view)
        receiver_future = self.client.fetch_user(user.id)
        await user.view_msg.send(receiver_future=receiver_future)
        user.save()

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

    async def handle_selected_user(self, user: User, emoji: str) -> None:
        num = self.validate_number_reaction(emoji, user)
        if not num:
            return
        selected_user_id = user.results[user.page * PAGE_STEP + num - 1]
        user.selected_user = self.users[selected_user_id]
        await user.view_msg.delete()
        await self.send_structure(STRUCTURES["selected_user"], user)  # type: ignore

    def validate_number_reaction(self, emoji_name: str, user: User) -> int | None:
        if emoji_name not in NUM_EMOJI:
            return None
        num = NUM_EMOJI.index(emoji_name) + 1
        if not (1 <= num <= PAGE_STEP) or not user.view_msg.message:
            return None
        return num

    @commands.Cog.listener()
    async def on_raw_reaction_remove(
        self, payload: discord.RawReactionActionEvent
    ) -> None:
        user = self.users.get(payload.user_id)
        if not user or not user.search_filter:
            return

        if user.view_msg.message and payload.message_id == user.view_msg.message.id:
            if user.change == "best_match_prio_order":
                await self.handle_best_match_prio_order(
                    user, payload.emoji.name, remove=True
                )

    def get_ok_button_for(
        self,
        user: User,
        wanted_structure: str = "",
        default_structure: str = "home",
    ) -> DcButton:
        button: DcButton = DcButton(label="OK", style=ButtonStyle.green)
        button.callback = self.get_structure_callback(  # type: ignore
            STRUCTURES.get(wanted_structure)
            or user.back_to_structure
            or STRUCTURES[default_structure]
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
