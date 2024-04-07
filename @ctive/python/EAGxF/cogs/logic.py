import asyncio
import datetime
import json
import os
import re
from typing import Sequence

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
    EMOJI_NUM,
    EMOJI_STATUS,
    NUM_EMOJI,
    NUM_NAME,
    PRIO_LIST_LENGTH,
    PRIORITY_MESSAGE,
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
        user = await self.client.fetch_user(user_id)
        await self.send_structure(user, STRUCTURES["home"])  # type: ignore

    def init_structures(self):
        for structure_id, structure in STRUCTURES.items():
            structure.id = structure_id
            for button in structure.buttons:
                to_structure = STRUCTURES[button.takes_to]
                if to_structure is None:
                    raise ValueError(f"Structure with id {button.takes_to} not found!")
                button.callback = self.get_structure_callback(
                    to_structure, button=button
                )

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
        self.MATCH_STEP = 10
        self.PRIO_FUNCTIONS = [
            self.get_language_score,
            self.get_question_score,
            self.get_keywords_score,
            self.get_location_distance,
            self.get_status,
            self.get_title_score,
        ]
        self.DEBUGGING = True

    def get_structure_callback(
        self, structure: Structure, button: Button | None = None
    ):
        async def callback(interaction: discord.Interaction):
            await interaction.response.defer()
            if button:
                await self.affect(button, interaction.user)
            await self.send_structure(interaction.user, structure)

        return callback

    async def affect(self, button: Button, dc_user: discord.User | discord.Member):
        user = self.users[dc_user.id]
        if button.effect == "best_matches_prev_page":
            user.matches_from -= self.MATCH_STEP
            user.matches_to -= self.MATCH_STEP
        if button.effect == "best_matches_next_page":
            user.matches_from += self.MATCH_STEP
            user.matches_to += self.MATCH_STEP
        if button.effect in [
            "reload_message",
            "cancel_change_prio",
            "save_prio",
        ]:
            await self.delete_last_msg_of(user)
            if button.effect == "save_prio":
                user.best_match_prio_order = user.best_match_prio_order_new
                self.save_user(user)
            user.best_match_prio_order_new = []
        if button.effect == "default_best_matches":
            user.best_match_prio_order = list(range(PRIO_LIST_LENGTH))
            self.save_user(user)

    async def send_structure(
        self, dc_user: discord.User | discord.Member, structure: Structure
    ):
        user = self.users[dc_user.id]
        user.back_to_structure = user.last_structure

        if structure.id in ["search", "show_results"]:
            user.found_users = self.search_users_for(user)

        if structure.condition and not self.condition_true_for(
            structure.condition, user
        ):
            ok_btn = self.get_ok_button_for(user)
            view = self.get_view([ok_btn])
            message = self.get_condition_message(structure.condition)
            reactions = False
        else:
            buttons = [
                button
                for button in structure.buttons
                if self.btn_condition_true_for(button.condition, user)
            ]
            view = self.get_view(buttons)
            message = self.replace_placeholders(structure.message, dc_user.id)
            reactions = True
        user.last_view = view

        if user.last_msg:
            await user.last_msg.edit(content=SPACER + message, view=view)
        else:
            user.last_msg = await dc_user.send(SPACER + message, view=view)
        user.last_structure = structure

        if structure.changes_property:
            user.change = structure.changes_property

        if reactions and structure.reactions:
            for emoji in structure.reactions:
                await user.last_msg.add_reaction(emoji)

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
            questions={
                "need_help": "?",
                "can_help": "?",
            },
            search_filter=PlatformUser(
                questions={"need_help": "?", "can_help": "?"},
                status=Status.ANY,
            ),
            best_match_prio_order=list(range(PRIO_LIST_LENGTH)),
        )
        self.save_user(user)

    def search_users_for(self, search_user: PlatformUser) -> list[int]:
        if not search_user.search_filter:
            return []
        return [
            user.id
            for user in self.users.values()
            if (
                search_user.search_filter.name.lower() in user.name.lower()
                or search_user.search_filter.name == "?"
            )
            and (
                search_user.search_filter.title.lower() in user.title.lower()
                or search_user.search_filter.title == "?"
            )
            and (
                search_user.search_filter.location.lower() in user.location.lower()
                or search_user.search_filter.location == "?"
            )
            and self.comma_and_search(
                user.languages, search_user.search_filter.languages
            )
            and self.comma_and_search(user.keywords, search_user.search_filter.keywords)
            and (
                user.status != Status.INVISIBLE
                and (
                    search_user.search_filter.status == user.status
                    or search_user.search_filter.status == Status.ANY
                )
            )
            and self.comma_and_search(
                user.questions["need_help"],
                search_user.search_filter.questions["need_help"],
            )
            and self.comma_and_search(
                user.questions["can_help"],
                search_user.search_filter.questions["can_help"],
            )
        ]

    def condition_true_for(self, condition: str, user: PlatformUser) -> bool:
        if condition == "profile_complete":
            basic_filled = all(
                getattr(user, attr) not in ["?", ""]
                for attr in ["name", "title", "location", "languages", "keywords"]
            )
            questions_filled = all(
                user.questions[question] not in ["?", ""]
                for question in ["need_help", "can_help"]
            )
            return basic_filled and questions_filled
        return False

    def get_condition_message(self, condition: str) -> str:
        if condition == "profile_complete":
            return (
                "*Your profile must be complete before you can "
                "change your status ;-)*"
                "\n*Fill out all details and try again!*"
            )
        return ""

    def check_conditions(self, user: PlatformUser) -> str:
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

    def btn_condition_true_for(self, condition: str, user: PlatformUser) -> bool:
        if not condition:
            return True
        if condition == "has_previous":
            return user.matches_from > 1
        elif condition == "has_next":
            return user.matches_to < len(user.best_matches)
        elif condition == "prio_order_full":
            return len(user.best_match_prio_order_new) == PRIO_LIST_LENGTH
        elif condition == "prio_order_at_least_one":
            return bool(user.best_match_prio_order_new)
        return False

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
            .replace("<number_of_results>", str(len(user.found_users)))
            .replace("<search_results>", self.get_results_for(user))
            .replace("<best_matches>", self.get_best_matches_for(user))
            .replace("<matches_from>", str(user.matches_from))
            .replace("<matches_to>", str(user.matches_to))
            .replace(
                "<best_match_prio_order_new>",
                self.format_priority_order(user, new=True),
            )
            .replace("<best_match_prio_order>", self.format_priority_order(user))
            .replace("<total_matches>", str(len(user.best_matches)))
        )
        if user.search_filter:
            message = (
                message.replace("<search_name>", user.search_filter.name)
                .replace("<search_title>", user.search_filter.title)
                .replace("<search_location>", user.search_filter.location)
                .replace("<search_languages>", user.search_filter.languages)
                .replace("<search_keywords>", user.search_filter.keywords)
                .replace(
                    "<search_status>",
                    (
                        "?"
                        if user.search_filter.status == Status.ANY
                        else f"{STATUS_EMOJI[user.search_filter.status]} "
                        f"({user.search_filter.status.value})"
                    ),
                )
                .replace(
                    "<search_need_help>", user.search_filter.questions["need_help"]
                )
                .replace("<search_can_help>", user.search_filter.questions["can_help"])
            )
        return message

    def get_results_for(self, user: PlatformUser) -> str:
        separator = "***========================***\n"
        return separator + f"\n\n{separator}".join(
            f"{self.to_emojis(i+1)} .: ***{u.name}*** :. "
            f"(Status: {STATUS_EMOJI[u.status]} "
            f"({u.status.value}))"
            f"\n- *Title:* {u.title}"
            f"\n- *Location:* {u.location}"
            f"\n- *Languages:* {u.languages}"
            f"\n- *Keywords:* {u.keywords}"
            "\n***------❓Questions ------***"
            f"\n- *Need Help:* {u.questions['need_help']}"
            f"\n- *Can Help:* {u.questions['can_help']}"
            for i, u in enumerate(map(lambda x: self.users[x], user.found_users))
        )

    def get_score_summary(self, user: PlatformUser, other: PlatformUser) -> str:
        """Returns a summary of the scores of the user and the other user."""
        return (
            f"(Lang: {self.get_language_score(user, other)}) "
            f"(Q: {self.get_question_score(user, other)}) "
            f"(Kw: {self.get_keywords_score(user, other)}) "
            f"(Title: {self.get_title_score(user, other)}) "
            f"(Loc: {self.get_location_distance(user, other)}) "
        )

    def to_emojis(self, number: int) -> str:
        """Converts a number to emojis. E.g. 123 -> ":one::two::three:"""
        return "".join(f":{NUM_NAME[int(n)]}:" for n in str(number))

    def get_best_matches_for(self, user: PlatformUser) -> str:
        """A list of the best matches for the user.
        Matches get sorted by multiple criteria.
        1. number of matching keywords in
            - languages
            - questions (in the opposite, so need_help for can_help and vice versa)
            - keywords
        2. Location distance
        3. Status
        4. number of matching words in title
        """
        if not user.best_matches:
            matches = self.users.copy()
            matches.pop(user.id)
            matches_list = sorted(
                matches.values(),
                key=lambda u: self.get_priority(user, u),
                reverse=True,
            )
            user.best_matches = [u.id for u in matches_list]
            user.matches_to = min(self.MATCH_STEP, len(user.best_matches))
        return "\n".join(
            f"{self.to_emojis(i+1)} .: ***{u.name}*** :. "
            f"(Status: {STATUS_EMOJI[u.status]} "
            f"({u.status.value}))"
            f"\n[SCORE:  {self.get_score_summary(user, u)}]"
            f"\n- *Title:* {u.title}"
            f"\n- *Location:* {u.location}"
            f"\n- *Languages:* {u.languages}"
            f"\n- *Keywords:* {u.keywords}"
            "\n***------❓Questions ------***"
            f"\n- *Need Help:* {u.questions['need_help']}"
            f"\n- *Can Help:* {u.questions['can_help']}"
            for i, u in enumerate(
                map(
                    lambda x: self.users[x],
                    user.best_matches[user.matches_from - 1 : user.matches_to],
                )
            )
        )

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
        """Returns 1 if the user and the other user have at least one matching language, 0 otherwise."""
        return int(
            any(
                kw.strip().lower() in other.languages.lower()
                for kw in user.languages.split(",")
            )
        )

    def get_question_score(self, user: PlatformUser, other: PlatformUser) -> int:
        """Returns the number of matching keywords in the questions of the user and the other user."""
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
        """Returns the number of matching keywords in the keywords of the user and the other user."""
        return sum(
            kw.strip().lower() in other.keywords.lower()
            for kw in user.keywords.split(",")
        )

    def get_title_score(self, user: PlatformUser, other: PlatformUser) -> int:
        """Returns the number of matching words in the title of the user and the other user."""
        return sum(
            self.not_alnum.sub("", kw.strip().lower()) in other.title.lower()
            for kw in user.title.split(" ")
        )

    def get_location_distance(self, user: PlatformUser, other: PlatformUser) -> int:
        """Should return the distance between the location of the user and the other user.
        For now it just returns the number of matching words in the location of the user and the other user.
        """
        return sum(
            self.not_alnum.sub("", kw.strip().lower()) in other.location.lower()
            for kw in user.location.split(" ")
        )

    def comma_and_search(self, a: str, b: str) -> bool:
        """Returns True if... for God's sake, just read the code!"""
        return (
            any(
                all(kw.strip().lower() in a.lower() for kw in block.split("&"))
                for block in b.split(", ")
            )
            or b == "?"
        )

    @commands.command(name="enter")
    async def enter(self, ctx: commands.Context):
        """Registers the user."""
        if ctx.author.id not in self.users:
            self.register_user(ctx.author)
            await self.send_structure(ctx.author, STRUCTURES["home"])  # type: ignore
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
        if ctx.author.id not in ADMINS:
            print(f"Unauthorized user ({ctx.author}) tried to stop the bot.")
            return
        for user in self.users.values():
            await self.delete_last_msg_of(user)
        await self.client.close()

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
        await self.send_structure(ctx.author, user.last_structure or STRUCTURES["home"])  # type: ignore

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
        message += self.check_conditions(user)

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
                user.change = ""
                self.save_user(user)
            if change == "best_match_prio_order":
                await self.handle_best_match_prio_order(user, payload.emoji)

    async def handle_best_match_prio_order(
        self, user: PlatformUser, emoji: discord.PartialEmoji, remove: bool = False
    ):
        num = EMOJI_NUM.get(str(emoji.name))
        if not num or not (1 <= num <= PRIO_LIST_LENGTH) or not user.last_msg:
            return

        if remove:
            user.best_match_prio_order_new.remove(num - 1)
        else:
            user.best_match_prio_order_new.append(num - 1)

        atleast1 = self.btn_condition_true_for("prio_order_at_least_one", user)
        if user.last_view:
            if not atleast1 and remove and user.save_btn:
                user.last_view.remove_item(user.save_btn)
                user.save_btn = None
            elif atleast1 and not remove and not user.save_btn:
                user.last_view.add_item(self.save_btn)
                user.save_btn = self.save_btn

        await user.last_msg.edit(
            content=SPACER
            + PRIORITY_MESSAGE.replace(
                "<best_match_prio_order_new>",
                self.format_priority_order(user, new=True),
            ).replace("<best_match_prio_order>", self.format_priority_order(user)),
            view=user.last_view,
        )

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
        if interaction.user.id not in ADMINS:
            print(f"Unauthorized user ({interaction.user}) tried to stop the bot.")
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
        # curdir = __file__.replace("\\", "/")
        # path = "/".join(curdir.split("/")[:-6]) + "/eagxf_users"
        path = f"{USERS_FOLDER_PATH}/{APP_NAME}_users"
        if not os.path.exists(path):
            os.makedirs(path)
        return path


async def setup(bot: commands.Bot):
    await bot.add_cog(Logic(bot))
