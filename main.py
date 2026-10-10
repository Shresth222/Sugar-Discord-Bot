"""Entry point for the Sugar Discord bot. Run with: python main.py"""

from sugar import config
from sugar.bot import SugarBot


def main() -> None:
    if not config.DISCORD_TOKEN:
        raise SystemExit("DISCORD_TOKEN is not set. Copy .env.example to .env and add your bot token.")

    bot = SugarBot()
    bot.run(config.DISCORD_TOKEN, root_logger=True)


if __name__ == "__main__":
    main()
