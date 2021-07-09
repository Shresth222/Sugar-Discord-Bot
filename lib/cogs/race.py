import discord
from discord.ext import commands
import random

#global variable for race
race_player1=""
race_player2=""
race_board1=[]
race_board2=[]
race_decorator=[]
race_gameover=True
race_sum_player1=0
race_sum_player2=0
race_turn=""
race_dice=[1,2,3,4]


class Race(commands.Cog):

    def __init__(self,client):
        self.client = client
        

    @commands.Cog.listener()
    async def on_ready(self):
        print("Race cog is ready.")

    #code for race game
    #starting the race game, i.e., '~race'
    @commands.command()
    async def race(self, ctx, p2:discord.Member):
        #calling all the global variable
        global race_player1
        global race_player2
        global race_board1
        global race_board2
        global race_gameover
        global race_turn
        global race_decorator
        global race_sum_player1
        global race_sum_player2
        if race_gameover :
            race_player2=p2              #initializing player2
            race_player1=ctx.author      #initializing player1
            race_gameover=False
            race_sum_player1=0
            race_sum_player2=0
            race_turn=""
            race_board1=[":red_car:",":white_large_square:", ":white_large_square:", ":white_large_square:",":white_large_square:", ":white_large_square:", ":white_large_square:",":white_large_square:", ":white_large_square:", ":white_large_square:",":white_large_square:", ":white_large_square:", ":white_large_square:",":fireworks:"]
            race_board2=[":blue_car:"]+race_board1[1:]
            race_decorator=[":vertical_traffic_light:",":mountain:",":mountain_snow:",":mount_fuji:",":mountain:",":mountain_snow:",":mount_fuji:",":mountain:",":mountain_snow:",":mount_fuji:",":mountain:",":mountain_snow:",":mount_fuji:",":fireworks:"]
            embed=discord.Embed(title="Roll and Race",description="Luck is all that you need.",colour=discord.Color.random(seed=None))
            embed.add_field(name="Rules to play :",value="Finish this race of luck by rolling the dice having number 1 to 4 alternatively. One who takes less number of roll wins the race. If both took same number of roll then its a draw. ",inline=False)
            embed.add_field(name="How to Play :",value="Use command `~drive` alternatively to roll the dice and move the car")      
            embed.set_thumbnail(url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTfPsDK1mJlpMKOV7A9CC7zDEOAW2W2HfKgtg&usqp=CAU')
            await ctx.send(embed=embed)
            line=""                 #prints the board
            for i in range(0,14):    #prints the board
                line=line + race_decorator[i]+" "+race_board1[i]+" "+race_board2[i]+" "+race_decorator[i] +"\n"
            await ctx.send(line)

            race_turn = race_player1           #giving first turn to starter of the game
            await ctx.send("First move will be played by <@" + str(race_player1.id) + "> who will drive the red car")   #if game is not finished the gameover will be false
        else:
            await ctx.send("A game is already in progress! Finish it before starting a new one.")         #game has began


    #for driving the car on alternate moves by the players
    @commands.command()
    async def drive(self, ctx):
        #calling all the global variable
        global race_player1
        global race_player2
        global race_board1
        global race_board2
        global race_sum_player1
        global race_sum_player2
        global race_gameover
        global race_turn
        global race_decorator
        global race_dice
        if not(race_gameover):    #game continues
            mark=""
            if race_turn == ctx.author:      #checks whethaer the correct player is marking
                dice=random.choice(race_dice)
                if race_turn == race_player1 :    #assigning cross to player
                    if (race_sum_player1+dice) <14 :
                        race_board1[race_sum_player1]=":white_large_square:"
                        race_sum_player1 += dice
                        race_board1[race_sum_player1]=":red_car:"
                        race_turn = race_player2
                    else:
                        race_turn = race_player2
                        await ctx.send("Stop there!!Don't cross the finish line.")
                else:                      
                    if (race_sum_player2+dice) <14 :
                        race_board2[race_sum_player2]=":white_large_square:"
                        race_sum_player2 += dice
                        race_board2[race_sum_player2]=":blue_car:"
                        race_turn = race_player1
                    else:
                        race_turn = race_player1
                        await ctx.send("Stop there!!Don't cross the finish line. Wait for next move")
                    if race_sum_player1==race_sum_player2==13:
                        await ctx.send("The race has tied")
                        race_gameover=True
                    elif race_sum_player2==13:
                        await ctx.send(f'{race_player2.mention} has won the race')
                        race_gameover=True
                    elif race_sum_player1==13:
                        await ctx.send(f'{race_player1.mention} has won the race')
                        race_gameover=True
                line=""
                for i in range(0,14):    #prints the board
                    line+=race_decorator[i]+" "+race_board1[i]+" "+race_board2[i]+" "+race_decorator[i] +"\n"
                await ctx.send(line)
            else:                                           #wrong person was trying to play
                await ctx.send("Wait for your turn!")
        else:                                               #the game has ended
            await ctx.send("Please start a new game using the ~race command.")


    #resetting the game
    @commands.command()
    async def quit_race(self, ctx):
        global race_player1
        global race_player2
        global race_board1
        global race_board2
        global race_sum_player1
        global race_sum_player2
        global race_gameover
        global race_turn
        global race_decorator
        global race_dice
        if race_gameover:
            await ctx.send("The game is not being played. To play enter the command `~race`")
        else:
            race_player1=""
            race_player2=""
            race_board1=[]
            race_board2=[]
            race_decorator=[]
            race_gameover=True
            race_sum_player1=0
            race_sum_player2=0
            race_turn=""
            race_dice=[1,2,3,4]
            await ctx.send("The game has ended. To play again enter the commmand `~race`")

    @race.error
    async def race_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please mention 1 players for this command.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please make sure to mention/ping players (ie. <@688534433879556134>).")

def setup(client):
    client.add_cog(Race(client))