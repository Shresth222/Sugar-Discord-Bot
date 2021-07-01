#importing all the needed libraries
import discord
import random
from discord.ext import commands



#token for the bot
TOKEN = 'ODU5OTQwMTMwODQzNjU2MjUy.YNz_qA.dL7YLiey26eQJj6L-fsVEPprs1s'
#creating bot object
client = commands.Bot(command_prefix='~')



#global variable for tictaktoe
player1=""
player2=""
board=[]
gameover=True
turn=""
count=0
wining_condition=[[0,1,2],[3,4,5],[6,7,8],[0,4,8],[2,4,6],[0,3,6],[1,4,7],[2,5,8]]




#initializing the bot
@client.event
async def on_ready():
  print("Hello I am {0.user}".format(client))




#Opening syntax,i.e., ~hello 
@client.command()
async def hello(ctx):
    await ctx.send("Hello " + str(ctx.author).split('#')[0] + ". I am the first bot made by Shresth. Please be kind.\n For more info send '~help'.")
    print(ctx.guild)







#code for tic-tak-toe game
#starting the game, i.e., ~tictaktoe  
@client.command()
async def tictactoe(ctx, p2:discord.Member):
    #calling all the global variable
    global turn
    global board
    global gameover
    global player1
    global player2
    if gameover :
        player2=p2              #initializing player2
        player1=ctx.author      #initializing player1
        gameover=False      
        board=[":white_large_square:", ":white_large_square:", ":white_large_square:",":white_large_square:", ":white_large_square:", ":white_large_square:",":white_large_square:", ":white_large_square:", ":white_large_square:"]
        await ctx.send("How to play :\n Each box of the following tic-tak-toe board is represented by number from 1 to 9.\n You can mark Your box using ~fill 'box you want to fill' command")      #display rules of playing
        line=""                 #prints the board
        for i in range(0,9):    #prints the board
            if i==2 or i==5 or i==8:
                line += " " + board[i]
                await ctx.send(line)
                line=""
            else:
                line += " " + board[i]
        turn = player1           #giving first turn to starter of the game
        await ctx.send("First move will be played by <@" + str(player1.id) + ">")   #if game is not finished the gameover will be false
    else:
        await ctx.send("A game is already in progress! Finish it before starting a new one.")         #game has began
           

#filling up the boxes using ~fill
@client.command()
async def fill(ctx, a:int):
    #calling all the global variable
    global turn
    global player1
    global player2
    global board
    global count
    global gameover
    if ~gameover:    #game continues
        mark=""
        if turn == ctx.author:      #checks whethaer the correct player is marking
            if turn == player1 :    #assigning cross to player1
                mark = ":regional_indicator_x:"
            else:                   
                mark=":o2:"         #assigning zero to player2
            if 0 <a < 10 and board[a-1] == ':white_large_square:':     #checks whether the input is correct
                board[a-1]=mark
                count += 1
                line=""                 #prints the board
                for i in range(len(board)):    #prints the board
                    if i==2 or i==5 or i==8:
                        print("ya bhi run kia")
                        line += " " + board[i]
                        await ctx.send(line)
                        line=""
                    else:
                        line += " " + board[i]
                checkWinner(wining_condition,mark)      #updates value of gameover 
                if gameover==True:                      #someone has won the game
                    await ctx.send(mark + "wins!")
                elif count>=9:
                    gameover = True                          #the game is a tie
                    await ctx.send("Its a tie!")
                if turn==player1:                       #switching the players move
                    turn=player2
                else:
                    turn=player1
            else:
                await ctx.send("Be sure to choose an integer between 1 and 9 (inclusive) and an unmarked tile.")
        else:                                           #wrong person was trying to play
            await ctx.send("Wait for your turn!")
    else:                                               #the game has ended
        await ctx.send("Please start a new game using the ~tictactoe command.")


#checks wheather someone won or not
def checkWinner(wining_condition,mark):
    global gameover
    for condition in wining_condition:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameover = True
            break



#for error inputs
@tictactoe.error
async def tictactoe_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention 1 players for this command.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to mention/ping players (ie. <@688534433879556134>).")


#for input errors
@fill.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please enter a position you would like to mark.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to enter an integer.")
    









client.run(TOKEN)
