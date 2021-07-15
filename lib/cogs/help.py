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
            embed.add_field(name=":musical_note:**Music**", value="`~play`\n`~pause`\n`~skip`\n`~leave`\n`~queue`\n`~resume`\n`~join`\n`~remove`\n`~clear`\n`~currentsong`", inline=True)
            embed.add_field(name=":video_game:**Games**", value="`~tictactoe`\n`~race`\n`~miniLudo`\n`~wordGusser`\n`~wordGuesser`", inline=True)
            embed.add_field(name=":performing_arts:**Gif**", value="`~slap`\n`~cry`\n`~hug`\n`~dance`\n`~shrug`\n`~wakeup`\n`~laugh`\n`~fakelaugh`\n`~blush`", inline=True)
            embed.add_field(name=":placard:**Meme**", value="`~meme`\n`~meme dank`\n`~meme casual`", inline=True)
            embed.add_field(name=":jigsaw:**Fun**", value="`~praise`\n`~roast`\n`~spam`", inline=True)
            await ctx.send(embed=embed)
        else:
            if args in ['Games','games','Game','game']:
                embed=discord.Embed(title=':video_game: Games', description='Info of how to play is given in the command itself', colour=discord.Color.random(seed=None))
                embed.add_field(name='Tic-Tac-Toe', value='`~tictactoe <@mention>`\n can be played between two players')
                embed.add_field(name='Car Racing', value='`~race <@mention>`\n can be played between two players')
                embed.add_field(name='Ludo', value='`~miniLudo <@mention>`\n can be played between two to four players')
                embed.add_field(name='Hangsman', value='`~wordGusser`\n single player word guessing game.')
                await ctx.send(embed=embed)
            elif args in ['GIF','gif','Gif']:
                embed=discord.Embed(title=':performing_arts: Gif', colour=discord.Color.random(seed=None))
                embed.add_field(name='Slap', value='`~slap <@mention>`\n to slap someone.')
                embed.add_field(name='Hug', value='`~hug <@mention>`\n to hug someone.')
                embed.add_field(name='Cry', value='`~cry <@mention>`\n to cry with someone.')
                embed.add_field(name='Blush', value='`~blush <@mention>`\n to blush from someone.')
                embed.add_field(name='Laugh', value='`~laugh <@mention>`\n to laugh on someone.')
                embed.add_field(name='Fake Laugh', value='`~fakelaugh <@mention>`\n to do fake laugh for someone.')
                embed.add_field(name='Dance', value='`~dance <@mention>`\n to dance with someone.')
                embed.add_field(name='Shrug', value='`~shrug <@mention>`\n to shrug for someone.')
                embed.add_field(name='Wake Up', value='`~wakeup <@mention>`\n to wake up someone.')
                await ctx.send(embed=embed)
            elif args in ['Music','music']:
                embed=discord.Embed(title=':musical_note: Music', colour=discord.Color.random(seed=None))
                embed.add_field(name='Play Song', value='`~play (song name)`\n to play song and add song to queue.')
                embed.add_field(name='Join VC', value='`~join`\n to join voice channel.')
                embed.add_field(name='Pause', value='`~pause`\n to pause music.')
                embed.add_field(name='Resume', value='`~resume`\n to resume paused song.')
                embed.add_field(name='Queue', value='`~queue`\n to view playlist.')
                embed.add_field(name='Now Playing', value='`~cp`\n to view the currntly palying song.')
                embed.add_field(name='Leave VC', value='`~leave`\n to leave voice channel.')
                embed.add_field(name='Clear Playlist', value='`~clear`\n to clear playlist.')
                embed.add_field(name='Skip', value='`~skipr`\n to skip the currnt song.')
                embed.add_field(name='Remove Playlist', value='`~remove (song number)`\n to remove specific song from playlist.')
                await ctx.send(embed=embed)
            elif args in ['Meme','meme','MeMe']:
                embed=discord.Embed(title=':placard: Meme', colour=discord.Color.random(seed=None))
                embed.add_field(name='Random Meme', value='`~meme`\n sends a random meme')
                embed.add_field(name='Dank Meme', value='`~meme dank`\n sends a dank meme')
                embed.add_field(name='Casual Meme', value='`~meme casual`\n sends a casual meme')
                await ctx.send(embed=embed)
            elif args in ['Fun','fun']:
                embed=discord.Embed(title=':jigsaw: Fun', colour=discord.Color.random(seed=None))
                embed.add_field(name='Praise', value='`~praise`\n to prase someone')
                embed.add_field(name='Roast', value='`~roast`\n to roast someone')
                embed.add_field(name='Spam', value='`~spam`\n to spam')
                await ctx.send(embed=embed)
            else:
                await ctx.send("That section does not exist.")

def setup(bot):
    bot.add_cog(Help(bot))