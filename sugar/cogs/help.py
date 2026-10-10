"""A custom, sectioned help command."""

from __future__ import annotations

from dataclasses import dataclass

import discord
from discord.ext import commands


@dataclass(frozen=True)
class Section:
    emoji: str
    title: str
    entries: tuple[tuple[str, str], ...]  # (usage without prefix, description)


SECTIONS = {
    "music": Section(":musical_note:", "Music", (
        ("play <song or url>", "Play a song, or add it to the queue"),
        ("join", "Join your voice channel"),
        ("pause", "Pause the music"),
        ("resume", "Resume paused music"),
        ("skip", "Skip the current song"),
        ("queue", "Show the upcoming songs"),
        ("nowplaying", "Show the current song"),
        ("remove <number>", "Remove a song from the queue"),
        ("clear", "Clear the queue"),
        ("volume <0-100>", "Change the volume"),
        ("leave", "Leave the voice channel"),
    )),
    "games": Section(":video_game:", "Games", (
        ("tictactoe @player", "Tic-Tac-Toe for two players"),
        ("race @player", "Car race of pure luck for two players"),
        ("ludo @player [@player @player]", "Mini-Ludo for 2 to 4 players"),
        ("wordguesser", "Guess the hidden word, hangman style"),
    )),
    "gif": Section(":performing_arts:", "GIF", (
        ("slap @member", "Slap someone"),
        ("hug @member", "Hug someone"),
        ("wakeup @member", "Wake someone up"),
        ("cry [@member]", "Cry"),
        ("dance [@member]", "Dance"),
        ("shrug [@member]", "Shrug"),
        ("blush [@member]", "Blush"),
        ("laugh [@member]", "Laugh"),
        ("fakelaugh [@member]", "Fake a laugh"),
    )),
    "meme": Section(":placard:", "Meme", (
        ("meme", "A random meme"),
        ("meme dank", "A dank meme"),
        ("meme casual", "A casual meme"),
    )),
    "fun": Section(":jigsaw:", "Fun", (
        ("praise @member", "Say something nice"),
        ("roast @member", "Roast someone"),
        ("spam <times> <message>", "Repeat a message (max 10, once a minute)"),
    )),
}
ALIASES = {"game": "games", "gifs": "gif", "memes": "meme"}


class Help(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command(help="Show the command list, or details about one section.")
    async def help(self, ctx: commands.Context, section: str | None = None) -> None:
        prefix = ctx.clean_prefix

        if section is None:
            embed = discord.Embed(
                title=":heart_exclamation: Sugar's Commands :heart_exclamation:",
                description=f"Use `{prefix}help <section>` for details, e.g. `{prefix}help games`.",
                colour=discord.Colour.random(),
            )
            for name, sec in SECTIONS.items():
                names = dict.fromkeys(usage.split()[0] for usage, _ in sec.entries)  # dedupe, keep order
                listing = "\n".join(f"`{prefix}{cmd}`" for cmd in names)
                embed.add_field(name=f"{sec.emoji} **{sec.title}** (`{name}`)", value=listing)
            await ctx.send(embed=embed)
            return

        key = section.lower()
        sec = SECTIONS.get(ALIASES.get(key, key))
        if sec is None:
            await ctx.send(f"There's no section called `{section}`. Try one of: {', '.join(SECTIONS)}.")
            return

        embed = discord.Embed(title=f"{sec.emoji} {sec.title}", colour=discord.Colour.random())
        if sec is SECTIONS["games"]:
            embed.description = "Each game explains its rules when it starts."
        for usage, description in sec.entries:
            embed.add_field(name=f"`{prefix}{usage}`", value=description, inline=False)
        await ctx.send(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Help(bot))
