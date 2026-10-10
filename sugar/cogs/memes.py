"""Image memes pulled from Reddit."""

from __future__ import annotations

import logging
import random

import asyncpraw
import discord
from discord.ext import commands

from sugar import config

log = logging.getLogger(__name__)

# category -> subreddits to draw from
CATEGORIES = {
    "random": ("Memes_Of_The_Dank",),
    "dank": ("IndianDankMemes", "desimemes"),
    "casual": ("school_memes", "engineeringmemes", "indianmemer", "ComedyCemetery"),
}
IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".gif")
FETCH_LIMIT = 50


class Memes(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.reddit: asyncpraw.Reddit | None = None
        # category -> memes not shown yet, as (title, image_url)
        self.cache: dict[str, list[tuple[str, str]]] = {category: [] for category in CATEGORIES}

    async def cog_load(self) -> None:
        if config.REDDIT_CLIENT_ID and config.REDDIT_CLIENT_SECRET:
            self.reddit = asyncpraw.Reddit(
                client_id=config.REDDIT_CLIENT_ID,
                client_secret=config.REDDIT_CLIENT_SECRET,
                user_agent=config.REDDIT_USER_AGENT,
            )

    async def cog_unload(self) -> None:
        if self.reddit:
            await self.reddit.close()

    async def refill(self, category: str) -> None:
        subreddit = await self.reddit.subreddit("+".join(CATEGORIES[category]))
        async for post in subreddit.hot(limit=FETCH_LIMIT):
            if not post.over_18 and not post.stickied and post.url.lower().endswith(IMAGE_EXTENSIONS):
                self.cache[category].append((post.title, post.url))

    @commands.command(help="Send a meme. Categories: random (default), dank, casual.")
    async def meme(self, ctx: commands.Context, category: str = "random") -> None:
        category = category.lower()
        if category not in CATEGORIES:
            await ctx.send(f"Unknown category. Choose from: {', '.join(CATEGORIES)}.")
            return
        if self.reddit is None:
            await ctx.send("Memes are disabled: Reddit credentials are not configured.")
            return

        memes = self.cache[category]
        if not memes:
            try:
                async with ctx.typing():
                    await self.refill(category)
            except Exception:
                log.exception("Fetching memes failed")
                await ctx.send("Couldn't reach Reddit right now. Try again later.")
                return
            if not memes:
                await ctx.send("No memes found right now. Try again later.")
                return

        title, url = memes.pop(random.randrange(len(memes)))
        await ctx.send(embed=discord.Embed(title=title[:256], colour=discord.Colour.random()).set_image(url=url))


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Memes(bot))
