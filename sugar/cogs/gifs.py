"""Reaction GIF commands powered by the Giphy search API."""

from __future__ import annotations

import logging
import random
from dataclasses import dataclass

import discord
from discord.ext import commands
from discord.utils import escape_markdown

from sugar import config

log = logging.getLogger(__name__)

GIPHY_SEARCH_URL = "https://api.giphy.com/v1/gifs/search"


@dataclass(frozen=True)
class GifAction:
    query: str
    solo_titles: tuple[str, ...]    # used when nobody is mentioned; {a} = author
    target_titles: tuple[str, ...]  # used when someone is mentioned; {t} = target


ACTIONS = {
    "slap": GifAction(
        "anime slap",
        (),
        ("Oooof! **{a}** slaps **{t}**!!", "Ouch! **{t}** got smashed by **{a}**!", "**{a}** lands a mighty blow on **{t}**!!"),
    ),
    "hug": GifAction("anime hug", (), ("**{a}** hugs **{t}**",)),
    "wakeup": GifAction("anime wake up", (), ("**{a}** wakes **{t}** up!!",)),
    "cry": GifAction(
        "anime cry",
        ("**{a}** is sad ;_;", "**{a}** cries ;_;"),
        ("**{a}** cries on **{t}**'s shoulder ;_;",),
    ),
    "dance": GifAction("anime dance", ("**{a}** is _vibing_", "**{a}** dances!"), ("**{a}** dances with **{t}**!",)),
    "shrug": GifAction("shrug", ("**{a}** shrugs",), ("**{a}** shrugs at **{t}**",)),
    "blush": GifAction("anime blush", ("**{a}** is blushing ^>^",), ("**{t}** made **{a}** blush ^>^",)),
    "laugh": GifAction(
        "anime laugh",
        ("LOL! **{a}** can't stop laughing", "HAHAHAHA!!! **{a}** can't stop laughing", "XD **{a}** can't stop laughing"),
        ("**{a}** laughs at **{t}** XD",),
    ),
    "fakelaugh": GifAction("fake laugh", ("**{a}** pretends to laugh...",), ("**{a}** fake-laughs at **{t}**'s joke",)),
}


class Gifs(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    async def send_gif(self, ctx: commands.Context, action_name: str, target: discord.Member | None) -> None:
        if not config.GIPHY_API_KEY:
            await ctx.send("GIFs are disabled: no `GIPHY_API_KEY` is configured.")
            return

        action = ACTIONS[action_name]
        if target is None and not action.solo_titles:
            await ctx.send(f"Mention someone to {action_name}!")
            return

        params = {"q": action.query, "api_key": config.GIPHY_API_KEY, "limit": "30", "rating": "pg-13"}
        try:
            async with ctx.typing(), self.bot.http_session.get(GIPHY_SEARCH_URL, params=params) as response:
                response.raise_for_status()
                results = (await response.json())["data"]
        except Exception:
            log.exception("Giphy request failed")
            await ctx.send("Couldn't reach Giphy right now. Try again later.")
            return

        if not results:
            await ctx.send("No GIFs found.")
            return

        author = escape_markdown(ctx.author.display_name)
        if target is None:
            title = random.choice(action.solo_titles).format(a=author)
        else:
            title = random.choice(action.target_titles).format(a=author, t=escape_markdown(target.display_name))

        gif_url = random.choice(results)["images"]["original"]["url"]
        await ctx.send(embed=discord.Embed(title=title, colour=discord.Colour.random()).set_image(url=gif_url))

    @commands.command(help="Slap someone.")
    async def slap(self, ctx: commands.Context, member: discord.Member) -> None:
        await self.send_gif(ctx, "slap", member)

    @commands.command(help="Hug someone.")
    async def hug(self, ctx: commands.Context, member: discord.Member) -> None:
        await self.send_gif(ctx, "hug", member)

    @commands.command(help="Wake someone up.")
    async def wakeup(self, ctx: commands.Context, member: discord.Member) -> None:
        await self.send_gif(ctx, "wakeup", member)

    @commands.command(help="Cry (optionally on someone's shoulder).")
    async def cry(self, ctx: commands.Context, member: discord.Member | None = None) -> None:
        await self.send_gif(ctx, "cry", member)

    @commands.command(help="Dance (optionally with someone).")
    async def dance(self, ctx: commands.Context, member: discord.Member | None = None) -> None:
        await self.send_gif(ctx, "dance", member)

    @commands.command(help="Shrug (optionally at someone).")
    async def shrug(self, ctx: commands.Context, member: discord.Member | None = None) -> None:
        await self.send_gif(ctx, "shrug", member)

    @commands.command(help="Blush (optionally because of someone).")
    async def blush(self, ctx: commands.Context, member: discord.Member | None = None) -> None:
        await self.send_gif(ctx, "blush", member)

    @commands.command(help="Laugh (optionally at someone).")
    async def laugh(self, ctx: commands.Context, member: discord.Member | None = None) -> None:
        await self.send_gif(ctx, "laugh", member)

    @commands.command(help="Fake a laugh (optionally at someone).")
    async def fakelaugh(self, ctx: commands.Context, member: discord.Member | None = None) -> None:
        await self.send_gif(ctx, "fakelaugh", member)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Gifs(bot))
