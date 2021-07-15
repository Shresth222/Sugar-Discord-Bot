from typing import Optional
import discord
from discord import colour
from discord.utils import get
from discord.ext import commands

class Help(commands.Cog):

    def __init__(self,bot):
        self.bot = bot
        self.bot.remove_command("help")

    @commands.Cog.listener()
    async def on_ready(self):
        print("Help cog is ready.")

    @commands.command()
    async def help(self, ctx, args=None):
        if args is None :
            embed=discord.Embed(title=":heart_exclamation: Bot's Commands :heart_exclamation: ",description="`You can know about each section by using '~help (section_name)'.`", colour=discord.Color.random(seed=None))
            embed.add_field(name=":musical_note:**Music**", value="`~play`\n`~pause`\n`~skip`\n`~quit`", inline=True)
            embed.add_field(name=":video_game:**Games**", value="`~tictactoe`\n`~race`\n`~miniLudo`\n`~wordGusser`", inline=True)
            embed.add_field(name=":jigsaw:**Fun**", value="`~roast`\n`~praise`\n`~disturb`", inline=True)
            await ctx.send(embed=embed)
        else:
            if args in ['Games','games','Game','game']:
                embed=discord.Embed(title=':video_game: Games', description='Info of how to play is given in the command itself', colour=discord.Color.random(seed=None))
                embed.add_field(name='Tic-Tac-Toe', value='`~tictactoe <@mention>`\n can be played between two players')
                embed.add_field(name='Car Racing', value='`~race <@mention>`\n can be played between two players')
                embed.add_field(name='Ludo', value='`~miniLudo <@mention>`\n can be played between two to four players')
                embed.add_field(name='Hangsman', value='`~wordGusser`\n single player word guessing game.')
                await ctx.send(embed=embed)
            else:
                await ctx.send("That section does not exist.")

def setup(bot):
    bot.add_cog(Help(bot))