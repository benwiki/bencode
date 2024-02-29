import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import asyncio
import datetime
import json

import discord
from discord import ButtonStyle
from discord.ext import commands
from discord.ui import Button as DCButton
from discord.ui import View as DCView
from eagxf.constants import ADMINS, EMOJI_STATUS, SPACER, STATUS_EMOJI, STRUCTURES
from eagxf.date import Date
from eagxf.platform_user import PlatformUser
from eagxf.status import Status
from eagxf.structure import Structure
from eagxf.user_saver import UserSaver


class Logic(commands.Cog):
    start_view = DCView()

    def __init__(self, client: discord.Client) -> None:
        self.client = client
        self.channel = None
        self.users: dict[int, PlatformUser] = self.load_users()
        for user_id in self.users:
            asyncio.create_task(self.send_starting_message_to(user_id))
        self.init_structures()
        self.init_other_stuff()

    def get_file_path(self):
        curdir = __file__.replace("\\", "/")
        return "/".join(curdir.split("/")[:-6])

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
                button.callback = self.get_structure_callback(to_structure)

    def init_other_stuff(self) -> None:
        self.home_btn: DCButton = DCButton(label="🏠 Home", style=ButtonStyle.primary)
        self.home_btn.callback = self.get_structure_callback(STRUCTURES["home"])  # type: ignore

    def get_structure_callback(self, structure: Structure):
        async def callback(interaction: discord.Interaction):
            await interaction.response.defer()
            await self.send_structure(interaction.user, structure)

        return callback

    async def send_structure(
        self, dc_user: discord.User | discord.Member, structure: Structure
    ):
        user = self.register_user(dc_user)
        user.back_to_structure = user.last_structure
        await self.delete_entry_msg_of(user)

        if structure.id in ["search", "show_results"]:
            user.found_users = self.search_users_for(user)

        view = DCView()
        for button in structure.buttons:
            if button.condition:
                if not self.condition_true_for(button.condition, user):
                    continue
            view.add_item(button)

        message = self.replace_placeholders(structure.message, dc_user.id)
        if user.last_message:
            await user.last_message.edit(content=SPACER + message, view=view)
        else:
            user.last_message = await dc_user.send(SPACER + message, view=view)
        user.last_structure = structure

        if structure.changes_property:
            user.change = structure.changes_property

        if structure.reactions:
            for emoji in structure.reactions:
                await user.last_message.add_reaction(emoji)
        self.save_users()

    def register_user(self, user: discord.User | discord.Member):
        if user.id not in self.users:
            current = datetime.datetime.now()
            self.users[user.id] = PlatformUser(
                id=user.id,
                date_joined=Date(
                    day=current.day,
                    month=current.month,
                    year=current.year,
                ),
                name=user.name,
                questions={
                    "need_help": "?",
                    "can_help": "?",
                },
                search_filter=PlatformUser(
                    questions={"need_help": "?", "can_help": "?"},
                    status=Status.ANY,
                ),
            )
        return self.users[user.id]

    def search_users_for(self, search_user: PlatformUser) -> list[int]:
        if not search_user.search_filter:
            return []
        return [
            user.id for user in self.users.values()
            if (search_user.search_filter.name.lower() in user.name.lower()
                or search_user.search_filter.name == "?")
            and (search_user.search_filter.title.lower() in user.title.lower()
                or search_user.search_filter.title == "?")
            and (search_user.search_filter.location.lower() in user.location.lower()
                or search_user.search_filter.location == "?")
            and self.comma_and_search(
                user.languages,
                search_user.search_filter.languages)
            and self.comma_and_search(
                user.keywords,
                search_user.search_filter.keywords)
            and (user.status != Status.INVISIBLE and
                 (search_user.search_filter.status == user.status
                 or search_user.search_filter.status == Status.ANY))
            and self.comma_and_search(
                user.questions["need_help"],
                search_user.search_filter.questions["need_help"])
            and self.comma_and_search(
                user.questions["can_help"],
                search_user.search_filter.questions["can_help"])
        ]

    def condition_true_for(self, condition: str, user: PlatformUser) -> bool:
        if condition == "profile_complete":
            basic_filled = all(
                getattr(user, attr) not in ["?", ""]
                for attr in
                ["name", "title", "location", "languages", "keywords"]
            )
            questions_filled = all(
                user.questions[question] not in ["?", ""]
                for question in ["need_help", "can_help"]
            )
            return basic_filled and questions_filled
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
            .replace("<conditional_status_warning>",
                ("" if self.condition_true_for("profile_complete", user) else
                "\n\n*( Can't find the button to change your status?*"
                "\n*Your profile must be complete before you can do that ;-)*"
                "\n*Fill out the other details and the button will appear! )*"))
        )
        if user.search_filter:
            message = (
                message.replace("<search_name>", user.search_filter.name)
                .replace("<search_title>", user.search_filter.title)
                .replace("<search_location>", user.search_filter.location)
                .replace("<search_languages>", user.search_filter.languages)
                .replace("<search_keywords>", user.search_filter.keywords)
                .replace("<search_status>",
                         "?" if user.search_filter.status == Status.ANY else
                         f"{STATUS_EMOJI[user.search_filter.status]} "
                         "({user.search_filter.status.value})")
                .replace("<search_need_help>",
                         user.search_filter.questions["need_help"])
                .replace("<search_can_help>",
                         user.search_filter.questions["can_help"])
            )
        return message

    def get_results_for(self, user: PlatformUser) -> str:
        separator = "***========================***\n"
        return separator + f"\n\n{separator}".join(
            f"{i+1}.:  ***{u.name}***  (Status: {STATUS_EMOJI[u.status]} "
            f"({u.status.value}))"
            f"\n- *Title:* {u.title}"
            f"\n- *Location:* {u.location}"
            f"\n- *Languages:* {u.languages}"
            f"\n- *Keywords:* {u.keywords}"
            "\n\n❓**Questions**"
            f"\n- *Need Help:* {u.questions['need_help']}"
            f"\n- *Can Help:* {u.questions['can_help']}"
            for i, u in enumerate(map(
                lambda x: self.users[x],
                user.found_users
            ))
        )

    def comma_and_search(self, a: str, b: str) -> bool:
        return any(all(kw.strip().lower() in a.lower()
                       for kw in block.split("&"))
                   for block in b.split(", ")) or b == "?"

    @commands.command(name="enter")
    async def enter(self, ctx: commands.Context):
        """Gives you the starting button."""
        user = self.register_user(ctx.author)
        if user.enter_message:
            await user.enter_message.delete()

        view = DCView()
        button: DCButton = DCButton(label="Enter Platform", style=ButtonStyle.primary)
        view.add_item(button)
        button.callback = self.get_structure_callback(STRUCTURES["home"])  # type: ignore
        user.enter_message = await ctx.send(
            "Hello! If you click the button, the bot will DM you"
            " and you enter the platform!",
            view=view,
        )

    @commands.command(name="stop")
    async def stop(self, ctx: commands.Context):
        """Stops the bot."""
        if ctx.author.id not in ADMINS:
            print(f"Unauthorized user ({ctx.author}) tried to stop the bot.")
            return
        for user in self.users.values():
            await self.delete_entry_msg_of(user)
            await self.delete_last_msg_of(user)
        await self.client.close()

    @commands.command(name="reset")
    async def reset(self, ctx: commands.Context):
        await self.hi(ctx)

    @commands.command(name="hi")
    async def hi(self, ctx: commands.Context):
        user = await self.bye(ctx)
        await self.send_structure(
            ctx.author,
            user.last_structure or STRUCTURES["home"])  # type: ignore

    @commands.command(name="bye")
    async def bye(self, ctx: commands.Context) -> PlatformUser:
        if ctx.author.id not in self.users:
            return
        user = self.users[ctx.author.id]
        await self.delete_entry_msg_of(user)
        await self.delete_last_msg_of(user)
        return user

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        user = self.users.get(msg.author.id)
        if user is None or user.change in ["status", ""] or not user.search_filter:
            return

        view = DCView()
        ok_btn: DCButton = DCButton(label="OK", style=ButtonStyle.green)
        ok_structure = user.back_to_structure or STRUCTURES["edit_profile"]
        ok_btn.callback = self.get_structure_callback(ok_structure)  # type: ignore
        view.add_item(ok_btn)
        view.add_item(self.home_btn)

        await self.delete_entry_msg_of(user)
        await self.delete_last_msg_of(user)
        await msg.add_reaction("✅")

        changed = change = user.change
        search = change.startswith("search_")
        if search:  # chop off the "search_" prefix
            change = changed = change[7:]

        change_user = user.search_filter if search else user
        pronome = "Your" if not search else "The filter's"
        kw_needed = (
            change in ["keywords", "languages"]
            or search and change in ["need_help", "can_help"]
        )
        changed_to = msg.content

        if kw_needed:
            kws = [
                kw.strip().capitalize()
                    if change == "languages" else
                kw.strip()
                for kw in msg.content.split(",")]
            kws = [" & ".join(w.strip() for w in kw.split('&')) for kw in kws]
            evenly_spaced_kws = ", ".join(kws)
            changed_to = evenly_spaced_kws
            print(changed_to)

        if change in ["need_help", "can_help"]:
            changed = "answer"
            change_user.questions[change] = changed_to
        else:
            setattr(change_user, change, changed_to)

        message = f'✅ {pronome} {changed} have been changed to "{changed_to}"!'
        user.last_message = await msg.author.send(SPACER + message, view=view)
        user.change = ""
        self.save_users()

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        user = self.users[payload.user_id]
        if not user.search_filter:
            return

        view = DCView()
        ok_btn: DCButton = DCButton(label="OK", style=ButtonStyle.green)
        view.add_item(ok_btn)
        ok_structure = user.back_to_structure or STRUCTURES["edit_profile"]
        ok_btn.callback = self.get_structure_callback(ok_structure)  # type: ignore
        view.add_item(self.home_btn)

        search = user.change.startswith("search_")
        pronome = "Your" if not search else "The filter's"
        change = user.change
        change_user = user.search_filter if search else user
        if search:
            change = user.change[7:]

        if user.last_message and payload.message_id == user.last_message.id:
            if change == "status":
                emoji = str(payload.emoji)
                if not (status := EMOJI_STATUS.get(emoji)):
                    if emoji == "❓" and search:
                        status = Status.ANY
                    else: return
                change_user.status = status
                await self.delete_entry_msg_of(user)
                await self.delete_last_msg_of(user)
                dc_user = await self.client.fetch_user(user.id)
                user.last_message = await dc_user.send(
                    SPACER + f"✅ {pronome} status has been changed to {emoji} ({status.value})!",
                    view=view,
                )
                user.change = ""
                self.save_users()

    async def delete_last_msg_of(self, user: PlatformUser):
        if user.last_message:
            await user.last_message.delete()
            user.last_message = None

    async def delete_entry_msg_of(self, user: PlatformUser):
        if user.enter_message:
            await user.enter_message.delete()
            user.enter_message = None

    def is_valid_date(self, date: str):
        return (
            len(date) == 10
            and date[2] == date[5] == "."
            and date.replace(".", "").isnumeric()
        )

    def load_users(self) -> dict[int, PlatformUser]:
        path = self.get_file_path()
        try:
            with open(f"{path}/users.txt", "r", encoding="utf-8") as file:
                raw_users: list[dict] = json.loads(file.read())
                users = [UserSaver.load(user) for user in raw_users]
                return {user.id: user for user in users}
        except FileNotFoundError:
            return {}

    def save_users(self):
        path = self.get_file_path()
        with open(f"{path}/users.txt", "w", encoding="utf-8") as file:
            users = (UserSaver.dumps(user) for user in self.users.values())
            users_str = ", ".join(users)
            file.write(f"[{users_str}]")


async def setup(bot: commands.Bot):
    await bot.add_cog(Logic(bot))
