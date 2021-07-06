import discord
from discord.ext import commands

tictactoe_player1=""
tictactoe_player2=""
tictactoe_board=[]
tictactoe_gameover=True
tictactoe_turn=""
tictactoe_count=0
tictactoe_wining_condition=[[0,1,2],[3,4,5],[6,7,8],[0,4,8],[2,4,6],[0,3,6],[1,4,7],[2,5,8]]


class Ticktactoe(commands.Cog):

    def __init__(self,client):
        self.client = client
        

    @commands.Cog.listener()
    async def on_ready(self):
        print("tictactoe cog is ready.")


    @commands.command()
    async def tictactoe(self, ctx, p2:discord.Member):

        global tictactoe_player1
        global tictactoe_player2
        global tictactoe_board
        global tictactoe_gameover
        global tictactoe_turn
        global tictactoe_count
        global tictactoe_wining_condition

        if tictactoe_gameover :
            tictactoe_player2=p2              #initializing player2
            tictactoe_player1=ctx.author      #initializing player1
            tictactoe_gameover=False
            tictactoe_count=0      
            tictactoe_board=[":white_large_square:", ":white_large_square:", ":white_large_square:",":white_large_square:", ":white_large_square:", ":white_large_square:",":white_large_square:", ":white_large_square:", ":white_large_square:"]
            #display rules of playing
            embed=discord.Embed(title="Tic-Tac-Toe",description="Scratch your brain. No luck.",colour=discord.Color.random(seed=None))
            embed.add_field(name="Rules to play :",value="The object of Tic Tac Toe is to get three in a row. The first player is known as X and the second is O. Players alternate placing X's and O's on the game board until either oppent has three in a row or all nine squares are filled.",inline=True)
            embed.add_field(name="How to Play :",value="Each box of the following tic-tak-toe board is represented by number from `1 to 9`. Player can mark box by using the command `~fill (grid_number)`.")      
            embed.set_thumbnail(url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQL00_5G8vrtl5R7xEmjiej1Sq3SCta25Pr8Q&usqp=CAU')
            await ctx.send(embed=embed)
            line=""                 #prints the board
            for i in range(0,9):    #prints the board
                if i==2 or i==5 or i==8:
                    line += " " + tictactoe_board[i]
                    await ctx.send(line)
                    line=""
                else:
                    line += " " + tictactoe_board[i]
            tictactoe_turn = tictactoe_player1           #giving first turn to starter of the game
            await ctx.send(f'First move will be played by {tictactoe_turn.mention}>')   
        else:               #if game is not finished the gameover will be false
            await ctx.send("A game is already in progress! Finish it before starting a new one.")         #game has began
 
    
    #filling up the boxes using ~fill
    @commands.command()
    async def fill(self, ctx, a:int):
        #calling all the global variable
        global tictactoe_turn
        global tictactoe_player1
        global tictactoe_player2
        global tictactoe_board
        global tictactoe_count
        global tictactoe_gameover
        if not(tictactoe_gameover):    #game continues
            mark=""
            if tictactoe_turn == ctx.author:      #checks whethaer the correct player is marking
                if tictactoe_turn == tictactoe_player1 :    #assigning cross to player1
                    mark = ":regional_indicator_x:"
                else:                   
                    mark=":o2:"         #assigning zero to player2
                if 0 <a < 10 and tictactoe_board[a-1] == ':white_large_square:':     #checks whether the input is correct
                    tictactoe_board[a-1]=mark
                    tictactoe_count += 1
                    line=""                 #prints the board
                    for i in range(len(tictactoe_board)):    #prints the board
                        if i==2 or i==5 or i==8:
                            line += " " + tictactoe_board[i]
                            await ctx.send(line)
                            line=""
                        else:
                            line += " " + tictactoe_board[i]
                    self.tictactoe_checkWinner(tictactoe_wining_condition,mark)      #updates value of gameover 
                    if tictactoe_gameover==True:                      #someone has won the game
                        await ctx.send(mark + "wins!")
                    elif tictactoe_count>=9:
                        tictactoe_gameover = True                          #the game is a tie
                        await ctx.send("Its a tie!")
                    if tictactoe_turn==tictactoe_player1:                       #switching the players move
                        tictactoe_turn=tictactoe_player2
                    else:
                        tictactoe_turn=tictactoe_player1
                else:
                    await ctx.send("Be sure to choose an integer between 1 and 9 (inclusive) and an unmarked tile.")
            else:                                           #wrong person was trying to play
                await ctx.send("Wait for your turn!")
        else:                                               #the game has ended
            await ctx.send("Please start a new game using the ~tictactoe command.")


    #checks wheather someone won or not
    def tictactoe_checkWinner(wining_condition,mark):
        global tictactoe_gameover
        for condition in tictactoe_wining_condition:
            if tictactoe_board[condition[0]] == mark and tictactoe_board[condition[1]] == mark and tictactoe_board[condition[2]] == mark:
                tictactoe_gameover = True
                break


    @commands.command()
    async def quit_tictactoe(self, ctx):
        global tictactoe_turn
        global tictactoe_player1
        global tictactoe_player2
        global tictactoe_board
        global tictactoe_count
        global tictactoe_gameover
        if tictactoe_gameover:
            await ctx.send("The game is not being played. To play enter the command `~tictactoe`")
        else:
            tictactoe_player1=""
            tictactoe_player2=""
            tictactoe_board=[]
            tictactoe_gameover=True
            tictactoe_turn=""
            tictactoe_count=0
            await ctx.send("The game has ended. To play again enter the commmand `~tictactoe`")

    #for error inputs
    @tictactoe.error
    async def tictactoe_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please mention 1 players for this command.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please make sure to mention/ping players (ie. <@688534433879556134>).")
    
    
    #for input errors
    @fill.error
    async def fill_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please enter a position you would like to mark.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please make sure to enter an integer.")



def setup(client):
    client.add_cog(Ticktactoe(client))
    