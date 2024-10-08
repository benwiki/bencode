import discord
from discord.ext import commands
import os
import asyncio

TOKEN_PATH = 'C:/Users/Admin/prog/tokens/totpal.txt'

client = commands.Bot(command_prefix=".4$", intents=discord.Intents.all())

@client.event
async def on_ready():
    print("I'm ready. My name is", str(client.user))

async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            # cut off the .py from the file name
            await client.load_extension(f"cogs.{filename[:-3]}")
            
async def main():
    async with client:
        await load_extensions()
        await client.start(open(TOKEN_PATH).read())

asyncio.run(main())
