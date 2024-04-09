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
    SPACER,
    STATUS_EMOJI,
    STRUCTURES,
    USERS_FOLDER_PATH,
)
from eagxf.date import Date
from eagxf.platform_user import PlatformUser
from eagxf.status import Status
from eagxf.structure import Structure
from eagxf.user_saver import UserSaver


class Logic(commands.Cog):
    def __init__(self, client: discord.Client) -> None:
        self.client = client
        self.users_path = self.init_users_path()
        self.users: dict[int, PlatformUser] = self.load_users()
        for user_id in self.users:
            asyncio.create_task(self.send_starting_message_to(user_id))
        self.init_structures()
        self.init_other_stuff()

    async def send_starting_message_to(self, user_id: int):
        user = self.users[user_id]
        await self.send_structure(user, STRUCTURES["home"])  # type: ignore

    def init_structures(self):
        for structure_id, structure in STRUCTURES.items():
            structure.id = structure_id
            if structure.paged:
                structure.after_button_effects = self.comma_add(
                    structure.after_button_effects, "delete_message, empty_results"
                )
            for button in structure.buttons:
                to_structure = STRUCTURES[button.takes_to]
                if to_structure is None:
                    raise ValueError(f"Structure with id {button.takes_to} not found!")
                button.callback = self.get_structure_callback(
                    to_structure, button=button
                )
                if structure.after_button_effects:
                    button.effects = self.comma_add(
                        button.effects, structure.after_button_effects
                    )

    def comma_add(self, original: str, additional: str) -> str:
        if original:
            return f"{original}, {additional}"
        return additional

    def init_other_stuff(self) -> None:
        self.home_btn: DCButton = DCButton(label="🏠 Home", style=ButtonStyle.primary)
        self.home_btn.callback = self.get_structure_callback(STRUCTURES["home"])  # type: ignore
        self.save_btn = Button(
            label="💾 Save",
            takes_to="best_matches",
            effect="save_prio",
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
            self.get_title_score,
        ]
        self.DEBUGGING = True  # pylint: disable=C0103
        self.page_step = 10

    def get_structure_callback(
        self, structure: Structure, button: Button | None = None
    ):
        async def callback(interaction: discord.Interaction):
            await interaction.response.defer()
            user = self.users[interaction.user.id]
            if button and button.effects:
                for effect in button.effects.split(", "):
                    await self.affect(effect, user)
            await self.send_structure(user, structure)

        return callback

    async def affect(self, effect: str, user: PlatformUser):
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

    async def send_structure(self, user: PlatformUser, structure: Structure):
        user.back_to_structure = user.last_structure

        self.collect_data_for(user, structure)

        if structure.condition and not self.condition_true_for(
            structure.condition, user
        ):
            ok_btn = self.get_ok_button_for(user)
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
            message = self.replace_placeholders(structure.message, user.id)
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

    def collect_data_for(self, user: PlatformUser, structure: Structure):
        if not structure.paged:
            return
        if structure.id in ["search", "show_search_results"]:
            user.results = self.search_users_for(user)
        if structure.id == "best_matches":
            user.results = self.search_best_matches_for(user)
        if structure.id == "interests_sent":
            pass
        if structure.id == "interests_received":
            pass

    def search_best_matches_for(self, user: PlatformUser) -> list[int]:
        matches = self.users.copy()
        matches.pop(user.id)
        matches_list = sorted(
            matches.values(),
            key=lambda u: self.get_priority(user, u),
            reverse=True,
        )
        return [u.id for u in matches_list]

    def register_user(self, dc_user: discord.User | discord.Member):
        current = datetime.datetime.now()
        user = self.users[dc_user.id] = PlatformUser(
            id=dc_user.id,
            date_joined=Date(
                day=current.day,
                month=current.month,
                year=current.year,
            ),
            name=dc_user.name,
            questions={"need_help": "?", "can_help": "?"},
            search_filter=PlatformUser(
                questions={"need_help": "?", "can_help": "?"},
                status=Status.ANY,
            ),
            best_match_prio_order=list(range(PRIO_LIST_LENGTH)),
            interests={"sent": [], "received": []},
        )
        self.save_user(user)
        return user

    async def add_special_reactions_for(self, user: PlatformUser, structure: Structure):
        if structure.paged and user.last_msg:
            for i in range(min(self.page_step, len(user.results))):
                await user.last_msg.add_reaction(NUM_EMOJI[i])

    def search_users_for(self, search_user: PlatformUser) -> list[int]:
        if not search_user.search_filter:
            return []
        return [
            user.id
            for user in self.users.values()
            if user.search_applicable_for(search_user)
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
                "\n\n*( Your profile is incomplete, so your status has been "
                "changed to invisible! )*"
            )
        return ""

    def btn_condition_true_for(self, user: PlatformUser, condition: str) -> bool:
        if not condition:
            return True
        if condition == "has_previous_page":
            return user.page > 0
        elif condition == "has_next_page":
            return user.page < len(user.results) // self.page_step - 1
        elif condition == "prio_order_full":
            return len(user.best_match_prio_order_new) == PRIO_LIST_LENGTH
        elif condition == "prio_order_at_least_one":
            return bool(user.best_match_prio_order_new)
        raise ValueError(f"Invalid condition: {condition}")

    def replace_placeholders(self, message: str, user_id: int) -> str:
        user = self.users[user_id]
        message = (
            message.replace("<id>", str(user.id))
            .replace("<date_joined>", str(user.date_joined))
            .replace("<name>", user.name)
            .replace("<title>", user.title)
            .replace("<location>", user.location)
            .replace("<languages>", user.languages)
            .replace("<need_help>", user.questions["need_help"])
            .replace("<can_help>", user.questions["can_help"])
            .replace("<keywords>", user.keywords)
            .replace("<status>", f"{STATUS_EMOJI[user.status]} ({user.status.value})")
            .replace("<number_of_results>", str(len(user.results)))
            .replace("<search_results>", self.get_formatted_results_for(user))
            .replace(
                "<best_matches>",
                self.get_formatted_results_for(user, self.get_score_summary(user)),
            )
            .replace("<page_reference>", self.get_page_reference_for(user))
            .replace(
                "<best_match_prio_order_new>",
                self.format_priority_order(user, new=True),
            )
            .replace("<best_match_prio_order>", self.format_priority_order(user))
        )
        if user.search_filter:
            message = (
                message.replace("<search_name>", user.search_filter.name)
                .replace("<search_title>", user.search_filter.title)
                .replace("<search_location>", user.search_filter.location)
                .replace("<search_languages>", user.search_filter.languages)
                .replace("<search_keywords>", user.search_filter.keywords)
                .replace("<search_status>", self.get_search_status(user.search_filter))
                .replace(
                    "<search_need_help>", user.search_filter.questions["need_help"]
                )
                .replace("<search_can_help>", user.search_filter.questions["can_help"])
            )
        return message

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
            f"\n- *Title:* {u.title}"
            f"\n- *Location:* {u.location}"
            f"\n- *Languages:* {u.languages}"
            f"\n- *Keywords:* {u.keywords}"
            "\n***------❓Questions ------***"
            f"\n- *Need Help:* {u.questions['need_help']}"
            f"\n- *Can Help:* {u.questions['can_help']}"
            for i, u in enumerate(self.get_results_for(user, user.results))
        )

    def get_results_for(self, user: PlatformUser, results: list[int]):
        return self.convert_users(self.paged_list_of(results, user))

    def get_score_summary(self, user: PlatformUser) -> Callable[[PlatformUser], str]:
        """Returns a summary of the scores of the user and the other user."""
        return lambda other: (
            f"\n[SCORE: "
            f"(Lang: {self.get_language_score(user, other)}) "
            f"(Q: {self.get_question_score(user, other)}) "
            f"(Kw: {self.get_keywords_score(user, other)}) "
            f"(Title: {self.get_title_score(user, other)}) "
            f"(Loc: {self.get_location_distance(user, other)}) "
            "]"
        )

    def to_emojis(self, number: int) -> str:
        """Converts a number to emojis. E.g. 123 -> ":one::two::three:"""
        return "".join(f":{NUM_NAME[int(n)]}:" for n in str(number))

    def paged_list_of(self, lst: list, user: PlatformUser):
        return lst[user.page * self.page_step : (user.page + 1) * self.page_step]

    def convert_users(self, user_ids: list[int]) -> Iterator[PlatformUser]:
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
            self.not_alnum.sub("", kw.strip().lower())
            in other.questions["need_help"].lower()
            for kw in user.questions["can_help"].split(" ")
        ) + sum(
            self.not_alnum.sub("", kw.strip().lower())
            in other.questions["can_help"].lower()
            for kw in user.questions["need_help"].split(" ")
        )

    def get_keywords_score(self, user: PlatformUser, other: PlatformUser) -> int:
        """Returns the number of matching keywords in the keywords of the user
        and the other user."""
        return sum(
            kw.strip().lower() in other.keywords.lower()
            for kw in user.keywords.split(",")
        )

    def get_title_score(self, user: PlatformUser, other: PlatformUser) -> int:
        """Returns the number of matching words in the title of the user
        and the other user."""
        return sum(
            self.not_alnum.sub("", kw.strip().lower()) in other.title.lower()
            for kw in user.title.split(" ")
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
    async def enter(self, ctx: commands.Context):
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
    async def stop(self, ctx: commands.Context):
        """Stops the bot."""
        await self.stop_request_by(ctx.author.id)

    @commands.command(name="reset")
    async def reset(self, ctx: commands.Context):
        """Resets the bot."""
        await self.hi(ctx)

    @commands.command(name="hi")
    async def hi(self, ctx: commands.Context):
        """Sends the user's home structure."""
        if ctx.author.id not in self.users:
            return
        await self.bye(ctx)
        user = self.users[ctx.author.id]
        user.best_match_prio_order_new = []
        await self.send_structure(user, user.last_structure or STRUCTURES["home"])  # type: ignore

    @commands.command(name="bye")
    async def bye(self, ctx: commands.Context):
        """Deletes the user's last message."""
        if ctx.author.id not in self.users:
            return
        user = self.users[ctx.author.id]
        await self.delete_last_msg_of(user)

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        user = self.users.get(msg.author.id)
        if (
            user is None
            or user.change
            in [
                "best_match_prio_order",
                "status",
                "",
            ]
            or not user.search_filter
        ):
            return

        ok_btn = self.get_ok_button_for(user, default_structure="edit_profile")
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
        kw_needed = plural or search and change in ["need_help", "can_help"]
        has_have = "have" if plural else "has"
        changed_to = msg.content

        if kw_needed:
            evenly_spaced_kws = ", ".join(
                " & ".join(
                    w.capitalize() if change == "languages" else w
                    for w in map(str.strip, kw.split("&"))
                )
                for kw in map(str.strip, msg.content.split(","))
            )
            changed_to = evenly_spaced_kws

        if change in ["need_help", "can_help"]:
            changed = "answer"
            change_user.questions[change] = changed_to
        else:
            setattr(change_user, change, changed_to)

        message = f'✅ {pronome} {changed} {has_have} been changed to "{changed_to}"!'
        message += self.additional_info_with_side_effects(user)

        user.last_msg = await msg.author.send(SPACER + message, view=view)
        user.change = ""
        self.save_user(user)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        user = self.users[payload.user_id]
        if not user.search_filter:
            return

        ok_btn = self.get_ok_button_for(user, default_structure="edit_profile")
        view = self.get_view([ok_btn, self.home_btn])

        search = user.change.startswith("search_")
        pronome = "Your" if not search else "The filter's"
        change = user.change
        change_user = user.search_filter if search else user
        if search:
            change = user.change[7:]

        if user.last_msg and payload.message_id == user.last_msg.id:
            if change == "status":
                emoji = str(payload.emoji)
                if not (status := EMOJI_STATUS.get(emoji)):
                    if emoji == "❓" and search:
                        status = Status.ANY
                    else:
                        return
                change_user.status = status
                await self.delete_last_msg_of(user)
                dc_user = await self.client.fetch_user(user.id)
                user.last_msg = await dc_user.send(
                    SPACER
                    + f"✅ {pronome} status has been changed to {emoji} ({status.value})!",
                    view=view,
                )
                self.save_user(user)
            if change == "best_match_prio_order":
                await self.handle_best_match_prio_order(user, payload.emoji)

    async def handle_best_match_prio_order(
        self, user: PlatformUser, emoji: discord.PartialEmoji, remove: bool = False
    ):
        if emoji.name not in NUM_EMOJI:
            return
        num = NUM_EMOJI.index(emoji.name) + 1
        if not (1 <= num <= PRIO_LIST_LENGTH) or not user.last_msg:
            return

        if remove:
            user.best_match_prio_order_new.remove(num - 1)
        else:
            user.best_match_prio_order_new.append(num - 1)

        atleast1 = self.btn_condition_true_for(user, "prio_order_at_least_one")
        if user.last_view:
            if not atleast1 and remove:
                user.show_save_btn = False
                user.last_view.remove_item(self.save_btn)
            elif not remove and not user.show_save_btn:
                user.show_save_btn = True
                user.last_view.add_item(self.save_btn)

        await self.send_structure(user, STRUCTURES["change_priority"])  # type: ignore

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        user = self.users[payload.user_id]
        if not user.search_filter:
            return

        if user.last_msg and payload.message_id == user.last_msg.id:
            if user.change == "best_match_prio_order":
                await self.handle_best_match_prio_order(
                    user, payload.emoji, remove=True
                )

    async def delete_last_msg_of(self, user: PlatformUser):
        if user.last_msg:
            await user.last_msg.delete()
            user.last_msg = None

    def get_ok_button_for(
        self, user: PlatformUser, default_structure: str = "home"
    ) -> DCButton:
        button: DCButton = DCButton(label="OK", style=ButtonStyle.green)
        button.callback = self.get_structure_callback(  # type: ignore
            user.back_to_structure or STRUCTURES[default_structure]
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

    async def stop_callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        await self.stop_request_by(interaction.user.id)

    async def stop_request_by(self, user_id: int):
        if user_id not in ADMINS:
            print(f"Unauthorized user (id: {user_id}) tried to stop the bot.")
            return
        for user in self.users.values():
            await self.delete_last_msg_of(user)
        await self.client.close()

    def is_valid_date(self, date: str):
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
        if name.endswith(".txt") and (id_str := name[:-4]).isdecimal():
            return id_str
        return ""

    def load_user(self, id_str: str) -> PlatformUser:
        filename = f"{self.users_path}/{id_str}.txt"
        with open(filename, "r", encoding="utf-8") as file:
            raw_user: dict = json.loads(file.read())
            return UserSaver.load(raw_user)

    def save_user(self, user: PlatformUser):
        filename = f"{self.users_path}/{user.id}.txt"
        with open(filename, "w", encoding="utf-8") as file:
            file.write(UserSaver.dumps(user))

    def init_users_path(self) -> str:
        path = f"{USERS_FOLDER_PATH}/{APP_NAME}_users"
        if not os.path.exists(path):
            os.makedirs(path)
        return path


async def setup(bot: commands.Bot):
    await bot.add_cog(Logic(bot))
