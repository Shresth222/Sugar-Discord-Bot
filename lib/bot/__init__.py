from discord.ext.commands import Bot as BotBase
from discord.ext import commands
import os

PRIFIX = "~"

class Bot(BotBase):

    def __init__(self):
        self.PRIFIX = PRIFIX
        super().__init__(command_prefix=PRIFIX)

    def setup(self):
        for filename in os.listdir("./lib/cogs"):
            if filename.endswith('.py'):
                super().load_extension(f'lib.cogs.{filename[:-3]}')
                print(f'cogs.{filename} cog loaded')
        
        print("setup completed")

    def run(self):

        print("running setup")
        self.setup()

        with open("./lib/bot/token.txt", "r") as t:
            self.TOKEN = t.readlines()[0].strip()

        print("running bot...")
        super().run(self.TOKEN)

    async def on_connect(self):
        print("Bot connected")

    async def on_disconnect(self):
        print("Bot disconnected")

    async def on_ready(self):
        print("Hello I am ready")

    
client=Bot()










    