"""The bot class: loads every cog and handles command errors in one place."""

from __future__ import annotations

import logging

import aiohttp
import discord
from discord.ext import commands

from . import config

log = logging.getLogger(__name__)

EXTENSIONS = (
    "sugar.cogs.help",
    "sugar.cogs.fun",
    "sugar.cogs.gifs",
    "sugar.cogs.memes",
    "sugar.cogs.music",
    "sugar.cogs.games.tictactoe",
    "sugar.cogs.games.race",
    "sugar.cogs.games.ludo",
    "sugar.cogs.games.word_guesser",
)


class SugarBot(commands.Bot):
    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.message_content = True  # also enable "Message Content Intent" in the developer portal

        super().__init__(
            command_prefix=commands.when_mentioned_or(config.PREFIX),
            intents=intents,
            help_command=None,  # replaced by the Help cog
            case_insensitive=True,
        )
        self.http_session: aiohttp.ClientSession | None = None

    async def setup_hook(self) -> None:
        self.http_session = aiohttp.ClientSession()
        for extension in EXTENSIONS:
            try:
                await self.load_extension(extension)
                log.info("Loaded %s", extension)
            except Exception:
                log.exception("Failed to load %s", extension)

    async def close(self) -> None:
        if self.http_session:
            await self.http_session.close()
        await super().close()

    async def on_ready(self) -> None:
        log.info("Logged in as %s (ID: %s)", self.user, self.user.id)
        await self.change_presence(activity=discord.Game(name=f"{config.PREFIX}help"))

    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError) -> None:
        if isinstance(error, commands.CommandNotFound):
            return

        usage = f"`{ctx.clean_prefix}{ctx.command.qualified_name} {ctx.command.signature}`" if ctx.command else ""

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"You're missing `{error.param.name}`. Usage: {usage}")
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send("I couldn't find that member. Mention them like @name.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send(f"That argument doesn't look right. Usage: {usage}")
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"Slow down! Try again in {error.retry_after:.0f}s.")
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send("This command only works in a server.")
        elif isinstance(error, commands.CheckFailure):
            await ctx.send("You can't use this command here.")
        else:
            log.error("Error in command %s", ctx.command, exc_info=error)
            await ctx.send("Something went wrong while running that command.")
