# SUGAR - Discord Bot
This is my first Discord bot, "Sugar". This is a fun bot with many features. Using this bot you can play games, play music, send GIFs, read memes and more.

## Setup

1. **Python 3.10+** and **[FFmpeg](https://ffmpeg.org/download.html)** (needed for music; it must be on your `PATH`).
2. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a bot in the [Discord Developer Portal](https://discord.com/developers/applications). Under **Bot**, turn on **Message Content Intent**.
4. Copy `.env.example` to `.env` and fill in your values:
   | Variable | Required | Purpose |
   | --- | --- | --- |
   | `DISCORD_TOKEN` | yes | Your bot token |
   | `BOT_PREFIX` | no | Command prefix (default `~`) |
   | `GIPHY_API_KEY` | for GIFs | [Giphy API key](https://developers.giphy.com/) |
   | `REDDIT_CLIENT_ID` / `REDDIT_CLIENT_SECRET` | for memes | [Reddit app](https://www.reddit.com/prefs/apps) credentials |
5. Run the bot:
   ```
   python main.py
   ```

> Never commit your `.env` file. It is already listed in `.gitignore`.

## Project structure
```
main.py                     entry point
sugar/
  bot.py                    bot class, extension loading, global error handling
  config.py                 settings read from the environment / .env
  utils.py                  shared helpers
  cogs/
    help.py  fun.py  gifs.py  memes.py  music.py
    games/
      tictactoe.py  race.py  ludo.py  word_guesser.py
data/text/                  praises, roasts and word list
```

## Commands
Use `~help` to see everything in Discord, or `~help <section>` (`music`, `games`, `gif`, `meme`, `fun`) for details.

| Section | Commands |
| --- | --- |
| Games | `~tictactoe @player`, `~race @player`, `~ludo @player [@player @player]`, `~wordguesser` |
| Music | `~play <song>`, `~pause`, `~resume`, `~skip`, `~queue`, `~nowplaying`, `~remove <n>`, `~clear`, `~volume <0-100>`, `~join`, `~leave` |
| GIF | `~slap`, `~hug`, `~wakeup` (need a mention); `~cry`, `~dance`, `~shrug`, `~blush`, `~laugh`, `~fakelaugh` (mention optional) |
| Meme | `~meme`, `~meme dank`, `~meme casual` |
| Fun | `~praise @member`, `~roast @member`, `~spam <times> <message>` (max 10, once a minute) |

Every game runs per channel, so different channels and servers can play at the same time.

## Games Description
### Tic-Tac-Toe
Use `~tictactoe @player` to play this game.
Scratch your brain with no luck.

![image](https://github.com/Shresth222/Bot_Creation/assets/79076392/97898d9a-1366-41e9-966e-0af14a156864)
#### How to Play
The object of Tic Tac Toe is to get three in a row. The first player is X and the second is O. Players take turns placing X's and O's until one of them has three in a row or all nine squares are filled.
Each square is numbered 1 to 9. Mark a square with `~fill <number>`. End the game with `~quit_tictactoe`.

### Car Race
Use `~race @player` to play this game.
Luck is all you need.

![image](https://github.com/Shresth222/Bot_Creation/assets/79076392/cbb21c0a-c81c-4155-97dc-8dbfb22d02d0)

#### How to Play
Take turns rolling a die numbered 1 to 4 with `~drive`. You must land exactly on the finish line. Whoever gets there in fewer rolls wins. If both players need the same number of rolls, it's a draw. End the game with `~quit_race`.

### Ludo
Use `~ludo @player [@player @player]` to play this game with 2 to 4 players.
Luck with scratching your head.

![image](https://github.com/Shresth222/Bot_Creation/assets/79076392/e2a0ab2e-abaf-4c3a-b537-4eff0f549daa)

#### How to Play
Mostly normal Ludo rules, with a few changes. Each player has two pieces, and you need a 6 to bring a piece out. Rolling a 6 gives you another roll. Landing on an opponent sends their piece home, except on the :radioactive: start squares, which are safe. Both of your pieces can share a square, but if someone lands there, both go back home. You must reach the centre with an exact roll.
Use `~roll` to roll the die and `~move 1` or `~move 2` to choose a piece. If only one move is possible, it's made for you. Use `~pieces` to see which piece is which. End the game with `~quit_ludo`.

### Guess The Word
Use `~wordguesser` (or `~wg`) to play this game.
Scratch your head till you get it.

![image](https://github.com/Shresth222/Bot_Creation/assets/79076392/bf5bbf2f-97dc-4141-8293-f75f71b9c3ea)

#### How to Play
Like hangman. The vowels are already filled in, and you have to guess the consonants before making 6 wrong guesses. Anyone in the channel can guess.
Use `~guess <letter>` to guess a consonant. End the game with `~quit_wordguesser`.
