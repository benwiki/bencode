import asyncio
import datetime
from dataclasses import dataclass, field
from enum import Enum
import json
from typing import Callable

import discord
from discord.ext import commands


@dataclass
class Date:
    day: int
    month: int
    year: int
    hour: int | None = None
    minute: int | None = None
    second: int | None = None

    def __str__(self):
        if self.hour is not None:
            return (
                f"{self.day:02}.{self.month:02}.{self.year}"
                f" {self.hour:02}:{self.minute:02}:{self.second:02}"
            )
        return f"{self.day:02}.{self.month:02}.{self.year}"

    def __repr__(self):
        return str(self)


class Status(Enum):
    AVAILABLE = "Available"
    BUSY = "Busy"
    OFFLINE = "Offline"
    INVISIBLE = "Invisible"
    DO_NOT_DISTURB = "Do Not Disturb"


STATUS_EMOJI: dict[Status, str] = {
    Status.AVAILABLE: "🟢",
    Status.BUSY: "🟡",
    Status.OFFLINE: "⚪",
    Status.INVISIBLE: "🟣",
    Status.DO_NOT_DISTURB: "🔴",
}


@dataclass
class PlatformUser:
    id: int = 0
    date_joined: Date = field(default_factory=lambda: Date(1, 1, 2000))
    name: str = "?"  # max 50 chars
    title: str = "?"  # max 100 chars
    location: str = "?"
    languages: str = "?"  # comma separated
    questions: dict[str, str] = field(default_factory=dict)
    keywords: str = "?"  # comma separated
    status: Status = Status.INVISIBLE
    msg_to_delete: discord.Message | None = None
    change: str = ""


class UserSaver:
    @staticmethod
    def dumps(user: PlatformUser):
        return json.dumps(
            {
                "id": user.id,
                "date_joined": str(user.date_joined),
                "name": user.name,
                "title": user.title,
                "location": user.location,
                "languages": user.languages,
                "questions": user.questions,
                "keywords": user.keywords,
                "status": user.status.value,
            }
        )

    @staticmethod
    def load(user_data: dict):
        user = PlatformUser()
        user.id = user_data["id"]
        d, m, y = map(int, user_data["date_joined"].split("."))
        user.date_joined = Date(day=d, month=m, year=y)
        user.name = user_data["name"]
        user.title = user_data["title"]
        user.location = user_data["location"]
        user.languages = user_data["languages"]
        user.questions = user_data["questions"]
        user.keywords = user_data["keywords"]
        user.status = Status(user_data["status"])
        return user


@dataclass
class SimpleButton:
    label: str = field(default_factory=str)
    style: discord.ButtonStyle = discord.ButtonStyle.primary
    callback: Callable | None = None
    structure: "Structure | None" = None
    takes_to: int = -1


@dataclass
class Structure:
    id: int = field(default_factory=int)
    message: str = field(default_factory=str)
    buttons: list[SimpleButton] = field(default_factory=list)
    reactions: list[str] = field(default_factory=list)
    changes_property: str | None = None
    comma_separated: bool = False


class Logic(commands.Cog):
    start_view = discord.ui.View()
    profile = (
        "***=== Your profile ===***"
        "\n\n**Metadata**"
        "\n- *User ID:* <id>"
        "\n- *Date Joined:* <date_joined>"
        "\n**Personal**"
        "\n- *Name:* <name>"
        "\n- *Title:* <title>"
        "\n- *Location:* <location>"
        "\n- *Languages:* <languages>"
        "\n**Questions**"
        "\n*Where do I need help / what do I want to learn?*"
        "\n- <need_help>"
        "\n*Where can I help / what is my expertise?*"
        "\n- <can_help>"
        "\n*What do I trust / recommend?*"
        "\n- <trust_recommend>"
        "\n*What am I concerned about / what do I not recommend?*"
        "\n- <concern_not_recommend>"
        "\n**Keywords**: <keywords>"
        "\n**Status**: <status>"
    )

    def __init__(self, client: discord.Client) -> None:
        self.client = client
        self.channel = None
        self.app_name = "EAGxF"
        self.users: dict[int, PlatformUser] = self.load_users()
        for user_id in self.users:
            asyncio.create_task(self.send_starting_message_to(user_id))
        self.start_messages: list[discord.Message] = []
        self.structures = [
            Structure(
                id=2,
                message=f"status: <status>\nWelcome to {self.app_name}, <name>!"
                " Click the buttons to use the app!",
                buttons=[
                    SimpleButton(label="See Profile", takes_to=3),
                    SimpleButton(label="Edit Profile", takes_to=4),
                ],
            ),
            Structure(
                id=3,
                message=self.profile,
                buttons=[
                    SimpleButton(
                        label="⬅️ Back", style=discord.ButtonStyle.red, takes_to=2
                    ),
                    SimpleButton(label="Edit", takes_to=4),
                ],
            ),
            Structure(
                id=4,
                message=self.profile + "\n\n🛠️ **Edit Profile** 🛠️"
                "\n\nWhat do you want to change?",
                buttons=[
                    SimpleButton(
                        label="⬅️ Back", style=discord.ButtonStyle.red, takes_to=2
                    ),
                    SimpleButton(label="Name", takes_to=5),
                    SimpleButton(label="Title", takes_to=6),
                    SimpleButton(label="Location", takes_to=7),
                    SimpleButton(label="Languages", takes_to=8),
                    SimpleButton(
                        label="Answers to Questions",
                        style=discord.ButtonStyle.secondary,
                        takes_to=9,
                    ),
                    SimpleButton(label="Keywords", takes_to=10),
                    SimpleButton(label="Status", takes_to=11),
                ],
            ),
            Structure(
                id=5,
                message="Your current name is: <name>."
                "\nWhat do you want to change your name to?",
                changes_property="name",
            ),
            Structure(
                id=6,
                message="Your current title is: <title>."
                "\nWhat do you want to change your title to?",
                changes_property="title",
            ),
            Structure(
                id=7,
                message="Your current location is: <location>."
                "\nWhat do you want to change your location to?",
                changes_property="location",
            ),
            Structure(
                id=8,
                message="Your current languages are: <languages>."
                "\nWhat do you want to change your languages to?"
                "\n(Comma separated, e.g. English, German, Spanish)",
                changes_property="languages",
                comma_separated=True,
            ),
            Structure(
                id=9,
                message="**Your current answers to questions are:**"
                "\nWhere do I need help / what do I want to learn?"
                "\n- <need_help>"
                "\nWhere can I help / what is my expertise?"
                "\n- <can_help>"
                "\nWhat do I trust / recommend?"
                "\n- <trust_recommend>"
                "\nWhat am I concerned about / what do I not recommend?"
                "\n- <concern_not_recommend>"
                "\nWhat do you want to change?",
                buttons=[
                    SimpleButton(
                        label="⬅️ Back", style=discord.ButtonStyle.red, takes_to=4
                    ),
                    SimpleButton(label="Need Help", takes_to=12),
                    SimpleButton(label="Can Help", takes_to=13),
                    SimpleButton(label="Trust / Recommend", takes_to=14),
                    SimpleButton(label="Concern / Not Recommend", takes_to=15),
                ],
            ),
            Structure(
                id=10,
                message="Your current keywords are: <keywords>."
                "\nWhat do you want to change your keywords to?"
                "\n(Comma separated, e.g. psychology, Python, electric guitar)",
                changes_property="keywords",
                comma_separated=True,
            ),
            Structure(
                id=11,
                message="Your current status is: <status>."
                "\nWhat do you want to change your status to?"
                "\n(Select the corresponding reaction!)\n"
                + "\n".join(
                    f"{emoji} ({status.value})"
                    for status, emoji in STATUS_EMOJI.items()
                ),
                reactions=list(STATUS_EMOJI.values()),
                changes_property="status",
            ),
            Structure(
                id=12,
                message="Your current answer to 'Where do I need help /"
                " what do I want to learn?' is: <need_help>."
                "\nWhat do you want to change it to?",
                changes_property="need_help",
            ),
            Structure(
                id=13,
                message="Your current answer to 'Where can I help /"
                " what is my expertise?' is: <can_help>."
                "\nWhat do you want to change it to?",
                changes_property="can_help",
            ),
            Structure(
                id=14,
                message="Your current answer to 'What do I trust /"
                " recommend?' is: <trust_recommend>."
                "\nWhat do you want to change it to?",
                changes_property="trust_recommend",
            ),
            Structure(
                id=15,
                message="Your current answer to 'What am I concerned about /"
                " what do I not recommend?' is: <concern_not_recommend>."
                "\nWhat do you want to change it to?",
                changes_property="concern_not_recommend",
            ),
        ]
        self.init_structures()
    
    def load_users(self) -> dict[int, PlatformUser]:
        path = self.get_file_path()
        try:
            with open(f"{path}/users.txt", "r", encoding="utf-8") as file:
                raw_users: list[dict] = json.loads(file.read())
                users = [UserSaver.load(user) for user in raw_users]
                return {user.id: user for user in users}
        except FileNotFoundError:
            return {}

    async def save_users(self):
        path = self.get_file_path()
        with open(f"{path}/users.txt", "w", encoding="utf-8") as file:
            users = (UserSaver.dumps(user) for user in self.users.values())
            users_str = ", ".join(users)
            file.write(f"[{users_str}]")

    def get_file_path(self):
        curdir = __file__.replace('\\', '/')
        return '/'.join(curdir.split('/')[:-1])

    async def send_starting_message_to(self, user_id: int):
        user = await self.client.fetch_user(user_id)
        await self.send_structure(user, self.get_structure(2))  # type: ignore

    def init_structures(self):
        for structure in self.structures:
            for button in structure.buttons:
                structure = self.get_structure(button.takes_to)
                if structure is None:
                    raise ValueError(f"Structure with id {button.takes_to} not found!")
                button.structure = structure
                button.callback = self.get_structure_callback(button.structure)

    def get_structure_callback(self, structure: Structure):
        async def callback(interaction: discord.Interaction):
            await interaction.response.defer()
            await self.send_structure(interaction.user, structure)

        return callback

    async def send_structure(
        self, dc_user: discord.User | discord.Member, structure: Structure
    ):
        user = self.register_user(dc_user)
        await self.delete_last_msg_of(user)
        view = discord.ui.View()
        for button in structure.buttons:
            dc_button: discord.ui.Button = discord.ui.Button(
                label=button.label, style=button.style
            )
            dc_button.callback = button.callback  # type: ignore
            view.add_item(dc_button)

        user.msg_to_delete = await dc_user.send(
            self.replace_placeholders(structure.message, dc_user.id),
            view=view,
        )

        if structure.changes_property:
            user.change = structure.changes_property

        if structure.reactions:
            for emoji in structure.reactions:
                await user.msg_to_delete.add_reaction(emoji)
        await self.save_users()

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
                    "trust_recommend": "?",
                    "concern_not_recommend": "?",
                },
            )
        return self.users[user.id]

    def get_structure(self, structure_id: int):
        for structure in self.structures:
            if structure.id == structure_id:
                return structure
        return None

    def replace_placeholders(self, message: str, user_id: int) -> str:
        user = self.users[user_id]

        return (
            message.replace("<id>", str(user.id))
            .replace("<date_joined>", str(user.date_joined))
            .replace("<name>", user.name)
            .replace("<title>", user.title)
            .replace("<location>", user.location)
            .replace("<languages>", user.languages)
            .replace("<need_help>", user.questions["need_help"])
            .replace("<can_help>", user.questions["can_help"])
            .replace("<trust_recommend>", user.questions["trust_recommend"])
            .replace("<concern_not_recommend>", user.questions["concern_not_recommend"])
            .replace("<keywords>", user.keywords)
            .replace("<status>", f"{STATUS_EMOJI[user.status]} ({user.status.value})")
        )

    @commands.command(name="b")
    async def enter(self, ctx: commands.Context):
        """Gives you the starting button."""
        view = discord.ui.View()
        button: discord.ui.Button = discord.ui.Button(
            label="Enter Platform", style=discord.ButtonStyle.primary
        )
        view.add_item(button)
        enter = self.get_structure(2)
        button.callback = self.get_structure_callback(enter)  # type: ignore
        self.start_messages.append(
            await ctx.send(
                "Hello! If you click the button, the bot will DM you"
                " and you enter the platform!",
                view=view,
            )
        )

    @commands.command(name="stop")
    async def stop(self, _):
        """Stops the bot."""
        for user in self.users.values():
            await self.delete_last_msg_of(user)
        for msg in self.start_messages:
            await msg.delete()
        await self.client.close()

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        user = self.users.get(msg.author.id)
        if user is None or user.change in ["status", ""]:
            return

        view = discord.ui.View()
        ok_btn: discord.ui.Button = discord.ui.Button(
            label="OK", style=discord.ButtonStyle.green
        )
        ok_btn.callback = self.get_structure_callback(self.get_structure(4))  # type: ignore
        view.add_item(ok_btn)
        home_btn: discord.ui.Button = discord.ui.Button(
            label="Home", style=discord.ButtonStyle.secondary
        )
        home_btn.callback = self.get_structure_callback(self.get_structure(2))  # type: ignore
        view.add_item(home_btn)

        await self.delete_last_msg_of(user)
        await msg.add_reaction("✅")
        user = self.users[msg.author.id]

        changed = user.change
        if user.change in [
            "need_help",
            "can_help",
            "trust_recommend",
            "concern_not_recommend",
        ]:
            changed = "answer"
            user.questions[user.change] = msg.content
        elif user.change in ["keywords", "languages"]:
            kws = [kw.strip() for kw in msg.content.split(",")]
            evenly_spaced_kws = ", ".join(kws)
            setattr(user, user.change, evenly_spaced_kws)
        else:
            setattr(user, user.change, msg.content)

        if user.change in ["keywords", "languages"]:
            keywords = "\n- ".join(kws)
            user.msg_to_delete = await msg.channel.send(
                f"✅ Your {changed} have been changed to:\n- {keywords}"
                f'\n("{evenly_spaced_kws}")',
                view=view,
            )
        else:
            user.msg_to_delete = await msg.channel.send(
                f'✅ Your {changed} has been changed to "{msg.content}"!', view=view
            )
        user.change = ""
        await self.save_users()

    @commands.Cog.listener()
    async def on_reaction_add(
        self, reaction: discord.Reaction, dc_user: discord.User | discord.Member
    ):
        view = discord.ui.View()
        ok_btn: discord.ui.Button = discord.ui.Button(
            label="OK", style=discord.ButtonStyle.green
        )
        view.add_item(ok_btn)
        ok_btn.callback = self.get_structure_callback(self.get_structure(4))  # type: ignore
        home_btn: discord.ui.Button = discord.ui.Button(
            label="Home", style=discord.ButtonStyle.secondary
        )
        home_btn.callback = self.get_structure_callback(self.get_structure(2))  # type: ignore
        view.add_item(home_btn)

        user = self.users[dc_user.id]
        if (
            user.msg_to_delete is not None
            and reaction.message.id == user.msg_to_delete.id
        ):
            if user.change == "status":
                for status, emoji in STATUS_EMOJI.items():
                    if reaction.emoji == emoji:
                        user.status = status
                        await self.delete_last_msg_of(user)
                        user.msg_to_delete = await reaction.message.channel.send(
                            f"✅ Your status has been changed to {emoji} ({status.value})!",
                            view=view,
                        )
                        user.change = ""
                        await self.save_users()

    async def delete_last_msg_of(self, user: PlatformUser):
        if user.msg_to_delete is not None:
            await user.msg_to_delete.delete()
            user.msg_to_delete = None

    def is_valid_date(self, date: str):
        return (
            len(date) == 10
            and date[2] == date[5] == "."
            and date.replace(".", "").isnumeric()
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(Logic(bot))
