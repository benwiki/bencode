import random
import struct
from dataclasses import dataclass, field
from typing import Callable

import discord
from discord.ext import commands


@dataclass
class Birthday:
    day: int
    month: int
    year: int

    def __str__(self):
        return f"{self.day:02}.{self.month:02}.{self.year}"
    
    def __repr__(self):
        return str(self)

@dataclass
class PlatformUser:
    name: str
    birthday: Birthday
    change: str = ""
    # def __init__(self, name, birthday) -> None:
    #     self.name = name
    #     self.birthday = birthday
    #     self.change: str = ""
    
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
    reply_required: bool = field(default=False)


class Logic(commands.Cog):
    start_view = discord.ui.View()

    def __init__(self, client) -> None:
        self.client = client
        self.channel = None
        self.app_name = "EAGxF"
        self.users: dict[int, PlatformUser] = {}
        self.msg_to_delete: discord.Message | None = None
        self.structures = [
            Structure(
                id=2, message=
                    f"Welcome to {self.app_name}, <name>! Click the buttons to use the app!",
                buttons=[
                    SimpleButton(
                        label="See Profile",
                        takes_to=3 ),
                    SimpleButton(
                        label="Edit Profile",
                        takes_to=4 )]),
            Structure(
                id=3, message=
                    "- Name: <name>\n- Birthday: <birthday>",
                buttons=[
                    SimpleButton(
                        label="⬅️ Back",
                        style=discord.ButtonStyle.red,
                        takes_to=2 )]),
            Structure(
                id=4, message=
                    "Let's edit your profile! What do you want to change?",
                buttons=[
                    SimpleButton(
                        label="⬅️ Back",
                        style=discord.ButtonStyle.red,
                        takes_to=2 ),
                    SimpleButton(
                        label="Name",
                        takes_to=5 ),
                    SimpleButton(
                        label="Birthday",
                        takes_to=6 )]),
            Structure(
                id=5, message=
                    "Your current name is: <name>.\nWhat do you want to change your name to?",
                reply_required=True),
            Structure(
                id=6, message=
                    "Your current birthday is: <birthday>.\nWhat do you want to change your birthday to?",
                reply_required=True)
        ]
        self.init_structures()

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
            self.register_user(interaction.user)
            await self.delete_last_msg()
            view = discord.ui.View()
            for button in structure.buttons:
                dc_button: discord.ui.Button = discord.ui.Button(
                    label=button.label, style=button.style)
                dc_button.callback = button.callback  # type: ignore
                view.add_item(dc_button)
              
            self.msg_to_delete = await interaction.user.send(
                self.replace_placeholders(structure.message, interaction.user.id),
                view=view)

            user_id = interaction.user.id
            user = self.users[user_id]
            if structure.reply_required:
                if structure.id == 5:
                    user.change = "name"
                elif structure.id == 6:
                    user.change = "birthday"
        return callback
    
    def register_user(self, user: discord.User | discord.Member):
        if user.id not in self.users:
            self.users[user.id] = PlatformUser(user.name, Birthday(1, 1, 2000))
    
    def get_structure(self, structure_id: int):
        for structure in self.structures:
            if structure.id == structure_id:
                return structure
        return None
    
    def replace_placeholders(self, message: str, user_id: int) -> str:
        user_name = self.users[user_id].name
        user_birthday = self.users[user_id].birthday
        
        return ( message
            .replace("<name>", user_name)
            .replace("<birthday>", str(user_birthday))
        )

    @commands.command(name="b")
    async def gimmebutton(self, ctx: commands.Context):
        """Gives you buttons."""
        view = discord.ui.View()
        button: discord.ui.Button = discord.ui.Button(
            label="Enter Platform", style=discord.ButtonStyle.primary)
        view.add_item(button)
        enter = self.get_structure(2)
        button.callback = self.get_structure_callback(enter)  # type: ignore
        await ctx.send(
            "Hello! If you click the button, the bot will DM you"
            " and you enter the platform!", view=view)

    @commands.Cog.listener()
    async def on_message(self, msg: discord.Message):
        user = self.users.get(msg.author.id)
        if user is None:
            return

        ok_view = discord.ui.View()
        ok_btn: discord.ui.Button = discord.ui.Button(
            label="OK", style=discord.ButtonStyle.green)
        ok_view.add_item(ok_btn)
        ok_btn.callback = self.get_structure_callback( # type: ignore
            self.get_structure(2))  # type: ignore

        # ------ Name Changer ------
        if user.change == "name":  # name_id is not None and message_id == name_id:
            await self.delete_last_msg()
            await msg.add_reaction("✅")
            self.users[msg.author.id].name = msg.content
            self.msg_to_delete = await msg.channel.send(
                f"✅ Your name has been changed to \"{msg.content}\"!",
                view=ok_view)
            user.change = ""

        # ------ Birthday Changer ------
        elif user.change == "birthday":
            await self.delete_last_msg()
            if not self.is_valid_date(msg.content):
                await msg.add_reaction("❌")
                self.msg_to_delete = await msg.channel.send(
                    "❌ Invalid date format! Please use (DD.MM.YYYY) format!"
                    "\nReply to this message with your new birthday in (DD.MM.YYYY) format!")
            else:
                await msg.add_reaction("✅")
                day, month, year = map(int, msg.content.split("."))
                self.users[msg.author.id].birthday = Birthday(day, month, year)
                self.msg_to_delete = await msg.channel.send(
                    f"✅ Your birthday has been changed to \"{msg.content}\"!",
                    view=ok_view)
                user.change = ""

    async def delete_last_msg(self):
        if self.msg_to_delete is not None:
            await self.msg_to_delete.delete()
            self.msg_to_delete = None

    def is_valid_date(self, date: str):
        return (
            len(date) == 10
            and date[2] == date[5] == "."
            and date.replace(".", "").isnumeric())

async def setup(bot: commands.Bot):
    await bot.add_cog(Logic(bot))
