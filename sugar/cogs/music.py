"""Music playback from YouTube (via yt-dlp), with one queue per server.

Requires FFmpeg on the PATH.
"""

from __future__ import annotations

import asyncio
import logging
from collections import deque
from dataclasses import dataclass
from functools import partial

import discord
import yt_dlp
from discord.ext import commands

log = logging.getLogger(__name__)

YTDL_OPTIONS = {
    "format": "bestaudio/best",
    "noplaylist": True,
    "quiet": True,
    "no_warnings": True,
    "default_search": "ytsearch",
    "source_address": "0.0.0.0",  # IPv6 addresses cause issues sometimes
}
FFMPEG_OPTIONS = {
    # Reconnect if YouTube drops the stream part-way through.
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -nostdin",
    "options": "-vn",
}
IDLE_TIMEOUT = 300  # seconds to wait for a new song before leaving
QUEUE_PAGE_SIZE = 10

ytdl = yt_dlp.YoutubeDL(YTDL_OPTIONS)


def format_duration(seconds: int | float | None) -> str:
    if not seconds:
        return "live"
    minutes, secs = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours}:{minutes:02}:{secs:02}" if hours else f"{minutes}:{secs:02}"


def info_embed(text: str) -> discord.Embed:
    return discord.Embed(description=text, colour=discord.Colour.green())


@dataclass
class Track:
    title: str
    web_url: str
    duration: int | None
    requester: discord.Member

    @property
    def link(self) -> str:
        return f"[{discord.utils.escape_markdown(self.title)}]({self.web_url})"

    @classmethod
    async def search(cls, query: str, requester: discord.Member, loop: asyncio.AbstractEventLoop) -> Track:
        data = await loop.run_in_executor(None, partial(ytdl.extract_info, query, download=False))
        if data and "entries" in data:
            data = next(iter(data["entries"]), None)
        if not data:
            raise LookupError(f"No results for {query!r}")
        return cls(data.get("title", "Unknown title"), data.get("webpage_url") or query, data.get("duration"), requester)

    async def create_source(self, loop: asyncio.AbstractEventLoop, volume: float) -> discord.PCMVolumeTransformer:
        # Stream URLs expire, so resolve a fresh one right before playing.
        data = await loop.run_in_executor(None, partial(ytdl.extract_info, self.web_url, download=False))
        return discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(data["url"], **FFMPEG_OPTIONS), volume=volume)


class MusicPlayer:
    """The queue and playback loop for a single server."""

    def __init__(self, cog: Music, guild: discord.Guild, channel: discord.abc.Messageable) -> None:
        self.cog = cog
        self.bot = cog.bot
        self.guild = guild
        self.channel = channel

        self.tracks: deque[Track] = deque()
        self.current: Track | None = None
        self.volume = 0.5
        self._has_tracks = asyncio.Event()
        self._song_finished = asyncio.Event()
        self.task = self.bot.loop.create_task(self.player_loop())

    def add(self, track: Track) -> None:
        self.tracks.append(track)
        self._has_tracks.set()

    async def _next_track(self) -> Track:
        while not self.tracks:
            self._has_tracks.clear()
            await self._has_tracks.wait()
        return self.tracks.popleft()

    async def player_loop(self) -> None:
        await self.bot.wait_until_ready()

        while True:
            try:
                track = await asyncio.wait_for(self._next_track(), IDLE_TIMEOUT)
            except asyncio.TimeoutError:
                await self.channel.send(embed=info_embed("Nothing played for 5 minutes, so I left the voice channel."))
                self.bot.loop.create_task(self.cog.cleanup(self.guild))
                return

            voice = self.guild.voice_client
            if voice is None:
                self.bot.loop.create_task(self.cog.cleanup(self.guild))
                return

            try:
                source = await track.create_source(self.bot.loop, self.volume)
            except Exception as error:
                log.exception("Could not play %s", track.web_url)
                await self.channel.send(embed=info_embed(f"Couldn't play {track.link}: `{error}`"))
                continue

            self.current = track
            self._song_finished.clear()
            voice.play(source, after=lambda _: self.bot.loop.call_soon_threadsafe(self._song_finished.set))
            await self.channel.send(
                embed=discord.Embed(
                    title="Now playing",
                    description=f"{track.link} [{track.requester.mention}]",
                    colour=discord.Colour.green(),
                )
            )
            await self._song_finished.wait()

            source.cleanup()
            self.current = None


class Music(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.players: dict[int, MusicPlayer] = {}

    async def cog_check(self, ctx: commands.Context) -> bool:
        if ctx.guild is None:
            raise commands.NoPrivateMessage()
        return True

    async def cog_unload(self) -> None:
        for player in list(self.players.values()):
            await self.cleanup(player.guild)

    async def cleanup(self, guild: discord.Guild) -> None:
        if guild.voice_client:
            await guild.voice_client.disconnect(force=True)
        player = self.players.pop(guild.id, None)
        if player and player.task is not asyncio.current_task():
            player.task.cancel()

    def get_player(self, ctx: commands.Context) -> MusicPlayer:
        player = self.players.get(ctx.guild.id)
        if player is None:
            player = self.players[ctx.guild.id] = MusicPlayer(self, ctx.guild, ctx.channel)
        return player

    async def ensure_voice(self, ctx: commands.Context) -> bool:
        """Connect to the author's voice channel if needed. Returns False (after explaining why) on failure."""
        if ctx.voice_client:
            return True
        if not ctx.author.voice or not ctx.author.voice.channel:
            await ctx.send(embed=info_embed("Join a voice channel first."))
            return False
        await ctx.author.voice.channel.connect()
        return True

    async def require_voice(self, ctx: commands.Context) -> discord.VoiceClient | None:
        voice = ctx.voice_client
        if not voice or not voice.is_connected():
            await ctx.send(embed=info_embed("I'm not connected to a voice channel."))
            return None
        return voice

    @commands.command(name="join", aliases=["connect", "j"], help="Join your voice channel.")
    async def join(self, ctx: commands.Context) -> None:
        if ctx.voice_client:
            await ctx.send(embed=info_embed(f"I'm already in **{ctx.voice_client.channel}**."))
        elif await self.ensure_voice(ctx):
            await ctx.send(f"**Joined `{ctx.voice_client.channel}`**")

    @commands.command(name="play", aliases=["sing", "p"], help="Play a song, or add it to the queue.")
    async def play(self, ctx: commands.Context, *, search: str) -> None:
        if not await self.ensure_voice(ctx):
            return

        async with ctx.typing():
            try:
                track = await Track.search(search, ctx.author, self.bot.loop)
            except (LookupError, yt_dlp.utils.DownloadError):
                await ctx.send(embed=info_embed(f"I couldn't find anything for **{discord.utils.escape_markdown(search)}**."))
                return

        self.get_player(ctx).add(track)
        await ctx.send(embed=info_embed(f"Queued {track.link} [{ctx.author.mention}]"))

    @commands.command(name="pause", aliases=["pa"], help="Pause the music.")
    async def pause(self, ctx: commands.Context) -> None:
        voice = ctx.voice_client
        if not voice or not voice.is_playing():
            await ctx.send(embed=info_embed("I'm not playing anything right now."))
            return
        voice.pause()
        await ctx.send("Paused ⏸️")

    @commands.command(name="resume", aliases=["r", "re"], help="Resume paused music.")
    async def resume(self, ctx: commands.Context) -> None:
        voice = await self.require_voice(ctx)
        if voice and voice.is_paused():
            voice.resume()
            await ctx.send("Resuming ⏯️")

    @commands.command(name="skip", aliases=["ss", "playnext", "pn"], help="Skip the current song.")
    async def skip(self, ctx: commands.Context) -> None:
        voice = await self.require_voice(ctx)
        if voice and (voice.is_playing() or voice.is_paused()):
            voice.stop()
            await ctx.message.add_reaction("⏭️")

    @commands.command(name="remove", aliases=["rm", "rem", "del"], help="Remove a song from the queue by its number.")
    async def remove(self, ctx: commands.Context, position: int) -> None:
        if not await self.require_voice(ctx):
            return
        tracks = self.get_player(ctx).tracks
        if not 1 <= position <= len(tracks):
            await ctx.send(embed=info_embed(f"There's no song #{position} in the queue."))
            return
        track = tracks[position - 1]
        del tracks[position - 1]
        await ctx.send(embed=info_embed(f"Removed {track.link} [{track.requester.mention}]"))

    @commands.command(name="clear", aliases=["clr", "cl"], help="Clear the queue.")
    async def clear(self, ctx: commands.Context) -> None:
        if await self.require_voice(ctx):
            self.get_player(ctx).tracks.clear()
            await ctx.send("💣 **Cleared**")

    @commands.command(name="queue", aliases=["q", "playlist", "que"], help="Show the upcoming songs.")
    async def queue(self, ctx: commands.Context) -> None:
        if not await self.require_voice(ctx):
            return
        player = self.get_player(ctx)
        if not player.current and not player.tracks:
            await ctx.send(embed=info_embed("The queue is empty."))
            return

        lines = []
        if player.current:
            current = player.current
            lines += ["__Now playing__:", f"{current.link} | `{format_duration(current.duration)}` Requested by {current.requester.mention}", ""]
        if player.tracks:
            lines.append("__Up next__:")
            for number, track in enumerate(list(player.tracks)[:QUEUE_PAGE_SIZE], start=1):
                lines.append(f"`{number}.` {track.link} | `{format_duration(track.duration)}` Requested by {track.requester.mention}")
            if len(player.tracks) > QUEUE_PAGE_SIZE:
                lines.append(f"...and {len(player.tracks) - QUEUE_PAGE_SIZE} more")
        lines.append(f"\n**{len(player.tracks)} song(s) in queue**")

        embed = discord.Embed(title=f"Queue for {ctx.guild.name}", description="\n".join(lines), colour=discord.Colour.green())
        embed.set_footer(text=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=embed)

    @commands.command(
        name="nowplaying",
        aliases=["np", "song", "current", "currentsong", "playing", "cp"],
        help="Show the current song.",
    )
    async def now_playing(self, ctx: commands.Context) -> None:
        if not await self.require_voice(ctx):
            return
        track = self.get_player(ctx).current
        if not track:
            await ctx.send(embed=info_embed("I'm not playing anything right now."))
            return
        embed = info_embed(f"{track.link} [{track.requester.mention}] | `{format_duration(track.duration)}`")
        embed.set_author(name="Now Playing 🎶", icon_url=self.bot.user.display_avatar.url)
        await ctx.send(embed=embed)

    @commands.command(name="volume", aliases=["vol"], help="Change the volume (0-100).")
    async def volume(self, ctx: commands.Context, percent: int) -> None:
        voice = await self.require_voice(ctx)
        if not voice:
            return
        if not 0 <= percent <= 100:
            await ctx.send("Volume must be between 0 and 100.")
            return
        self.get_player(ctx).volume = percent / 100
        if isinstance(voice.source, discord.PCMVolumeTransformer):
            voice.source.volume = percent / 100
        await ctx.send(f"🔊 Volume set to **{percent}%**")

    @commands.command(name="leave", aliases=["stop", "dc", "disconnect", "bye"], help="Leave the voice channel.")
    async def leave(self, ctx: commands.Context) -> None:
        if await self.require_voice(ctx):
            await self.cleanup(ctx.guild)
            await ctx.send("**Successfully disconnected** 👋")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Music(bot))
