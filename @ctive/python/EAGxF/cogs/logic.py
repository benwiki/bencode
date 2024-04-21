import asyncio
import datetime
import json
import os
import re
from typing import Callable, Iterator, Sequence

import discord
from discord import ButtonStyle
from discord.ext import commands
from discord.ui import Button as DCButton
from discord.ui import View as DCView

from eagxf.button import Button
from eagxf.constants import (
    ADMINS,
    APP_NAME,
    DEFAULT_PRIO_ORDER,
    EMOJI_STATUS,
    NUM_EMOJI,
    NUM_NAME,
    PRIO_LIST_LENGTH,
    QUESTION_NAMES,
    SPACER,
    STATUS_EMOJI,
    USERS_FOLDER_PATH,
    VISIBLE_SIMPLE_USER_PROPS,
)
from eagxf.date import Date
from eagxf.platform_user import PlatformUser
from eagxf.status import Status
from eagxf.structure import Structure
from eagxf.structures import PRIORITY_MESSAGE, STRUCTURES
from eagxf.user_saver import UserManager


class Logic(commands.Cog):
    def __init__(self, client: discord.Client) -> None:
        self.client = client
        self.init_users()
        self.init_structures()
        self.init_other_stuff()

    def init_users(self) -> None:
        self.users_path = self.init_users_path()
        self.users: dict[int, PlatformUser] = self.load_users()
        for user in self.users.values():
            asyncio.create_task(self.send_starting_message_to(user))

    async def send_starting_message_to(self, user: PlatformUser) -> None:
        await self.send_structure(user, STRUCTURES["home"])  # type: ignore

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
        structure.changes_property = "selected_user"

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
        if to_structure is None:
            print(f"Structure with id {button.takes_to} not found!")
        button.callback = self.get_structure_callback(  # type: ignore
            to_structure, button=button
        )
        if structure.after_button_effects:
            button.effects = self.comma_add(
                button.effects, structure.after_button_effects
            )

    def init_other_stuff(self) -> None:
        self.home_btn: DCButton = DCButton(label="🏠 Home", style=ButtonStyle.primary)
        self.home_btn.callback = self.get_structure_callback(STRUCTURES["home"])  # type: ignore
        self.save_btn = Button(
            label="💾 Save",
            takes_to="best_matches",
            effect="save_prio, delete_message, reset_new_prio_order",
            style=ButtonStyle.green,
        )
        self.save_btn.callback = self.get_structure_callback(  # type: ignore
            STRUCTURES["best_matches"], button=self.save_btn
        )
        self.not_alnum = re.compile(r"[\W_]+", re.UNICODE)
        self.PRIO_FUNCTIONS = [  # pylint: disable=C0103
            self.get_language_score,
            self.get_question_score,
            self.get_keywords_score,
            self.get_location_distance,
            self.get_status,
            self.get_headline_score,
        ]
        self.REACTION_FUNCTIONS: dict[str, Callable] = {  # pylint: disable=C0103
            "status": self.handle_status_change,
            "best_match_prio_order": self.handle_best_match_prio_order,
            "selected_user": self.handle_selected_user,
        }
        self.DEBUGGING = False  # pylint: disable=C0103
        self.page_step = 10
        asyncio.create_task(self.refresh())

    async def refresh(self) -> None:
        while True:
            await asyncio.sleep(60)
            for user in self.users.values():
                if user.last_structure:
                    await self.send_structure(user, user.last_structure)

    def get_structure_callback(
        self, structure: Structure | None, button: Button | None = None
    ):
        async def callback(interaction: discord.Interaction) -> None:
            await interaction.response.defer()
            user = self.users[interaction.user.id]
            if button and button.effects:
                for effect in button.effects.split(", "):
                    await self.affect(effect, user)
            if button and button.takes_to == "<back>" and user.back_to_structure:
                await self.send_structure(user, user.back_to_structure)
            elif structure:
                await self.send_structure(user, structure)
            else:
                print(f"No structure found for the button '{button}'!")

        return callback

    async def affect(self, effect: str, user: PlatformUser) -> None:
        if effect == "go_to_previous_page":
            user.page -= 1
        if effect == "go_to_next_page":
            user.page += 1
        if effect == "delete_message":
            await self.delete_last_msg_of(user)
        if effect == "save_prio":
            user.best_match_prio_order = user.best_match_prio_order_new
            self.save_user(user)
        if effect == "reset_new_prio_order":
            user.best_match_prio_order_new = []
        if effect == "default_best_matches":
            user.best_match_prio_order = list(range(PRIO_LIST_LENGTH))
            self.save_user(user)
        if effect == "reset_user_property_change":
            user.change = ""
        if effect == "empty_results":
            user.results = []
            user.page = 0
        if effect == "send_interest":
            self.send_interest(user)
        if effect == "cancel_interest":
            self.cancel_interest(user)

    def send_interest(self, user: PlatformUser) -> None:
        if not user.selected_user:
            return
        user.selected_user.interests["received"].append(user.id)
        user.interests["sent"].append(user.selected_user.id)
        self.save_user(user.selected_user)
        self.save_user(user)

    def cancel_interest(self, user: PlatformUser) -> None:
        if not user.selected_user:
            return
        user.selected_user.interests["received"].remove(user.id)
        user.interests["sent"].remove(user.selected_user.id)
        self.save_user(user.selected_user)
        self.save_user(user)

    async def send_structure(self, user: PlatformUser, structure: Structure) -> None:
        user.back_to_structure = user.last_structure

        self.collect_data_for(user, structure)

        if structure.condition and not self.condition_true_for(
            structure.condition, user
        ):
            ok_btn = self.get_ok_button_for(user, wanted_structure="edit_profile")
            view = self.get_view([ok_btn])
            message = self.get_condition_message(structure.condition, user)
            add_reactions = False
        else:
            buttons = [
                button
                for button in structure.buttons
                if self.btn_condition_true_for(user, button.condition)
            ]
            view = self.get_view(buttons)
            message = self.replace_placeholders(structure.message, user)
            add_reactions = True
        user.last_view = view

        if user.last_msg:
            await user.last_msg.edit(content=SPACER + message, view=view)
        else:
            dc_user = await self.client.fetch_user(user.id)
            user.last_msg = await dc_user.send(SPACER + message, view=view)
        user.last_structure = structure

        if structure.changes_property:
            user.change = structure.changes_property

        if add_reactions and structure.reactions:
            for emoji in structure.reactions:
                await user.last_msg.add_reaction(emoji)
        await self.add_special_reactions_for(user, structure)

    def collect_data_for(self, user: PlatformUser, structure: Structure) -> None:
        if structure.id in ["search", "show_search_results"]:
            user.results = self.search_users_for(user)
        if structure.id == "best_matches":
            user.results = self.search_best_matches_for(user)
        if structure.id == "interests_sent":
            user.results = user.interests["sent"]
        if structure.id == "interests_received":
            user.results = user.interests["received"]

    def search_best_matches_for(self, user: PlatformUser) -> list[int]:
        matches_list = sorted(
            filter(
                lambda u: u.id != user.id and u.status != Status.INVISIBLE,
                self.users.values(),
            ),
            key=lambda u: self.get_priority(user, u),
            reverse=True,
        )
        return [u.id for u in matches_list]

    def register_user(self, dc_user: discord.User | discord.Member) -> PlatformUser:
        current = datetime.datetime.now()
        user = self.users[dc_user.id] = PlatformUser(
            id=dc_user.id,
            date_joined=Date(
                day=current.day,
                month=current.month,
                year=current.year,
            ),
            name=dc_user.name,
            questions={q: "?" for q in QUESTION_NAMES},
            search_filter=PlatformUser(
                questions={q: "?" for q in QUESTION_NAMES},
                status=Status.ANY,
            ),
            best_match_prio_order=list(range(PRIO_LIST_LENGTH)),
            interests={"sent": [], "received": []},
        )
        self.save_user(user)
        return user

    async def add_special_reactions_for(
        self, user: PlatformUser, structure: Structure
    ) -> None:
        if structure.paged and user.last_msg:
            for i in range(
                min(self.page_step, len(user.results) - user.page * self.page_step)
            ):
                await user.last_msg.add_reaction(NUM_EMOJI[i])

    def search_users_for(self, user_searching: PlatformUser) -> list[int]:
        if not user_searching.search_filter:
            return []
        return [
            user.id
            for user in self.users.values()
            if user.is_selected_by(user_searching)
        ]

    def condition_true_for(self, condition: str, user: PlatformUser) -> bool:
        if condition == "profile_complete":
            return user.is_complete()
        return False

    def get_condition_message(self, condition: str, user: PlatformUser) -> str:
        if condition == "profile_complete":
            return user.incomplete_msg()
        return ""

    def additional_info_with_side_effects(self, user: PlatformUser) -> str:
        if (
            not self.condition_true_for("profile_complete", user)
            and user.status != Status.INVISIBLE
        ):
            user.status = Status.INVISIBLE
            return (
                "\n\n*(Your profile is incomplete, so your status has been "
                "changed to invisible!)*"
            )
        return ""

    def btn_condition_true_for(self, user: PlatformUser, condition: str) -> bool:
        if not condition:
            return True
        if condition == "has_previous_page":
            return user.page > 0
        if condition == "has_next_page":
            return user.page < (len(user.results) - 1) // self.page_step
        if condition == "prio_order_full":
            return len(user.best_match_prio_order_new) == PRIO_LIST_LENGTH
        if condition in ["interest_sent", "interest_not_sent"]:
            interest_sent = (
                user.selected_user is not None
                and user.id in user.selected_user.interests["received"]
                and user.selected_user.id in user.interests["sent"]
            )
            if condition == "interest_sent":
                return interest_sent
            if condition == "interest_not_sent":
                return not interest_sent
        print(f"Invalid condition: {condition}")
        return False

    def replace_placeholders(self, message: str, user: PlatformUser) -> str:
        message = (
            message.replace("<id>", str(user.id))
            .replace("<date_joined>", str(user.date_joined))
            .replace("<status>", f"{STATUS_EMOJI[user.status]} ({user.status.value})")
            .replace("<number_of_results>", str(len(user.results)))
            .replace("<search_results>", self.get_formatted_results_for(user))
            .replace(
                "<best_matches>",
                self.get_formatted_results_for(
                    user, additional=self.get_score_summary(user)
                ),
            )
            .replace("<page_reference>", self.get_page_reference_for(user))
            .replace(
                "<best_match_prio_order_new>",
                self.format_priority_order(user, new=True),
            )
            .replace("<best_match_prio_order>", self.format_priority_order(user))
            .replace("<num_of_interests_sent>", str(len(user.interests["sent"])))
            .replace(
                "<num_of_interests_received>", str(len(user.interests["received"]))
            )
            .replace("<interests_sent>", self.get_interests(user, "sent"))
            .replace("<interests_received>", self.get_interests(user, "received"))
            .replace("<selected_user_name>", self.get_name_of(user.selected_user))
        )
        for q_id in QUESTION_NAMES:
            message = message.replace(f"<{q_id}>", user.questions[q_id])
        for prop_id in VISIBLE_SIMPLE_USER_PROPS:
            message = message.replace(f"<{prop_id}>", getattr(user, prop_id))
        if user.search_filter:
            message = message.replace(
                "<search_status>", self.get_search_status(user.search_filter)
            )
            for q_id in QUESTION_NAMES:
                message = message.replace(
                    f"<search_{q_id}>", user.search_filter.questions[q_id]
                )
            for prop_id in VISIBLE_SIMPLE_USER_PROPS:
                message = message.replace(
                    f"<search_{prop_id}>", getattr(user.search_filter, prop_id)
                )
        return message

    def get_name_of(self, user: PlatformUser | None) -> str:
        return user.name if user else ""

    def get_interests(self, user: PlatformUser, kind: str) -> str:
        return "\n".join(
            f"{self.prefix(i+1, user)}{NUM_EMOJI[i]} .: ***{u.name}*** :. (Headline: *{u.headline}*)"
            for i, u in enumerate(self.get_results_for(user, user.interests[kind]))
        )

    def prefix(self, i: int, user: PlatformUser) -> str:
        i = i + user.page * self.page_step
        return f"**{i // self.page_step}** " if i >= self.page_step else "   "

    def get_search_status(self, search_filter: PlatformUser) -> str:
        return (
            "?"
            if search_filter.status == Status.ANY
            else f"{STATUS_EMOJI[search_filter.status]} "
            f"({search_filter.status.value})"
        )

    def get_page_reference_for(self, user: PlatformUser) -> str:
        page_from = user.page * self.page_step + 1
        page_to = min((user.page + 1) * self.page_step, len(user.results))
        page_total = len(user.results)
        return f"**({page_from} - {page_to}) from total {page_total}**"

    def get_formatted_results_for(
        self,
        user: PlatformUser,
        additional: Callable[[PlatformUser], str] | None = None,
    ) -> str:
        separator = "***========================***\n"
        return separator + f"\n\n{separator}".join(
            f"{self.to_emojis(i+1)} .: ***{u.name}*** :. "
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
            for i, u in enumerate(self.get_results_for(user, user.results))
        )

    def get_results_for(
        self, user: PlatformUser, results: list[int]
    ) -> Iterator[PlatformUser]:
        return self.users_by_ids(self.paged_list_of(results, user))

    def get_score_summary(self, user: PlatformUser) -> Callable[[PlatformUser], str]:
        """Returns a summary of the scores of the user and the other user."""
        return lambda other: (
            f"\n[SCORE: "
            f"(Lang: {self.get_language_score(user, other)}) "
            f"(Q: {self.get_question_score(user, other)}) "
            f"(Kw: {self.get_keywords_score(user, other)}) "
            f"(H.line: {self.get_headline_score(user, other)}) "
            f"(Loc: {self.get_location_distance(user, other)}) "
            "]"
        )

    def to_emojis(self, number: int) -> str:
        """Converts a number to emojis. E.g. 123 -> ":one::two::three:"""
        return "".join(f":{NUM_NAME[int(n)]}:" for n in str(number))

    def paged_list_of(self, lst: list, user: PlatformUser) -> list[int]:
        return lst[user.page * self.page_step : (user.page + 1) * self.page_step]

    def users_by_ids(self, user_ids: list[int]) -> Iterator[PlatformUser]:
        return map(lambda x: self.users[x], user_ids)

    def get_priority(self, user: PlatformUser, u: PlatformUser) -> tuple:
        """This function takes into account the best match priority order of the user"""
        return tuple(
            self.PRIO_FUNCTIONS[i](user, u) for i in user.best_match_prio_order
        )

    def get_status(self, _: PlatformUser, u: PlatformUser) -> Status:
        """Returns the status of the user."""
        return u.status

    def format_priority_order(self, user: PlatformUser, new: bool = False) -> str:
        """Returns the best match priority order of the user in a formatted way."""
        order = user.best_match_prio_order_new if new else user.best_match_prio_order
        things = range(2, PRIO_LIST_LENGTH + 1)
        return ("1. " if order != [] else "") + "\n{}. ".join(
            DEFAULT_PRIO_ORDER[i] for i in order
        ).format(*things)

    def get_language_score(self, user: PlatformUser, other: PlatformUser) -> int:
        """Returns 1 if the user and the other user have at least one matching language,
        0 otherwise."""
        return int(
            any(
                kw.strip().lower() in other.languages.lower()
                for kw in user.languages.split(",")
            )
        )

    def get_question_score(self, user: PlatformUser, other: PlatformUser) -> int:
        """Returns the number of matching keywords in the questions of the user
        and the other user."""
        return sum(
            self.not_alnum.sub("", kw.strip().lower()) in other.questions[q_id].lower()
            for q_id in QUESTION_NAMES
            for kw in user.questions[q_id].split(" ")
        )

    def get_keywords_score(self, user: PlatformUser, other: PlatformUser) -> int:
        """Returns the number of matching keywords in the keywords of the user
        and the other user."""
        return sum(
            kw.strip().lower() in other.keywords.lower()
            for kw in user.keywords.split(",")
        )

    def get_headline_score(self, user: PlatformUser, other: PlatformUser) -> int:
        """Returns the number of matching words in the headline of the user
        and the other user."""
        return sum(
            self.not_alnum.sub("", kw.strip().lower()) in other.headline.lower()
            for kw in user.headline.split(" ")
        )

    def get_location_distance(self, user: PlatformUser, other: PlatformUser) -> int:
        """Should return the distance between the location of the user and the other user.
        For now it just returns the number of matching words in the location of the user
        and the other user.
        """
        return sum(
            self.not_alnum.sub("", kw.strip().lower()) in other.location.lower()
            for kw in user.location.split(" ")
        )

    @commands.command(name="enter")
    async def enter(self, ctx: commands.Context) -> None:
        """Registers the user."""
        if ctx.author.id not in self.users:
            user = self.register_user(ctx.author)
            await self.send_structure(user, STRUCTURES["home"])  # type: ignore
        else:
            user = self.users[ctx.author.id]
            await self.delete_last_msg_of(user)
            ok_btn = self.get_ok_button_for(user)
            view = self.get_view([ok_btn])
            user.last_msg = await ctx.send(
                SPACER + "You're already in the platform!", view=view
            )

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
        await self.send_structure(user, user.last_structure or STRUCTURES["home"])  # type: ignore

    @commands.command(name="bye")
    async def bye(self, ctx: commands.Context) -> None:
        """Deletes the user's last message."""
        if ctx.author.id not in self.users:
            return
        user = self.users[ctx.author.id]
        await self.delete_last_msg_of(user)

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message) -> None:
        user = self.users.get(msg.author.id)
        if (
            user is None
            or user.change in [*self.REACTION_FUNCTIONS, ""]
            or not user.search_filter
        ):
            return

        ok_btn = self.get_ok_button_for(user, wanted_structure="edit_profile")
        view = self.get_view([ok_btn, self.home_btn])

        await self.delete_last_msg_of(user)
        await msg.add_reaction("✅")

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

        if kw_needed:
            need_caps = change == "languages"
            evenly_spaced_kws = self.evenly_space(msg.content, need_caps)
            changed_to = evenly_spaced_kws

        if change in QUESTION_NAMES:
            changed = "answer"
            change_user.questions[change] = changed_to
        else:
            setattr(change_user, change, changed_to)

        message = f'✅ {pronome} {changed} {has_have} been changed to "{changed_to}"!'
        message += self.additional_info_with_side_effects(user)

        user.last_msg = await msg.author.send(SPACER + message, view=view)
        user.change = ""
        self.save_user(user)

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
        user = self.users[payload.user_id]
        change = user.change
        if change.startswith("search_"):
            change = change[7:]

        if user.last_msg and payload.message_id == user.last_msg.id:
            if handle_reaction := self.REACTION_FUNCTIONS.get(change):
                await handle_reaction(user, payload.emoji.name)

    async def handle_status_change(self, user: PlatformUser, emoji: str) -> None:
        if not user.search_filter:
            return  # only because of type hinting
        search = user.change.startswith("search_")
        change_user = user.search_filter if search else user
        pronome = "Your" if not search else "The filter's"

        if not (status := EMOJI_STATUS.get(emoji)):
            if emoji == "❓" and search:
                status = Status.ANY
            else:
                return
        change_user.status = status

        ok_btn = self.get_ok_button_for(user, wanted_structure="edit_profile")
        view = self.get_view([ok_btn, self.home_btn])
        dc_user = await self.client.fetch_user(user.id)

        await self.delete_last_msg_of(user)
        user.last_msg = await dc_user.send(
            SPACER
            + f"✅ {pronome} status has been changed to {emoji} ({status.value})!",
            view=view,
        )
        self.save_user(user)

    async def handle_best_match_prio_order(
        self, user: PlatformUser, emoji: str, remove: bool = False
    ) -> None:
        num = self.validate_number_reaction(emoji, user)
        if not (num and user.last_view and user.last_msg):
            return

        if remove:
            user.best_match_prio_order_new.remove(num - 1)
        else:
            user.best_match_prio_order_new.append(num - 1)

        none_selected = user.best_match_prio_order_new == []

        if remove and none_selected:
            user.last_view.remove_item(self.save_btn)
            user.added_save_btn = False
        elif not remove and not user.added_save_btn:
            user.last_view.add_item(self.save_btn)
            user.added_save_btn = True

        await user.last_msg.edit(
            content=SPACER + self.replace_placeholders(PRIORITY_MESSAGE, user),
            view=user.last_view,
        )

    async def handle_selected_user(self, user: PlatformUser, emoji: str) -> None:
        num = self.validate_number_reaction(emoji, user)
        if not num:
            return
        selected_user_id = user.results[user.page * self.page_step + num - 1]
        user.selected_user = self.users[selected_user_id]
        await self.delete_last_msg_of(user)
        await self.send_structure(user, STRUCTURES["selected_user"])  # type: ignore

    def validate_number_reaction(
        self, emoji_name: str, user: PlatformUser
    ) -> int | None:
        if emoji_name not in NUM_EMOJI:
            return None
        num = NUM_EMOJI.index(emoji_name) + 1
        if not (1 <= num <= self.page_step) or not user.last_msg:
            return None
        return num

    @commands.Cog.listener()
    async def on_raw_reaction_remove(
        self, payload: discord.RawReactionActionEvent
    ) -> None:
        user = self.users[payload.user_id]
        if not user.search_filter:
            return

        if user.last_msg and payload.message_id == user.last_msg.id:
            if user.change == "best_match_prio_order":
                await self.handle_best_match_prio_order(
                    user, payload.emoji.name, remove=True
                )

    async def delete_last_msg_of(self, user: PlatformUser) -> None:
        if user.last_msg:
            await user.last_msg.delete()
            user.last_msg = None

    def get_ok_button_for(
        self,
        user: PlatformUser,
        wanted_structure: str = "",
        default_structure: str = "home",
    ) -> DCButton:
        button: DCButton = DCButton(label="OK", style=ButtonStyle.green)
        button.callback = self.get_structure_callback(  # type: ignore
            STRUCTURES[wanted_structure]
            or user.back_to_structure
            or STRUCTURES[default_structure]
        )
        return button

    def get_view(self, buttons: Sequence[Button | DCButton]) -> DCView:
        view = DCView()
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
            await self.delete_last_msg_of(user)
        await self.client.close()

    def is_valid_date(self, date: str) -> bool:
        return (
            len(date) == 10
            and date[2] == date[5] == "."
            and date.replace(".", "").isnumeric()
        )

    def load_users(self) -> dict[int, PlatformUser]:
        return {
            int(id_str): self.load_user(id_str)
            for filename in os.listdir(self.users_path)
            if (id_str := self.valid_file_name(filename))
        }

    def valid_file_name(self, name: str) -> str:
        if name.endswith(".json") and (id_str := name[:-5]).isdecimal():
            return id_str
        return ""

    def load_user(self, id_str: str) -> PlatformUser:
        filename = f"{self.users_path}/{id_str}.json"
        with open(filename, "r", encoding="utf-8") as file:
            raw_user: dict = json.loads(file.read())
            return UserManager.load(raw_user)

    def save_user(self, user: PlatformUser) -> None:
        filename = f"{self.users_path}/{user.id}.json"
        with open(filename, "w", encoding="utf-8") as file:
            file.write(UserManager.dumps(user))

    def init_users_path(self) -> str:
        path = f"{USERS_FOLDER_PATH}/{APP_NAME}_users"
        if not os.path.exists(path):
            os.makedirs(path)
        return path


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Logic(bot))
