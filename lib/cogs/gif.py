import discord
from discord.ext import commands
import random
import requests

url = "http://api.giphy.com/v1/gifs/search"
key="RdeOyxVKcwiuOcV1L06EC0ZrNdZYGxOL"


class Gif(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Gif cog is ready.")

    @commands.command()
    async def slap(self, ctx, p2:discord.Member):
        x=ctx.author.display_name
        y=p2.display_name
        await ctx.channel.send(embed=self.gif("slap",x,y))
    
    @commands.command()
    async def wakeup(self, ctx, p2:discord.Member):
        x=ctx.author.display_name
        y=p2.display_name
        await ctx.channel.send(embed=self.gif("wakeup",x,y))

    @commands.command()
    async def hug(self, ctx, p2:discord.Member):
        x=ctx.author.display_name
        y=p2.display_name
        await ctx.channel.send(embed=self.gif("hug",x,y))

    @commands.command()
    async def cry(self, ctx, p2:discord.Member):
        x=ctx.author.display_name
        y=p2.display_name
        await ctx.channel.send(embed=self.gif("cry",x,y))
    
    @commands.command()
    async def dance(self, ctx, p2:discord.Member):
        x=ctx.author.display_name
        y=p2.display_name
        await ctx.channel.send(embed=self.gif("dance",x,y))
    
    @commands.command()
    async def shrug(self, ctx, p2:discord.Member):
        x=ctx.author.display_name
        y=p2.display_name
        await ctx.channel.send(embed=self.gif("shrug",x,y))

    @commands.command()
    async def blush(self, ctx, p2:discord.Member):
        x=ctx.author.display_name
        y=p2.display_name
        await ctx.channel.send(embed=self.gif("blush",x,y))

    @commands.command()
    async def laugh(self, ctx, p2:discord.Member):
        x=ctx.author.display_name
        y=p2.display_name
        await ctx.channel.send(embed=self.gif("laugh",x,y))

    @commands.command()
    async def fakelaugh(self, ctx, p2:discord.Member):
        x=ctx.author.display_name
        y=p2.display_name
        await ctx.channel.send(embed=self.gif("fakelaugh",x,y))


    def gif(self,id,x,y):
        title=[["Oooof! **"+x+"** slaps **"+y+"** !!", "Ouch! **"+y+"** got smashed by **" + x+"**", "**"+x + "** lands a mighty blow on **"+y+"**!!"],
                ["**"+x+"** wakes " +"**"+y+"** up!!"],["**"+x+"** hugs **"+y+"**"],["**"+x+"** is sad ;_;","**"+x+"** cries ;_;"],["**"+x+"** is _vibing_","**"+x+"** dances!"],
                ["**"+x+"** shrugs"],["**"+x+"** is blushing ^>^" ],["Shhh! **"+x+"** is sleeping!" ],["LOL! **"+x+ "** can't stop laughing", "HAHAHAHA!!!!!!! **"+x+ "** can't stop laughing", "XD **"+x+ "** can't stop laughing" ]
                ]
        dictionary={"slap":["anime slap",title[0]],
        "wakeup":["anime wake up", title[1]],
        "hug":["anime hug",title[2]],
        "cry":["anime cry",title[3]],
        "dance":["anime dance",title[4]],
        "shrug":["shrug",title[5]],
        "blush":["anime blush",title[6]],
        "laugh":["anime laugh",title[7]],
        "fakelaugh":["fakelaugh",title[7]]
                    }
        payload={
            "q":dictionary[id][0],
            "api_key":key,
            "limit":"30"
            }
        r = requests.get(url, params=payload)
        gif=random.choice(r.json()["data"])["id"]
        gif_url="https://media.giphy.com/media/"+gif+"/giphy.gif"
        embed=discord.Embed(title=random.choice(dictionary[id][1]) , color=discord.Color.random(seed=None)).set_image(url=gif_url)
        return embed

    @slap.error
    async def slap_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please mention 1 person for this command.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please make sure to mention/ping person (ie. <@688534433879556134>).")

    @wakeup.error
    async def wakeup_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please mention 1 person for this command.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please make sure to mention/ping person (ie. <@688534433879556134>).")

    @hug.error
    async def hug_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please mention 1 person for this command.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please make sure to mention/ping person (ie. <@688534433879556134>).")

    @cry.error
    async def cry_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please mention 1 person for this command.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please make sure to mention/ping person (ie. <@688534433879556134>).")

    @dance.error
    async def dance_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please mention 1 person for this command.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please make sure to mention/ping person (ie. <@688534433879556134>).")

    @shrug.error
    async def shrug_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please mention 1 person for this command.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please make sure to mention/ping person (ie. <@688534433879556134>).")

    @blush.error
    async def blush_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please mention 1 person for this command.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please make sure to mention/ping person (ie. <@688534433879556134>).")

    @laugh.error
    async def laugh_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please mention 1 person for this command.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please make sure to mention/ping person (ie. <@688534433879556134>).")

    @fakelaugh.error
    async def fakelaugh_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please mention 1 person for this command.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please make sure to mention/ping person (ie. <@688534433879556134>).")


def setup(bot):
    bot.add_cog(Gif(bot))