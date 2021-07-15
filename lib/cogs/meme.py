import discord
from discord.embeds import Embed
from discord.ext import commands
import random
import praw

reddit = praw.Reddit(
    client_id="--5isiCvN764L-bWjwl55Q",
    client_secret="5ow52U3hXUreA0-cVQWpyYNbD5V6qQ",
    user_agent="test bot by maniac0112",
    check_for_async=False
    )

dank_sub1=reddit.subreddit("IndianDankMemes")
dank_sub2=reddit.subreddit("desimemes")
cas_sub1=reddit.subreddit("school_memes")
cas_sub2=reddit.subreddit("engineeringmemes")
cas_sub3=reddit.subreddit("indianmemer")
cas_sub4=reddit.subreddit("ComedyCemetry")
sub=reddit.subreddit("Memes_Of_The_Dank")
dank_meme=[]
casual_meme=[]
meme=[]



class Meme(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Meme cog is ready.")


    @commands.command()
    async def meme(self, ctx, args=None):
        if args is None :
            await ctx.send(embed=self.memes())
        elif args in ['dank','Dank']:
            await ctx.send(embed=self.dank())
        elif args in ['casual','Casual']:
            await ctx.send(embed=self.casual())
        else:
            await ctx.send("Please send correct argument or no argument.")


    def dank(self):
        global dank_meme
        global dank_sub1
        global dank_sub2

        if len(dank_meme)<=1:
            print("Updating Dank meme list....") 
            for submission in dank_sub1.new(limit=30):
                dank_meme.append((submission.title,submission.url))
            for submission in dank_sub2.new(limit=30):
                dank_meme.append((submission.title,submission.url))

        while(True):
           Z=random.choice(dank_meme)
           dank_meme.pop(dank_meme.index(Z))
           if Z[1][-3:]=="jpg" or Z[1][-3:]=="png" or Z[1][-3:]=="gif":
               embed=discord.Embed(title=Z[0], color=discord.Color.random(seed=None)).set_image(url=Z[1])
               return embed
           else:
               pass


    def casual(self):
        global casual_meme
        global cas_sub1
        global cas_sub2
        global cas_sub3
        global cas_sub4

        if len(casual_meme)<=1:
            print("Updating Casual meme list....") 
            for submission in cas_sub1.hot(limit=10):
                casual_meme.append((submission.title,submission.url))
            for submission in cas_sub2.hot(limit=10):
                casual_meme.append((submission.title,submission.url))
            for submission in cas_sub3.hot(limit=10):
                casual_meme.append((submission.title,submission.url))
            for submission in cas_sub4.hot(limit=10):
                casual_meme.append((submission.title,submission.url))

        while(True):
            Z=random.choice(casual_meme)
            casual_meme.pop(casual_meme.index(Z))
            if Z[1][-3:]=="jpg" or Z[1][-3:]=="png" or Z[1][-3:]=="gif":
                embed=discord.Embed(title=Z[0], color=discord.Color.random(seed=None)).set_image(url=Z[1])
                return embed
            else:
                pass
    

    def memes(self):
        global meme
        global sub

        if len(meme)<=1:
            print("Updating meme list....") 
            for submission in sub.new(limit=40):
                meme.append((submission.title,submission.url))
 
        while(True):
           Z=random.choice(meme)
           meme.pop(meme.index(Z))
           if Z[1][-3:]=="jpg" or Z[1][-3:]=="png" or Z[1][-3:]=="gif":
               embed=discord.Embed(title=Z[0], color=discord.Color.random(seed=None)).set_image(url=Z[1])
               return embed
           else:
               pass


def setup(bot):
    bot.add_cog(Meme(bot))