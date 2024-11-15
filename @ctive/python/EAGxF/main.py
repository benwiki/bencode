import asyncio
import os

import discord
from discord.ext import commands

from eagxf.constants import TOKEN_PATH
from tools.generate_error_codes import generate_error_codes

PROGRAM_PATH = os.path.dirname(os.path.realpath(__file__)).replace("\\", "/")

client = commands.Bot(command_prefix=".", intents=discord.Intents.all())


@client.event
async def on_ready() -> None:
    print("I'm ready. My name is", str(client.user))


async def load_extensions() -> None:
    for filename in os.listdir(f"{PROGRAM_PATH}/cogs"):
        if filename.endswith(".py"):
            # cut off the .py from the file name
            await client.load_extension(f"cogs.{filename[:-3]}")


async def main() -> None:
    generate_error_codes(PROGRAM_PATH)
    async with client:
        await load_extensions()
        await client.start(open(TOKEN_PATH, encoding="utf-8").read())


asyncio.run(main())
