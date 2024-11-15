from typing import Any, Coroutine

import discord
from discord.ext import commands

DcButton = discord.ui.Button
DcView = discord.ui.View
DcUser = discord.User | discord.Member
DcMessage = discord.Message
DcContext = commands.Context
DcClient = discord.Client
DcRawReactionEvent = discord.RawReactionActionEvent
DcEmoji = discord.Emoji
DcGuild = discord.Guild
DcInteraction = discord.Interaction

Receiver = DcUser | DcContext
ReceiverFuture = Coroutine[Any, Any, Receiver]
