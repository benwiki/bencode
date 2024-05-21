from typing import Any, Coroutine

import discord
from discord.ext import commands

DcButton = discord.ui.Button
DcView = discord.ui.View
DcUser = discord.User | discord.Member
DcMessage = discord.Message
DcContext = commands.Context

Receiver = DcUser | DcContext
ReceiverFuture = Coroutine[Any, Any, Receiver]
