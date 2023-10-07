import discord
from discord.ext import commands
import os

client = commands.Bot(command_prefix="-")

@client.event
async def on_ready():
    print("I'm ready. My name is", str(client.user))

initial_extensions = []

for filename in os.listdir('./cogs'):
    if filename.endswith(".py"):
        initial_extensions.append("cogs." + filename[:-3])

if __name__ == "__main__":
    for extension in initial_extensions:
        client.load_extension(extension)

client.run(
    'NzEzMDQ0NjU2MTAzMDk2Mzky.Xs5xDQ.j3Rkcn6uLPO0-mqOjJUmMl41_Pw'
)