from typing import Any, Callable, Coroutine

import discord
from discord.ext import commands

DcButton = discord.ui.Button
DcView = discord.ui.View
DcUser = discord.User
DcMember = discord.Member
DcMessage = discord.Message
DcContext = commands.Context

Receiver = DcUser | DcMember | DcContext
ReceiverFuture = Coroutine[Any, Any, Receiver]
