"""Helpers shared by several cogs."""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

import discord
from discord.ext import commands


def load_lines(path: Path) -> list[str]:
    """Read a text file into a list of its non-empty, stripped lines."""
    with open(path, encoding="utf-8") as file:
        return [line.strip() for line in file if line.strip()]


def rules_embed(title: str, tagline: str, rules: str, how_to_play: str, thumbnail: str | None = None) -> discord.Embed:
    """Build the embed every game shows when it starts."""
    embed = discord.Embed(title=title, description=tagline, colour=discord.Colour.random())
    embed.add_field(name="Rules", value=rules, inline=False)
    embed.add_field(name="How to play", value=how_to_play, inline=False)
    if thumbnail:
        embed.set_thumbnail(url=thumbnail)
    return embed


def opponent_error(ctx: commands.Context, opponents: Sequence[discord.Member]) -> str | None:
    """Return why these opponents can't play with the command author, or None if they can."""
    if any(member.bot for member in opponents):
        return "Bots can't play games. Mention a human instead."
    if ctx.author in opponents:
        return "You can't play against yourself. Mention someone else."
    if len(set(opponents)) != len(opponents):
        return "Each player can only be mentioned once."
    return None


def can_end_game(ctx: commands.Context, players: Sequence[discord.abc.User]) -> bool:
    """Players can end their own game; moderators can end any game."""
    return ctx.author in players or ctx.channel.permissions_for(ctx.author).manage_messages
