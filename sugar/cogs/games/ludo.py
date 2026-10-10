"""Mini-Ludo: Ludo on a 7x7 board for 2-4 players with two pieces each. One game per channel.

Each piece has a *progress* value:
    AT_HOME (-1)  locked in its home square; a 6 unlocks it
    0             unlocked, still sitting on its home square
    1..26         on the board at colour.path[progress - 1]
    26            reached the centre (finished)
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field

import discord
from discord.ext import commands

from sugar.utils import can_end_game, opponent_error, rules_embed

BOARD_SIZE = 7
CENTRE = 24
PATH_LENGTH = 26
AT_HOME = -1
SAFE_CELLS = frozenset({11, 15, 33, 37})  # the start squares (:radioactive:) - no captures here
PIECE_LABELS = (":one:", ":two:")
STACKED_LABEL = ":1234:"
THUMBNAIL = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSCz6G7l37Q5Kx7fz0lUdFbSIY0qgPIi48VkQ&usqp=CAU"

W, S = ":white_large_square:", ":radioactive:"
GS, YS, RS, BS = ":green_square:", ":yellow_square:", ":red_square:", ":blue_square:"
# The empty board, row by row. Home squares are drawn as coloured squares; pieces are drawn on top.
BASE_BOARD = (
    GS, GS, W,  W,  W,  YS, YS,
    GS, GS, W,  YS, S,  YS, YS,
    W,  S,  W,  YS, W,  W,  W,
    W,  GS, GS, ":white_square_button:", BS, BS, W,
    W,  W,  W,  RS, W,  S,  W,
    RS, RS, S,  RS, W,  BS, BS,
    RS, RS, W,  W,  W,  BS, BS,
)


@dataclass(frozen=True)
class Colour:
    name: str
    piece: str
    homes: tuple[int, int]   # home square of piece 1 and piece 2
    path: tuple[int, ...]    # the PATH_LENGTH squares a piece travels, ending at the centre


RED = Colour("red", ":red_circle:", (36, 42),
             (37, 30, 29, 28, 21, 14, 15, 16, 9, 2, 3, 4, 11, 18, 19, 20, 27, 34, 33, 32, 39, 46, 45, 38, 31, 24))
BLUE = Colour("blue", ":blue_circle:", (40, 48),
              (33, 32, 39, 46, 45, 44, 37, 30, 29, 28, 21, 14, 15, 16, 9, 2, 3, 4, 11, 18, 19, 20, 27, 26, 25, 24))
YELLOW = Colour("yellow", ":yellow_circle:", (12, 6),
                (11, 18, 19, 20, 27, 34, 33, 32, 39, 46, 45, 44, 37, 30, 29, 28, 21, 14, 15, 16, 9, 2, 3, 10, 17, 24))
GREEN = Colour("green", ":green_circle:", (8, 0),
               (15, 16, 9, 2, 3, 4, 11, 18, 19, 20, 27, 34, 33, 32, 39, 46, 45, 44, 37, 30, 29, 28, 21, 22, 23, 24))

# Colours in turn order for each player count (2 players sit opposite each other).
SEATING = {
    2: (RED, YELLOW),
    3: (RED, BLUE, YELLOW),
    4: (RED, BLUE, YELLOW, GREEN),
}


@dataclass
class LudoPlayer:
    member: discord.Member
    colour: Colour
    pieces: list[int] = field(default_factory=lambda: [AT_HOME, AT_HOME])

    def cell(self, piece: int) -> int:
        progress = self.pieces[piece]
        return self.colour.homes[piece] if progress <= 0 else self.colour.path[progress - 1]

    def can_move(self, piece: int, roll: int) -> bool:
        progress = self.pieces[piece]
        if progress == AT_HOME:
            return roll == 6
        return progress + roll <= PATH_LENGTH

    def on_track(self, piece: int) -> bool:
        return 0 < self.pieces[piece] < PATH_LENGTH

    @property
    def finished(self) -> bool:
        return all(progress == PATH_LENGTH for progress in self.pieces)


@dataclass
class MoveResult:
    events: list[str]
    extra_turn: bool


class LudoGame:
    def __init__(self, members: list[discord.Member]) -> None:
        self.players = [LudoPlayer(member, colour) for member, colour in zip(members, SEATING[len(members)])]
        self.turn = 0
        self.roll: int | None = None  # set between rolling and moving
        self.ranking: list[LudoPlayer] = []

    @property
    def current(self) -> LudoPlayer:
        return self.players[self.turn]

    @property
    def members(self) -> list[discord.Member]:
        return [player.member for player in self.players]

    @property
    def is_over(self) -> bool:
        return len(self.ranking) == len(self.players)

    def player_for(self, member: discord.abc.User) -> LudoPlayer | None:
        return next((player for player in self.players if player.member == member), None)

    def roll_die(self) -> int:
        self.roll = random.randint(1, 6)
        return self.roll

    def movable_pieces(self) -> list[int]:
        return [piece for piece in (0, 1) if self.current.can_move(piece, self.roll)]

    def move(self, piece: int) -> MoveResult:
        player, roll = self.current, self.roll
        self.roll = None

        if player.pieces[piece] == AT_HOME:
            player.pieces[piece] = 0
            return MoveResult([f"Piece {piece + 1} is out! Roll again to move it."], extra_turn=True)

        player.pieces[piece] += roll
        events = []
        if player.pieces[piece] == PATH_LENGTH:
            events.append(f"Piece {piece + 1} reached the centre! :tada:")
        elif (cell := player.cell(piece)) not in SAFE_CELLS:
            events += self._capture(player, cell)

        if player.finished:
            self.ranking.append(player)
            events.append(f"{player.colour.piece} {player.member.mention} finished in place #{len(self.ranking)}!")
            unfinished = [p for p in self.players if not p.finished]
            if len(unfinished) == 1:
                self.ranking.append(unfinished[0])
            return MoveResult(events, extra_turn=False)

        return MoveResult(events, extra_turn=roll == 6)

    def _capture(self, mover: LudoPlayer, cell: int) -> list[str]:
        events = []
        for other in self.players:
            if other is mover:
                continue
            hit = [piece for piece in (0, 1) if other.on_track(piece) and other.cell(piece) == cell]
            for piece in hit:
                other.pieces[piece] = AT_HOME
            if hit:
                which = "both pieces" if len(hit) == 2 else f"piece {hit[0] + 1}"
                events.append(f"You sent {other.member.mention}'s {which} back home!")
        return events

    def advance_turn(self) -> None:
        self.roll = None
        for _ in self.players:
            self.turn = (self.turn + 1) % len(self.players)
            if not self.current.finished:
                return

    def render(self, highlight: LudoPlayer | None = None) -> str:
        """Draw the board. If `highlight` is given, that player's pieces are labelled 1 and 2."""
        cells = list(BASE_BOARD)
        for player in self.players:
            if player is highlight:
                continue
            for piece in (0, 1):
                if player.pieces[piece] != PATH_LENGTH:
                    cells[player.cell(piece)] = player.colour.piece

        if highlight:
            own = [highlight.cell(piece) for piece in (0, 1) if highlight.pieces[piece] != PATH_LENGTH]
            for piece in (0, 1):
                if highlight.pieces[piece] != PATH_LENGTH:
                    cell = highlight.cell(piece)
                    cells[cell] = STACKED_LABEL if own.count(cell) == 2 else PIECE_LABELS[piece]

        return "\n".join("".join(cells[row:row + BOARD_SIZE]) for row in range(0, BOARD_SIZE ** 2, BOARD_SIZE))


class Ludo(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.games: dict[int, LudoGame] = {}  # channel id -> game

    async def get_turn_game(self, ctx: commands.Context) -> LudoGame | None:
        """Return the channel's game if it's the author's turn; otherwise explain why not and return None."""
        game = self.games.get(ctx.channel.id)
        if game is None:
            await ctx.send(f"No Ludo game here. Start one with `{ctx.clean_prefix}ludo @player`.")
            return None
        if ctx.author != game.current.member:
            await ctx.send("It's not your turn. Please wait patiently." if game.player_for(ctx.author) else "You're not playing this game.")
            return None
        return game

    async def announce_turn(self, ctx: commands.Context, game: LudoGame) -> None:
        await ctx.send(f"Now it's {game.current.colour.piece} {game.current.member.mention}'s turn to `{ctx.clean_prefix}roll`.")

    async def end_turn(self, ctx: commands.Context, game: LudoGame) -> None:
        game.advance_turn()
        await self.announce_turn(ctx, game)

    async def do_move(self, ctx: commands.Context, game: LudoGame, piece: int) -> None:
        result = game.move(piece)
        await ctx.send("\n".join(result.events) + "\n" + game.render() if result.events else game.render())

        if game.is_over:
            del self.games[ctx.channel.id]
            standings = "\n".join(
                f"**#{place}** {player.colour.piece} {player.member.mention}" for place, player in enumerate(game.ranking, start=1)
            )
            await ctx.send(embed=discord.Embed(title="The match is over! Final leaderboard", description=standings, colour=discord.Colour.gold()))
        elif result.extra_turn:
            await ctx.send(f"Lucky you, {game.current.member.mention}! Roll again.")
        else:
            await self.end_turn(ctx, game)

    @commands.command(aliases=["miniludo", "mini_ludo"], help="Start Mini-Ludo with 1 to 3 other players.")
    @commands.guild_only()
    async def ludo(self, ctx: commands.Context, opponents: commands.Greedy[discord.Member]) -> None:
        if ctx.channel.id in self.games:
            await ctx.send("A Ludo game is already running in this channel. Finish it first.")
            return
        if not 1 <= len(opponents) <= 3:
            await ctx.send(f"Mention 1 to 3 players to play with, e.g. `{ctx.clean_prefix}ludo @friend`.")
            return
        if error := opponent_error(ctx, opponents):
            await ctx.send(error)
            return

        game = self.games[ctx.channel.id] = LudoGame([ctx.author, *opponents])
        p = ctx.clean_prefix
        await ctx.send(embed=rules_embed(
            "Mini-Ludo",
            "Luck, plus a bit of head-scratching.",
            "Mostly normal Ludo rules. Each player has two pieces, and you need a 6 to bring a piece out. "
            "Rolling a 6 gives you another roll. Land on an opponent to send them home, except on the "
            ":radioactive: start squares, which are safe. Both of your pieces can share a square, but if "
            "someone lands there, both go home. You must land on the centre with an exact roll.",
            f"`{p}roll` to roll the die, then `{p}move 1` or `{p}move 2` to choose a piece. "
            f"`{p}pieces` shows which piece is which. Give up with `{p}quit_ludo`.",
            THUMBNAIL,
        ))
        await ctx.send(game.render())
        await ctx.send("\n".join(f"{player.colour.piece} {player.member.mention} is **{player.colour.name}**" for player in game.players))
        await self.announce_turn(ctx, game)

    @commands.command(help="Roll the die in your Ludo game.")
    @commands.guild_only()
    async def roll(self, ctx: commands.Context) -> None:
        game = await self.get_turn_game(ctx)
        if game is None:
            return
        if game.roll is not None:
            await ctx.send(f"You've already rolled a **{game.roll}**. Use `{ctx.clean_prefix}move 1` or `{ctx.clean_prefix}move 2`.")
            return

        roll = game.roll_die()
        movable = game.movable_pieces()
        await ctx.send(f"{game.current.colour.piece} You rolled a **{roll}** :game_die:")

        if not movable:
            await ctx.send("None of your pieces can move with that roll.")
            await self.end_turn(ctx, game)
        elif len({game.current.pieces[piece] for piece in movable}) == 1:
            # Only one real choice (one piece movable, or both in the same spot): move automatically.
            await self.do_move(ctx, game, movable[0])
        else:
            await ctx.send(f"Choose a piece: `{ctx.clean_prefix}move 1` or `{ctx.clean_prefix}move 2`.")

    @commands.command(help="Move piece 1 or 2 after rolling in Ludo.")
    @commands.guild_only()
    async def move(self, ctx: commands.Context, piece: int) -> None:
        game = await self.get_turn_game(ctx)
        if game is None:
            return
        if game.roll is None:
            await ctx.send(f"Roll first with `{ctx.clean_prefix}roll`.")
            return
        if piece not in (1, 2):
            await ctx.send("Choose piece 1 or 2.")
            return
        if piece - 1 not in game.movable_pieces():
            await ctx.send("That piece can't move with this roll. Move the other one.")
            return
        await self.do_move(ctx, game, piece - 1)

    @commands.command(aliases=["mypieces", "my_pieces"], help="Show where your Ludo pieces are.")
    @commands.guild_only()
    async def pieces(self, ctx: commands.Context) -> None:
        game = self.games.get(ctx.channel.id)
        player = game.player_for(ctx.author) if game else None
        if player is None:
            await ctx.send("You're not in a Ludo game in this channel.")
            return
        await ctx.send(f"Here are your pieces, {ctx.author.mention} ({player.colour.piece}):\n{game.render(highlight=player)}")

    @commands.command(aliases=["quitludo", "quit_miniludo", "quitminiludo"], help="End the Ludo game in this channel.")
    @commands.guild_only()
    async def quit_ludo(self, ctx: commands.Context) -> None:
        game = self.games.get(ctx.channel.id)
        if game is None:
            await ctx.send(f"No Ludo game is running. Start one with `{ctx.clean_prefix}ludo @player`.")
        elif not can_end_game(ctx, game.members):
            await ctx.send("Only the players (or a moderator) can end this game.")
        else:
            del self.games[ctx.channel.id]
            await ctx.send(f"The game has ended. Play again with `{ctx.clean_prefix}ludo @player`.")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Ludo(bot))
