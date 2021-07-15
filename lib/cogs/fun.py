
import discord
from discord import channel
from discord.embeds import Embed
from discord.ext import commands
import random

Praises=[]
Roasts=[]
with open("./data/text/praises.txt") as f:
     Praises = f.readlines()
with open("./data/text/roasts.txt") as f:
     Roasts = f.readlines()


class Fun(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Fun cog is ready.")

    @commands.command()
    async def praise(self, ctx, member:discord.Member):
        global Praises
        embed=discord.Embed(title="Dear **"+ member.display_name+"**, ", description=random.choice(Praises)+"\n \n **regards,** \n _"+ctx.author.display_name+"_", color=discord.Color.random(seed=None))
        await ctx.send(embed=embed)

    @commands.command()
    async def roast(self, ctx, member:discord.Member):
        global Roasts
        embed=discord.Embed(title="Dear **"+ member.display_name+"**, ", description=random.choice(Roasts)+"\n \n **regards,** \n _"+ctx.author.display_name+"_", color=discord.Color.random(seed=None))
        await ctx.send(embed=embed)

    @commands.command()
    async def spam(self, ctx, *args):
        channel = self.bot.get_channel(818490760038055960)
        for i in range (100):
            await channel.send(args[0])

    @roast.error
    async def roast_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please mention 1 person for this command.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please make sure to mention/ping person (ie. <@688534433879556134>).")

    @praise.error
    async def praise_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please mention 1 person for this command.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please make sure to mention/ping person (ie. <@688534433879556134>).")

def setup(bot):
    bot.add_cog(Fun(bot))