import asyncio
import os

import discord
from discord.ext import commands

from eagxf.constant_functions import INIT_USERS_PATH
from eagxf.constants import TOKEN_PATH

client = commands.Bot(command_prefix=".", intents=discord.Intents.all())
USERS_PATH = INIT_USERS_PATH()


@client.event
async def on_ready() -> None:
    print("I'm ready. My name is", str(client.user))

async def load_extensions() -> None:
    curdir = __file__.replace("\\", "/")
    curdir = "/".join(curdir.split("/")[:-1])
    for filename in os.listdir(f"{curdir}/cogs"):
        if filename.endswith(".py"):
            # cut off the .py from the file name
            await client.load_extension(f"cogs.{filename[:-3]}")


async def main() -> None:
    async with client:
        await load_extensions()
        await client.start(open(TOKEN_PATH).read())  # type: ignore


asyncio.run(main())
