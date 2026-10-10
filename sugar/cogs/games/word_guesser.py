"""Guess the Word: a hangman-style game where the vowels are given for free. One game per channel."""

from __future__ import annotations

import random

import discord
from discord.ext import commands

from sugar.config import DATA_DIR
from sugar.utils import load_lines, rules_embed

VOWELS = frozenset("aeiou")
CONSONANTS = frozenset("bcdfghjklmnpqrstvwxyz")
MAX_WRONG_GUESSES = 6
HIDDEN = ":white_large_square:"
THUMBNAIL = (
    "https://lh3.googleusercontent.com/Zx2bYc6anwawINc4OtTNcvav605vEdRSehu0uy_FyyCq3itAcQnv7POiG10jNSvo9xczjl1X1Jm"
    "SQqOLoJx3DgCSgw=w640-h400-e365-rj-sc0x00ffffff"
)


def letter_emoji(letter: str) -> str:
    return f":regional_indicator_{letter}:"


class WordGame:
    def __init__(self, word: str) -> None:
        self.word = word
        self.guessed: set[str] = set()
        self.wrong_guesses = 0

    @property
    def lives(self) -> int:
        return MAX_WRONG_GUESSES - self.wrong_guesses

    def guess(self, letter: str) -> bool:
        """Record a guess and return whether the letter is in the word."""
        self.guessed.add(letter)
        if letter in self.word:
            return True
        self.wrong_guesses += 1
        return False

    def is_solved(self) -> bool:
        return all(c in VOWELS or c in self.guessed for c in self.word)

    def masked(self) -> str:
        return " ".join(letter_emoji(c) if c in VOWELS or c in self.guessed else HIDDEN for c in self.word)

    def revealed(self) -> str:
        return " ".join(letter_emoji(c) for c in self.word)

    def wrong_letters(self) -> str:
        return ", ".join(sorted(self.guessed - set(self.word))) or "none"


class WordGuesser(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        words = load_lines(DATA_DIR / "text" / "words.txt")
        self.words = [w.lower() for w in words if w.isascii() and w.isalpha()]
        self.games: dict[int, WordGame] = {}  # channel id -> game

    def status_embed(self, game: WordGame, title: str, colour: discord.Colour) -> discord.Embed:
        embed = discord.Embed(title=title, description=game.masked(), colour=colour)
        embed.set_footer(text=f"Lives left: {game.lives} | Wrong letters: {game.wrong_letters()}")
        return embed

    @commands.command(aliases=["wg", "word_guesser", "wordgusser", "hangman"], help="Start a word guessing game.")
    @commands.guild_only()
    async def wordguesser(self, ctx: commands.Context) -> None:
        if ctx.channel.id in self.games:
            await ctx.send("A word game is already running in this channel. Finish it first.")
            return

        game = self.games[ctx.channel.id] = WordGame(random.choice(self.words))
        p = ctx.clean_prefix
        await ctx.send(embed=rules_embed(
            "Guess The Word",
            "Scratch your head till you get it.",
            f"The vowels are already filled in. Guess the consonants before you make {MAX_WRONG_GUESSES} wrong guesses. "
            "Anyone in the channel can guess.",
            f"Use `{p}guess <letter>` to guess a consonant. Give up with `{p}quit_wordguesser`.",
            THUMBNAIL,
        ))
        await ctx.send(embed=self.status_embed(game, "Guess this word", discord.Colour.random()))

    @commands.command(aliases=["g"], help="Guess a consonant in the word game.")
    @commands.guild_only()
    async def guess(self, ctx: commands.Context, letter: str) -> None:
        game = self.games.get(ctx.channel.id)
        if game is None:
            await ctx.send(f"No word game here. Start one with `{ctx.clean_prefix}wordguesser`.")
            return

        letter = letter.lower()
        if letter in VOWELS:
            await ctx.send("Vowels are already given. Guess a consonant.")
            return
        if letter not in CONSONANTS:
            await ctx.send("Please guess a single consonant (a letter that isn't a vowel).")
            return
        if letter in game.guessed:
            await ctx.send(f"`{letter}` has already been guessed.")
            return

        correct = game.guess(letter)
        if game.is_solved():
            del self.games[ctx.channel.id]
            await ctx.send(embed=self.status_embed(game, f"{ctx.author.display_name} guessed the word! You win!", discord.Colour.green()))
        elif game.lives == 0:
            del self.games[ctx.channel.id]
            embed = discord.Embed(title="You lost!", description=f"The word was\n{game.revealed()}", colour=discord.Colour.red())
            await ctx.send(embed=embed)
        elif correct:
            await ctx.send(embed=self.status_embed(game, f"Yes, `{letter}` is in the word!", discord.Colour.green()))
        else:
            await ctx.send(embed=self.status_embed(game, f"Nope, no `{letter}`.", discord.Colour.red()))

    @commands.command(aliases=["qwg", "quitwordguesser", "quitwordgusser"], help="End the word game in this channel.")
    @commands.guild_only()
    async def quit_wordguesser(self, ctx: commands.Context) -> None:
        game = self.games.pop(ctx.channel.id, None)
        if game is None:
            await ctx.send(f"No word game is running. Start one with `{ctx.clean_prefix}wordguesser`.")
        else:
            await ctx.send(f"The game has ended. The word was **{game.word}**. Play again with `{ctx.clean_prefix}wordguesser`.")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(WordGuesser(bot))
