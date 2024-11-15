from discord.ext import commands

from eagxf.enums.screen_id import ScreenId
from eagxf.managers.output_manager import OutputManager
from eagxf.managers.reaction_input_manager import ReactionInputManager
from eagxf.managers.text_input_manager import TextinputManager
from eagxf.managers.user_manager import UserManager
from eagxf.typedefs import DcClient, DcMessage, DcRawReactionEvent


class Logic(commands.Cog):
    def __init__(self, client: DcClient) -> None:
        self.client = client
        self.user_mng = UserManager(client)
        self.output_mng = OutputManager(self.user_mng)
        self.text_input_mng = TextinputManager(self.output_mng)
        self.reaction_input_mng = ReactionInputManager(self.output_mng)
        self.users = self.output_mng.users
        self.output_mng.start()

    @commands.command(name="enter")
    async def enter(self, ctx: commands.Context) -> None:
        """Registers the user."""
        if ctx.author.id not in self.users:
            user = self.user_mng.register_user(ctx.author)
            await self.output_mng.send_screen(ScreenId.HOME, user)
        else:
            user = self.users[ctx.author.id]
            await user.delete_message()
            await self.output_mng.send_screen(ScreenId.ALREADY_IN_PLATFORM, user)

    @commands.command(name="stop")
    async def stop(self, ctx: commands.Context) -> None:
        """Stops the bot."""
        await self.output_mng.stop_request_by(ctx.author.id)

    @commands.command(name="reset")
    async def reset(self, ctx: commands.Context) -> None:
        """Resets the bot."""
        await self.hi(ctx)

    @commands.command(name="hi")
    async def hi(self, ctx: commands.Context) -> None:
        """Sends the user's last screen."""
        if ctx.author.id not in self.users:
            return
        user = self.users[ctx.author.id]
        if not user.sleeping:
            await user.msg_bundle.send_front_spacer(ctx.author)
            await self.bye(ctx)
        user.best_match_prio_order_new = []
        await self.output_mng.send_screen(user.last_screen or ScreenId.HOME, user)
        await user.msg_bundle.delete_front_spacer()

    @commands.command(name="bye")
    async def bye(self, ctx: commands.Context) -> None:
        """Deletes the user's last message."""
        if ctx.author.id not in self.users:
            return
        user = self.users[ctx.author.id]
        await user.delete_message(spacer_too=True)

    @commands.Cog.listener()
    async def on_message(self, msg: DcMessage) -> None:
        await self.text_input_mng.handle_input(msg)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, reaction: DcRawReactionEvent) -> None:
        await self.reaction_input_mng.handle_added_reaction(reaction)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, reaction: DcRawReactionEvent) -> None:
        await self.reaction_input_mng.handle_removed_reaction(reaction)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Logic(bot))
