import discord
from discord.ext import commands

TOKEN_PATH = 'C:/Users/Admin/prog/tokens/totpal.txt'

client = commands.Bot(command_prefix="-", intents=discord.Intents.all())


@client.event
async def on_ready():
    print(f'{client.user} is ready!')

@client.command(name='greet')
async def greet(channel):
    await channel.send("Hi, I'm here!")

client.run(open(TOKEN_PATH).read())
