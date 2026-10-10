"""Two-player Tic-Tac-Toe. One game per channel."""

from __future__ import annotations

import discord
from discord.ext import commands

from sugar.utils import can_end_game, opponent_error, rules_embed

MARKS = (":regional_indicator_x:", ":o2:")
CELL_NUMBERS = (":one:", ":two:", ":three:", ":four:", ":five:", ":six:", ":seven:", ":eight:", ":nine:")
WIN_LINES = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
THUMBNAIL = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQL00_5G8vrtl5R7xEmjiej1Sq3SCta25Pr8Q&usqp=CAU"


class TicTacToeGame:
    def __init__(self, player1: discord.Member, player2: discord.Member) -> None:
        self.players = (player1, player2)
        self.board: list[str | None] = [None] * 9
        self.turn = 0

    @property
    def current(self) -> discord.Member:
        return self.players[self.turn]

    @property
    def mark(self) -> str:
        return MARKS[self.turn]

    def is_free(self, cell: int) -> bool:
        return 0 <= cell < 9 and self.board[cell] is None

    def place(self, cell: int) -> None:
        self.board[cell] = self.mark

    def has_won(self) -> bool:
        return any(all(self.board[i] == self.mark for i in line) for line in WIN_LINES)

    def is_full(self) -> bool:
        return None not in self.board

    def next_turn(self) -> None:
        self.turn = 1 - self.turn

    def render(self) -> str:
        cells = [mark or CELL_NUMBERS[i] for i, mark in enumerate(self.board)]
        return "\n".join(" ".join(cells[row:row + 3]) for row in range(0, 9, 3))


class TicTacToe(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.games: dict[int, TicTacToeGame] = {}  # channel id -> game

    @commands.command(aliases=["ttt"], help="Start a game of Tic-Tac-Toe against someone.")
    @commands.guild_only()
    async def tictactoe(self, ctx: commands.Context, opponent: discord.Member) -> None:
        if ctx.channel.id in self.games:
            await ctx.send("A Tic-Tac-Toe game is already running in this channel. Finish it first.")
            return
        if error := opponent_error(ctx, [opponent]):
            await ctx.send(error)
            return

        game = self.games[ctx.channel.id] = TicTacToeGame(ctx.author, opponent)
        p = ctx.clean_prefix
        await ctx.send(embed=rules_embed(
            "Tic-Tac-Toe",
            "Scratch your brain. No luck.",
            "Get three in a row to win. The first player is X and the second is O. "
            "Players take turns until someone has three in a row or all nine squares are filled.",
            f"Each square is numbered 1 to 9. Mark one with `{p}fill <number>`. Give up with `{p}quit_tictactoe`.",
            THUMBNAIL,
        ))
        await ctx.send(game.render())
        await ctx.send(f"{game.current.mention} ({MARKS[0]}) goes first!")

    @commands.command(aliases=["place"], help="Mark a square (1-9) in your Tic-Tac-Toe game.")
    @commands.guild_only()
    async def fill(self, ctx: commands.Context, square: int) -> None:
        game = self.games.get(ctx.channel.id)
        if game is None:
            await ctx.send(f"No game here. Start one with `{ctx.clean_prefix}tictactoe @player`.")
            return
        if ctx.author != game.current:
            await ctx.send("Wait for your turn!" if ctx.author in game.players else "You're not playing this game.")
            return
        if not game.is_free(square - 1):
            await ctx.send("Choose a number from 1 to 9 for a square that isn't marked yet.")
            return

        game.place(square - 1)
        await ctx.send(game.render())

        if game.has_won():
            del self.games[ctx.channel.id]
            await ctx.send(f"{game.mark} {game.current.mention} wins! :tada:")
        elif game.is_full():
            del self.games[ctx.channel.id]
            await ctx.send("It's a tie!")
        else:
            game.next_turn()
            await ctx.send(f"Your turn, {game.current.mention} ({game.mark}).")

    @commands.command(aliases=["quittictactoe", "quit_ttt"], help="End the Tic-Tac-Toe game in this channel.")
    @commands.guild_only()
    async def quit_tictactoe(self, ctx: commands.Context) -> None:
        game = self.games.get(ctx.channel.id)
        if game is None:
            await ctx.send(f"No game is running. Start one with `{ctx.clean_prefix}tictactoe @player`.")
        elif not can_end_game(ctx, game.players):
            await ctx.send("Only the players (or a moderator) can end this game.")
        else:
            del self.games[ctx.channel.id]
            await ctx.send(f"The game has ended. Play again with `{ctx.clean_prefix}tictactoe @player`.")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(TicTacToe(bot))
