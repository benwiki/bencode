import random

import discord
from discord.ext import commands


class Logic(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="roll")
    async def roll(self, ctx, *, dice: str):
        """Rolls a dice in NdN format."""
        try:
            rolls, limit = map(int, dice.split("d"))
        except Exception:
            await ctx.send("Format has to be in NdN!")
            return
        if rolls > 100:
            await ctx.send("I can't roll more than 100 dice at once!")
            return
        if limit > 1000:
            await ctx.send("I can't roll a dice with more than 1000 sides!")
            return
        result = ", ".join(str(random.randint(1, limit)) for r in range(rolls))
        await ctx.send(result)

    @commands.command(name="choose")
    async def choose(self, ctx, *choices: str):
        """Chooses between multiple choices."""
        await ctx.send(random.choice(choices))

    @commands.command(name="repeat")
    async def repeat(self, ctx, times: int, *, content: str):
        """Repeats a message multiple times."""
        if times > 100:
            await ctx.send("I can't repeat a message more than 100 times!")
            return
        for _ in range(times):
            await ctx.send(content)

    @commands.command(name="joined")
    async def joined(self, ctx, *, member: discord.Member):
        """Says when a member joined."""
        await ctx.send(f"{member.display_name} joined on {member.joined_at}")

    @commands.command(name="coolbot")
    async def coolbot(self, ctx):
        """Is the bot cool?"""
        await ctx.send("This bot is cool. :sunglasses:")

    @commands.command(name="cooluser")
    async def cooluser(self, ctx, member: discord.Member):
        """Is the user cool?"""
        await ctx.send(f"{member.display_name} is cool. :sunglasses:")

    @commands.command(name="ping")
    async def ping(self, ctx):
        """Pong!"""
        await ctx.send("Pong!")

async def setup(bot):
    await bot.add_cog(Logic(bot))