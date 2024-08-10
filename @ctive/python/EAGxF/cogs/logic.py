import discord
from discord.ext import commands

from eagxf.enums.screen_id import ScreenId
from eagxf.managers.output_manager import OutputManager
from eagxf.managers.reaction_input_manager import ReactionInputManager
from eagxf.managers.text_input_manager import TextinputManager
from eagxf.typedefs import DcMessage


class Logic(commands.Cog):
    def __init__(self, client: discord.Client) -> None:
        self.client = client
        self.opm = OutputManager(client)
        self.text_ipm = TextinputManager(self.opm)
        self.reaction_ipm = ReactionInputManager(self.opm)
        self.users = self.opm.users
        self.opm.start()

    @commands.command(name="enter")
    async def enter(self, ctx: commands.Context) -> None:
        """Registers the user."""
        if ctx.author.id not in self.users:
            user = self.opm.register_user(ctx.author)
            await self.opm.send_screen(ScreenId.HOME, user)
        else:
            user = self.users[ctx.author.id]
            await user.delete_message()
            await self.opm.send_screen(ScreenId.ALREADY_IN_PLATFORM, user)

    @commands.command(name="stop")
    async def stop(self, ctx: commands.Context) -> None:
        """Stops the bot."""
        await self.opm.stop_request_by(ctx.author.id)

    @commands.command(name="reset")
    async def reset(self, ctx: commands.Context) -> None:
        """Resets the bot."""
        await self.hi(ctx)

    @commands.command(name="hi")
    async def hi(self, ctx: commands.Context) -> None:
        """Sends the user's last screen."""
        if ctx.author.id not in self.users:
            return
        await self.bye(ctx)
        user = self.users[ctx.author.id]
        user.best_match_prio_order_new = []
        await self.opm.send_screen(user.last_screen or ScreenId.HOME, user)

    @commands.command(name="bye")
    async def bye(self, ctx: commands.Context) -> None:
        """Deletes the user's last message."""
        if ctx.author.id not in self.users:
            return
        user = self.users[ctx.author.id]
        await user.delete_message()

    @commands.Cog.listener()
    async def on_message(self, msg: DcMessage) -> None:
        await self.text_ipm.handle_input(msg)

    @commands.Cog.listener()
    async def on_raw_reaction_add(
        self, reaction: discord.RawReactionActionEvent
    ) -> None:
        await self.reaction_ipm.handle_added_reaction(reaction)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(
        self, reaction: discord.RawReactionActionEvent
    ) -> None:
        await self.reaction_ipm.handle_removed_reaction(reaction)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Logic(bot))
