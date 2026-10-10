"""Light-hearted text commands: praise, roast and (rate-limited) spam."""

from __future__ import annotations

import random

import discord
from discord.ext import commands

from sugar.config import DATA_DIR
from sugar.utils import load_lines

MAX_SPAM = 10


class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.praises = load_lines(DATA_DIR / "text" / "praises.txt")
        self.roasts = load_lines(DATA_DIR / "text" / "roasts.txt")

    @staticmethod
    def letter(author: discord.Member, member: discord.Member, message: str) -> discord.Embed:
        return discord.Embed(
            title=f"Dear {member.display_name},",
            description=f"{message}\n\n**Regards,**\n_{author.display_name}_",
            colour=discord.Colour.random(),
        )

    @commands.command(help="Say something nice to someone.")
    async def praise(self, ctx: commands.Context, member: discord.Member) -> None:
        await ctx.send(embed=self.letter(ctx.author, member, random.choice(self.praises)))

    @commands.command(help="Roast someone (all in good fun).")
    async def roast(self, ctx: commands.Context, member: discord.Member) -> None:
        await ctx.send(embed=self.letter(ctx.author, member, random.choice(self.roasts)))

    @commands.command(help=f"Repeat a message up to {MAX_SPAM} times.")
    @commands.guild_only()
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def spam(self, ctx: commands.Context, times: int, *, message: str) -> None:
        if not 1 <= times <= MAX_SPAM:
            ctx.command.reset_cooldown(ctx)
            await ctx.send(f"Pick a number between 1 and {MAX_SPAM}.")
            return
        for _ in range(times):
            await ctx.send(message, allowed_mentions=discord.AllowedMentions.none())


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Fun(bot))
