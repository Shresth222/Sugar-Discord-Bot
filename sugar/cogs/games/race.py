"""Roll and Race: a two-player car race decided by a 4-sided die. One game per channel."""

from __future__ import annotations

import random

import discord
from discord.ext import commands

from sugar.utils import can_end_game, opponent_error, rules_embed

TRACK_LENGTH = 14
FINISH = TRACK_LENGTH - 1
DIE_FACES = 4
CARS = (":red_car:", ":blue_car:")
ROAD = ":white_large_square:"
FINISH_LINE = ":fireworks:"
SCENERY = [":vertical_traffic_light:"] + [":mountain:", ":mountain_snow:", ":mount_fuji:"] * 4 + [FINISH_LINE]
THUMBNAIL = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTfPsDK1mJlpMKOV7A9CC7zDEOAW2W2HfKgtg&usqp=CAU"


class RaceGame:
    def __init__(self, player1: discord.Member, player2: discord.Member) -> None:
        self.players = (player1, player2)
        self.positions = [0, 0]
        self.turn = 0

    @property
    def current(self) -> discord.Member:
        return self.players[self.turn]

    def drive(self) -> tuple[int, bool]:
        """Roll the die and move the current car. Returns (roll, whether the car moved)."""
        roll = random.randint(1, DIE_FACES)
        if self.positions[self.turn] + roll > FINISH:
            return roll, False
        self.positions[self.turn] += roll
        return roll, True

    def finished(self) -> list[discord.Member]:
        return [player for player, pos in zip(self.players, self.positions) if pos == FINISH]

    def render(self) -> str:
        def lane(car: int, cell: int) -> str:
            if self.positions[car] == cell:
                return CARS[car]
            return FINISH_LINE if cell == FINISH else ROAD

        return "\n".join(f"{SCENERY[i]} {lane(0, i)} {lane(1, i)} {SCENERY[i]}" for i in range(TRACK_LENGTH))


class Race(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.games: dict[int, RaceGame] = {}  # channel id -> game

    @commands.command(help="Start a car race against someone.")
    @commands.guild_only()
    async def race(self, ctx: commands.Context, opponent: discord.Member) -> None:
        if ctx.channel.id in self.games:
            await ctx.send("A race is already running in this channel. Finish it first.")
            return
        if error := opponent_error(ctx, [opponent]):
            await ctx.send(error)
            return

        game = self.games[ctx.channel.id] = RaceGame(ctx.author, opponent)
        p = ctx.clean_prefix
        await ctx.send(embed=rules_embed(
            "Roll and Race",
            "Luck is all you need.",
            f"Take turns rolling a die numbered 1 to {DIE_FACES}. You must land exactly on the finish line. "
            "Whoever gets there in fewer rolls wins. If both of you need the same number of rolls, it's a draw.",
            f"Use `{p}drive` on your turn to roll and move your car. Give up with `{p}quit_race`.",
            THUMBNAIL,
        ))
        await ctx.send(game.render())
        await ctx.send(f"{game.players[0].mention} drives the red car and goes first. {game.players[1].mention} drives the blue car.")

    @commands.command(aliases=["d"], help="Roll the die and move your car.")
    @commands.guild_only()
    async def drive(self, ctx: commands.Context) -> None:
        game = self.games.get(ctx.channel.id)
        if game is None:
            await ctx.send(f"No race here. Start one with `{ctx.clean_prefix}race @player`.")
            return
        if ctx.author != game.current:
            await ctx.send("Wait for your turn!" if ctx.author in game.players else "You're not in this race.")
            return

        roll, moved = game.drive()
        if moved:
            await ctx.send(f"You rolled a **{roll}**.\n{game.render()}")
        else:
            await ctx.send(f"You rolled a **{roll}**. Stop there! That would take you past the finish line.")

        # Both players get the same number of rolls, so the result is only decided after the blue car's turn.
        if game.turn == 1 and (winners := game.finished()):
            del self.games[ctx.channel.id]
            if len(winners) == 2:
                await ctx.send("Both cars crossed the line together. It's a tie!")
            else:
                await ctx.send(f"{winners[0].mention} has won the race! :checkered_flag:")
            return

        game.turn = 1 - game.turn
        await ctx.send(f"Your turn, {game.current.mention}.")

    @commands.command(aliases=["quitrace"], help="End the race in this channel.")
    @commands.guild_only()
    async def quit_race(self, ctx: commands.Context) -> None:
        game = self.games.get(ctx.channel.id)
        if game is None:
            await ctx.send(f"No race is running. Start one with `{ctx.clean_prefix}race @player`.")
        elif not can_end_game(ctx, game.players):
            await ctx.send("Only the racers (or a moderator) can end this race.")
        else:
            del self.games[ctx.channel.id]
            await ctx.send(f"The race has ended. Play again with `{ctx.clean_prefix}race @player`.")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Race(bot))
