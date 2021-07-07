import discord
import random
from discord.ext import commands
from discord.ext.commands import Greedy

miniLudo_player1=""
miniLudo_player2=""
miniLudo_player3=""
miniLudo_player4=""
miniLudo_board=[":green_circle:",":green_square:",":white_large_square:",":white_large_square:",":white_large_square:",":yellow_square:",":yellow_circle:",":green_square:",":green_circle:",":white_large_square:",":yellow_square:",":radioactive:",":yellow_circle:",":yellow_square:",":white_large_square:",":radioactive:",":white_large_square:",":yellow_square:",":white_large_square:",":white_large_square:",":white_large_square:",":white_large_square:",":green_square:",":green_square:",":white_square_button:",":blue_square: ",":blue_square:",":white_large_square:",":white_large_square:",":white_large_square:",":white_large_square:",":red_square:",":white_large_square:",":radioactive:",":white_large_square:",":red_square:",":red_circle:",":radioactive:",":red_square:",":white_large_square:",":blue_circle:",":blue_square:",":red_circle:",":red_square:",":white_large_square:",":white_large_square:",":white_large_square:",":blue_square:",":blue_circle:"]
miniLudo_dice=0
miniLudo_path_green=[15,16,9,2,3,4,11,18,19,20,27,34,33,32,39,46,45,44,37,30,29,28,21,22,23,24]
miniLudo_path_yellow=[11,18,19,20,27,34,33,32,39,46,45,44,37,30,29,28,21,14,15,16,9,2,3,10,17,24]
miniLudo_path_blue=[33,32,39,46,45,44,37,30,29,28,21,14,15,16,9,2,3,4,11,18,19,20,27,26,25,24]
miniLudo_path_red=[37,30,29,28,21,14,15,16,9,2,3,4,11,18,19,20,27,34,33,32,39,46,45,38,31,24]
miniLudo_stars=[15,11,33,37]
miniLudo_green1=-1
miniLudo_green2=-1
miniLudo_yellow1=-1
miniLudo_yellow2=-1
miniLudo_blue1=-1
miniLudo_blue2=-1
miniLudo_red1=-1
miniLudo_red2=-1
miniLudo_turn=""
miniLudo_winner=[]
miniLudo_fakeplayers=0
miniLudo_roll_check = False
miniLudo_gameover=True

class Ludo(commands.Cog):

    def __init__(self,client):
        self.client = client
        

    @commands.Cog.listener()
    async def on_ready(self):
        print("Ludo cog is ready.")
    
    #code for miniludo game
    #starting the game, i.e, '~miniLudo'
    @commands.command(aliases=['Ludo', 'ludo', 'mini_ludo', 'Miniludo', 'miniludo'])
    async def miniLudo(self, ctx, players: Greedy[discord.Member] ):
        global miniLudo_player1
        global miniLudo_player2
        global miniLudo_player3
        global miniLudo_player4
        global miniLudo_board
        global miniLudo_path_green
        global miniLudo_path_yellow
        global miniLudo_path_blue
        global miniLudo_path_red
        global miniLudo_stars
        global miniLudo_green1
        global miniLudo_green2
        global miniLudo_yellow1
        global miniLudo_yellow2
        global miniLudo_blue1
        global miniLudo_blue2
        global miniLudo_red1
        global miniLudo_red2
        global miniLudo_turn
        global miniLudo_gameover
        global miniLudo_winner
        global miniLudo_roll_check
        global miniLudo_fakeplayers
        if 1<=len(players)<4:
            if miniLudo_gameover :
                miniLudo_green1=-1
                miniLudo_green2=-1
                miniLudo_yellow1=-1
                miniLudo_yellow2=-1
                miniLudo_blue1=-1
                miniLudo_blue2=-1
                miniLudo_red1=-1
                miniLudo_red2=-1
                miniLudo_turn=""
                miniLudo_roll_check = False
                miniLudo_gameover=False
                if len(players)==1:
                    miniLudo_player1=ctx.author
                    miniLudo_player2="fake1"
                    miniLudo_player3=players[0]
                    miniLudo_player4="fake2"
                    miniLudo_winner=[miniLudo_player2,miniLudo_player4]
                    miniLudo_fakeplayers=2
                elif len(players)==2:
                    miniLudo_player1=ctx.author
                    miniLudo_player2=players[0]
                    miniLudo_player3=players[1]
                    miniLudo_player4="fake1"
                    miniLudo_winner=[miniLudo_player4]
                    miniLudo_fakeplayers=1
                else:
                    miniLudo_winner=[]
                    miniLudo_player1=ctx.author
                    miniLudo_player2=players[0]
                    miniLudo_player3=players[1]
                    miniLudo_player4=players[2]
                    miniLudo_fakeplayers=0
                
                embed=discord.Embed(title="Mini-Ludo",description="Luck with scratching head.",colour=discord.Color.random(seed=None))
                embed.add_field(name="Rules to play :",value="Major rules are same as ludo but few changes. Each player has two ludo pieces. One will get an extra roll of dice onlyif he rolls 6. He won't be qiven second roll for making one of his piece reach its dectination nor for cutting other's piece. You can coincide both piece on a single spot but remember if some one came to the spot he both of your pieces has to start again.",inline=False)
                embed.add_field(name="How to Play :",value="Use command `~roll` alternatively to roll the dice and to move the desired piece use command `move (1 or 2 depending upon choice)`.")      
                embed.set_thumbnail(url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSCz6G7l37Q5Kx7fz0lUdFbSIY0qgPIi48VkQ&usqp=CAU')
                await ctx.send(embed=embed)
                line=""
                for i in range(49):
                    if i in [6,13,20,27,34,41,48]:
                        line += " "+miniLudo_board[i] + "\n"
                    else :
                        line += " "+miniLudo_board[i]
                await ctx.send(line)
                miniLudo_turn=miniLudo_player1
                if miniLudo_fakeplayers==0:
                    await ctx.send(f"{miniLudo_player1.mention} is :red_circle: (red)\n{miniLudo_player2.mention} is :blue_circle: (blue)\n{miniLudo_player3.mention} is :yellow_circle: (yellow)\n{miniLudo_player4.mention} is :green_circle: (green)") 
                elif miniLudo_fakeplayers==1:
                    await ctx.send(f"{miniLudo_player1.mention} is :red_circle: (red)\n{miniLudo_player2.mention} is :blue_circle: (blue)\n{miniLudo_player3.mention} is :yellow_circle: (yellow)")
                else:
                    await ctx.send(f"{miniLudo_player1.mention} is :red_circle: (red)\n{miniLudo_player3.mention} is :yellow_circle: (yellow)")  
                await ctx.send("Turns are respective to mentioned names above")   
            else:               #if game is not finished the gameover will be false
                await ctx.send("A game is already in progress! Finish it before starting a new one.")
        else:
            await ctx.send("Mention one to three players to play the game.")


    @commands.command()
    async def roll(self, ctx):
        global miniLudo_roll_check
        global miniLudo_gameover
        global miniLudo_dice
        global miniLudo_turn
        if not(miniLudo_gameover):
            if miniLudo_turn==ctx.author:
                if not(miniLudo_roll_check):
                    miniLudo_roll_check=True
                    miniLudo_dice=random.choice([1,2,3,4,5,6])
                    await ctx.send("You have rolled {}".format(miniLudo_dice))
                    if miniLudo_turn==miniLudo_player1:
                        if (miniLudo_red1==26 and miniLudo_red2+miniLudo_dice>26) or (miniLudo_red2==26 and miniLudo_red1+miniLudo_dice>26):
                            miniLudo_roll_check=False 
                            await ctx.send("This piece has already reached its destination and you cannot move the other piece so wait for the next roll")
                            t=self.miniLudo_next_player()
                            await ctx.send("Now its <@"+str(t.id)+"> turn to roll the dice")
                        elif miniLudo_red1==-1 and miniLudo_red2==-1 and miniLudo_dice!=6:
                            await ctx.send("None of your pieces are out. Try on next turn.")
                            miniLudo_roll_check=False
                            t=self.miniLudo_next_player()
                            await ctx.send("Now its <@"+str(t.id)+"> turn to roll the dice")
                    elif miniLudo_turn==miniLudo_player2:
                        if (miniLudo_blue1==26 and miniLudo_blue2+miniLudo_dice>26) or (miniLudo_blue2==26 and miniLudo_blue1+miniLudo_dice>26):
                            miniLudo_roll_check=False 
                            await ctx.send("This piece has already reached its destination and you cannot move the other piece so wait for the next roll")
                            t=self.miniLudo_next_player()
                            await ctx.send("Now its <@"+str(t.id)+"> turn to roll the dice")
                        elif miniLudo_blue1==-1 and miniLudo_blue2==-1 and miniLudo_dice!=6:
                            await ctx.send("None of your pieces are out. Try on next turn.")
                            miniLudo_roll_check=False
                            t=self.miniLudo_next_player()
                            await ctx.send("Now its <@"+str(t.id)+"> turn to roll the dice")
                    elif miniLudo_turn==miniLudo_player3:
                        if (miniLudo_yellow1==26 and miniLudo_yellow2+miniLudo_dice>26) or (miniLudo_yellow2==26 and miniLudo_yellow1+miniLudo_dice>26):
                            miniLudo_roll_check=False 
                            await ctx.send("This piece has already reached its destination and you cannot move the other piece so wait for the next roll")
                            t=self.miniLudo_next_player()
                            await ctx.send("Now its <@"+str(t.id)+"> turn to roll the dice")
                        elif miniLudo_yellow1==-1 and miniLudo_yellow2==-1 and miniLudo_dice!=6:
                            await ctx.send("None of your pieces are out. Try on next turn.")
                            miniLudo_roll_check=False
                            t=self.miniLudo_next_player()
                            await ctx.send("Now its <@"+str(t.id)+"> turn to roll the dice")
                    else:
                        if (miniLudo_green1==26 and miniLudo_green2+miniLudo_dice>26) or (miniLudo_green2==26 and miniLudo_green1+miniLudo_dice>26):
                            miniLudo_roll_check=False 
                            await ctx.send("This piece has already reached its destination and you cannot move the other piece so wait for the next roll")
                            t=self.miniLudo_next_player()
                            await ctx.send("Now its <@"+str(t.id)+"> turn to roll the dice")
                        elif miniLudo_green1==-1 and miniLudo_green2==-1 and miniLudo_dice!=6:
                            await ctx.send("None of your pieces are out. Try on next turn.")
                            miniLudo_roll_check=False
                            t=self.miniLudo_next_player()
                            await ctx.send("Now its <@"+str(t.id)+"> turn to roll the dice")
                else:
                   await ctx.send("You have rolled already")
            else: 
                await ctx.send("It is not your turn. Please wait patiently")
        else:                                               #the game has ended
            await ctx.send("Please start a game using the ~miniLudo command before using this command.")

    @commands.command()
    async def move(self, ctx, a:int):
        global miniLudo_player1
        global miniLudo_player2
        global miniLudo_player3
        global miniLudo_player4
        global miniLudo_board
        global miniLudo_path_green
        global miniLudo_path_yellow
        global miniLudo_path_blue
        global miniLudo_path_red
        global miniLudo_stars
        global miniLudo_green1
        global miniLudo_green2
        global miniLudo_yellow1
        global miniLudo_yellow2
        global miniLudo_blue1
        global miniLudo_blue2
        global miniLudo_red1
        global miniLudo_red2
        global miniLudo_turn
        global miniLudo_gameover
        global miniLudo_roll_check
        global miniLudo_dice
        global miniLudo_winner
        if not(miniLudo_gameover):
            if ctx.author==miniLudo_turn:
                if miniLudo_roll_check:
                    mover=0
                    if miniLudo_turn==miniLudo_player1:
                        mover=1
                    elif miniLudo_turn==miniLudo_player2:
                        mover=2
                    elif miniLudo_turn==miniLudo_player3:
                        mover=3
                    else :
                        mover=4
                    if a==1 :
                        if mover==1:
                            if miniLudo_red1==26 and miniLudo_red2+miniLudo_dice<27:
                                await ctx.send("This piece has already reached its destination, please move the otherone")
                            elif miniLudo_red1==-1 and miniLudo_dice!=6:
                                await ctx.send("This piece is not out. Please move the other piece.")
                            elif miniLudo_red1==-1 and miniLudo_dice==6:
                                await ctx.send("Piece_1 is out. Reroll to move it.")
                                miniLudo_roll_check=False
                                miniLudo_red1=0
                            elif miniLudo_red1+miniLudo_dice <=26:
                                miniLudo_roll_check=False
                                if miniLudo_red1==0:
                                    miniLudo_board[36]=":red_square:"
                                elif miniLudo_path_red[miniLudo_red1-1] in miniLudo_stars:
                                    miniLudo_board[miniLudo_path_red[miniLudo_red1-1]]=":radioactive:"
                                elif miniLudo_path_red[miniLudo_red1-1] in [31,38]:
                                    miniLudo_board[miniLudo_path_red[miniLudo_red1-1]]=":red_square:"
                                else:
                                    miniLudo_board[miniLudo_path_red[miniLudo_red1-1]]=":white_large_square:"
                                miniLudo_red1 += miniLudo_dice
                                if miniLudo_board[miniLudo_path_red[miniLudo_red1-1]]==":white_large_square:" or miniLudo_board[miniLudo_path_red[miniLudo_red1-1]]==":radioactive:" or (miniLudo_red1-1) in miniLudo_stars:
                                    miniLudo_board[miniLudo_path_red[miniLudo_red1-1]]=":red_circle:"
                                    await ctx.send("your move:")
                                else:
                                    if miniLudo_board[miniLudo_path_red[miniLudo_red1-1]]==":green_circle:":
                                        miniLudo_board[miniLudo_path_red[miniLudo_red1-1]]=":red_circle:"
                                        if miniLudo_green1==miniLudo_red1==miniLudo_green2:
                                            miniLudo_green1=-1
                                            miniLudo_green2=-1
                                            await ctx.send("You have sent back <@"+str(miniLudo_player4.id)+"> 's both piece 1 and piece 2 back home.")
                                        elif miniLudo_green1==miniLudo_red1:
                                            miniLudo_green1=-1
                                            await ctx.send("You have sent back <@"+str(miniLudo_player4.id)+"> 's piece 1  back home.")
                                        else:
                                            miniLudo_green2=-1
                                            await ctx.send("You have sent back <@"+str(miniLudo_player4.id)+"> 's piece 2 back home.")
                                    elif miniLudo_board[miniLudo_path_red[miniLudo_red1-1]]==":yellow_circle:":
                                        miniLudo_board[miniLudo_path_red[miniLudo_red1-1]]=":red_circle:"
                                        if miniLudo_yellow1==miniLudo_red1==miniLudo_yellow2:
                                            miniLudo_yellow1=-1
                                            miniLudo_yellow2=-1
                                            await ctx.send("You have sent back <@"+str(miniLudo_player3.id)+"> 's both piece 1 and piece 2 back home.")
                                        elif miniLudo_yellow1==miniLudo_red1:
                                            miniLudo_yellow1=-1
                                            await ctx.send("You have sent back <@"+str(miniLudo_player3.id)+"> 's piece 1  back home.")
                                        else:
                                            miniLudo_yellow2=-1
                                            await ctx.send("You have sent back <@"+str(miniLudo_player3.id)+"> 's piece 2 back home.")
                                    elif miniLudo_board[miniLudo_path_red[miniLudo_red1-1]]==":blue_circle:":
                                        miniLudo_board[miniLudo_path_red[miniLudo_red1-1]]=":red_circle:"
                                        if miniLudo_blue1==miniLudo_red1==miniLudo_blue2:
                                            miniLudo_blue1=-1
                                            miniLudo_blue2=-1
                                            await ctx.send("You have sent back <@"+str(miniLudo_player2.id)+"> 's both piece 1 and piece 2 back home.")
                                        elif miniLudo_blue1==miniLudo_red1:
                                            miniLudo_blue1=-1
                                            await ctx.send("You have sent back <@"+str(miniLudo_player2.id)+"> 's piece 1  back home.")
                                        else:
                                            miniLudo_blue2=-1
                                            await ctx.send("You have sent back <@"+str(miniLudo_player2.id)+"> 's piece 2 back home.")
                                await ctx.send(self.miniLudo_board_print(1))
                                if  miniLudo_red1 ==26 and miniLudo_red2 ==26:
                                    if len(miniLudo_winner)==2:
                                        await ctx.send("The match is over")
                                        miniLudo_winner.append(miniLudo_player1)
                                        miniLudo_gameover=True
                                        await ctx.send("Thus, the final leaderboard is:")
                                        await ctx.send(self.miniLudo_leaderboard())
                                    else :
                                        miniLudo_winner.append(miniLudo_player1)
                                        await ctx.send(":red_circle:(red) you are {}".format(len(miniLudo_winner)-miniLudo_fakeplayers))
                                        t=self.miniLudo_next_player()
                                        await ctx.send("Now its <@"+str(t.id)+"> turn to roll the dice")
                                else:
                                    if miniLudo_dice!=6:
                                        t=self.miniLudo_next_player()
                                        await ctx.send("Now its <@"+str(t.id)+"> turn to roll the dice")
                                    else:
                                        await ctx.send("You are lucky, next turn is also your.")
                            elif miniLudo_red1+miniLudo_dice >26 and miniLudo_red2+miniLudo_dice >26:
                                await ctx.send("None of your pieces can move, so try on next turn.")
                                miniLudo_roll_check=False
                                t=self.miniLudo_next_player()
                                await ctx.send("Now its <@"+str(t.id)+"> turn to roll the dice")
                            else:
                                await ctx.send("This piece cannot move therefore move the other piece.")
                        elif mover==2:
                            if miniLudo_blue1==26 and miniLudo_blue2+miniLudo_dice<27:
                                await ctx.send("This piece has already reached its destination, please move the otherone")
                            elif miniLudo_blue1==-1 and miniLudo_dice!=6:
                                await ctx.send("This piece is not out. Please move the other piece.")
                            elif miniLudo_blue1==-1 and miniLudo_dice==6:
                                await ctx.send("Piece_1 is out. Reroll to move it.")
                                miniLudo_roll_check=False
                                miniLudo_blue1=0
                            elif miniLudo_blue1+miniLudo_dice <=26:
                                miniLudo_roll_check=False
                                if miniLudo_blue1==0:
                                    miniLudo_board[40]=":blue_square:"
                                elif miniLudo_path_blue[miniLudo_blue1-1] in miniLudo_stars:
                                    miniLudo_board[miniLudo_path_blue[miniLudo_blue1-1]]=":radioactive:"
                                elif miniLudo_path_blue[miniLudo_red1-1] in [25,26]:
                                    miniLudo_board[miniLudo_path_blue[miniLudo_blue1-1]]=":blue_square:"
                                else:
                                    miniLudo_board[miniLudo_path_blue[miniLudo_blue1-1]]=":white_large_square:"
                                miniLudo_blue1 += miniLudo_dice
                                if miniLudo_board[miniLudo_path_blue[miniLudo_blue1-1]]==":white_large_square:" or miniLudo_board[miniLudo_path_blue[miniLudo_blue1-1]]==":radioactive:" or (miniLudo_red1-1) in miniLudo_stars:
                                    miniLudo_board[miniLudo_path_blue[miniLudo_blue1-1]]=":blue_circle:"
                                    await ctx.send("your move:")
                                else:
                                    if miniLudo_board[miniLudo_path_blue[miniLudo_blue1-1]]==":green_circle:":
                                        miniLudo_board[miniLudo_path_blue[miniLudo_blue1-1]]=":blue_circle:"
                                        if miniLudo_green1==miniLudo_blue1==miniLudo_green2:
                                            miniLudo_green1=-1
                                            miniLudo_green2=-1
                                            await ctx.send("You have sent back <@"+str(miniLudo_player4.id)+"> 's both piece 1 and piece 2 back home.")
                                        elif miniLudo_green1==miniLudo_blue1:
                                            miniLudo_green1=-1
                                            await ctx.send("You have sent back <@"+str(miniLudo_player4.id)+"> 's piece 1  back home.")
                                        else:
                                            miniLudo_green2=-1
                                            await ctx.send("You have sent back <@"+str(miniLudo_player4.id)+"> 's piece 2 back home.")
                                    elif miniLudo_board[miniLudo_path_blue[miniLudo_blue1-1]]==":yellow_circle:":
                                        miniLudo_board[miniLudo_path_blue[miniLudo_blue1-1]]=":blue_circle:"
                                        if miniLudo_yellow1==miniLudo_blue1==miniLudo_yellow2:
                                            miniLudo_yellow1=-1
                                            miniLudo_yellow2=-1
                                            await ctx.send("You have sent back <@"+str(miniLudo_player3.id)+"> 's both piece 1 and piece 2 back home.")
                                        elif miniLudo_yellow1==miniLudo_blue1:
                                            miniLudo_yellow1=-1
                                            await ctx.send("You have sent back <@"+str(miniLudo_player3.id)+"> 's piece 1  back home.")
                                        else:
                                            miniLudo_yellow2=-1
                                            await ctx.send("You have sent back <@"+str(miniLudo_player3.id)+"> 's piece 2 back home.")
                                    elif miniLudo_board[miniLudo_path_blue[miniLudo_blue1-1]]==":red_circle:":
                                        miniLudo_board[miniLudo_path_blue[miniLudo_blue1-1]]=":blue_circle:"
                                        if miniLudo_red1==miniLudo_blue1==miniLudo_red2:
                                            miniLudo_red1=-1
                                            miniLudo_red2=-1
                                            await ctx.send("You have sent back <@"+str(miniLudo_player1.id)+"> 's both piece 1 and piece 2 back home.")
                                        elif miniLudo_red1==miniLudo_blue1:
                                            miniLudo_red1=-1
                                            await ctx.send("You have sent back <@"+str(miniLudo_player1.id)+"> 's piece 1  back home.")
                                        else:
                                            miniLudo_red2=-1
                                            await ctx.send("You have sent back <@"+str(miniLudo_player1.id)+"> 's piece 2 back home.")
                                await ctx.send(self.miniLudo_board_print(2))
                                if  miniLudo_blue1 ==26 and miniLudo_blue2 ==26:
                                    if len(miniLudo_winner)==2:
                                        await ctx.send("The match is over")
                                        miniLudo_winner.append(miniLudo_player1)
                                        miniLudo_gameover=True
                                        await ctx.send("Thus, the final leaderboard is:")
                                        await ctx.send(self.miniLudo_leaderboard())
                                    else :
                                        miniLudo_winner.append(miniLudo_player1)
                                        await ctx.send(":blue_circle:(red) you are {}".format(len(miniLudo_winner)-miniLudo_fakeplayers))
                                        t=self.miniLudo_next_player()
                                        await ctx.send("Now its <@"+str(t.id)+"> turn to roll the dice")
                                else:
                                    if miniLudo_dice!=6:
                                        t=self.miniLudo_next_player()
                                        await ctx.send("Now its <@"+str(t.id)+"> turn to roll the dice")
                                    else:
                                        await ctx.send("You are lucky, next turn is also your.")
                            elif miniLudo_blue1+miniLudo_dice >26 and miniLudo_blue2+miniLudo_dice >26:
                                await ctx.send("None of your pieces can move, so try on next turn.")
                                miniLudo_roll_check=False
                                t=self.miniLudo_next_player()
                                await ctx.send("Now its <@"+str(t.id)+"> turn to roll the dice")
                            else:
                                await ctx.send("This piece cannot move therefore move the other piece.")
                        elif mover==3:
                            if miniLudo_yellow1==26 and miniLudo_yellow2+miniLudo_dice<27:
                                await ctx.send("This piece has already reached its destination, please move the otherone")                            
                            elif miniLudo_yellow1==-1 and miniLudo_dice!=6:
                                await ctx.send("This piece is not out. Please move the other piece.")
                            elif miniLudo_yellow1==-1 and miniLudo_dice==6:
                                await ctx.send("Piece_1 is out. Reroll to move it.")
                                miniLudo_roll_check=False
                                miniLudo_yellow1=0
                            elif miniLudo_yellow1+miniLudo_dice <=26:
                                miniLudo_roll_check=False
                                if miniLudo_yellow1==0:
                                    miniLudo_board[12]=":yellow_square:"
                                elif miniLudo_path_yellow[miniLudo_yellow1-1] in miniLudo_stars:
                                    miniLudo_board[miniLudo_path_yellow[miniLudo_yellow1-1]]=":radioactive:"
                                elif miniLudo_path_yellow[miniLudo_yellow1-1] in [10,17]:
                                    miniLudo_board[miniLudo_path_yellow[miniLudo_yellow1-1]]=":yellow_square:"
                                else:
                                    miniLudo_board[miniLudo_path_yellow[miniLudo_yellow1-1]]=":white_large_square:"
                                miniLudo_yellow1 += miniLudo_dice
                                if miniLudo_board[miniLudo_path_yellow[miniLudo_yellow1-1]]==":white_large_square:" or miniLudo_board[miniLudo_path_yellow[miniLudo_yellow1-1]]==":radioactive:" or (miniLudo_yellow1-1) in miniLudo_stars:
                                    miniLudo_board[miniLudo_path_yellow[miniLudo_yellow1-1]]=":red_circle:"
                                    await ctx.send("your move:")
                                else:
                                    if miniLudo_board[miniLudo_path_yellow[miniLudo_yellow1-1]]==":green_circle:":
                                        miniLudo_board[miniLudo_path_yellow[miniLudo_yellow1-1]]=":yellow_circle:"
                                        if miniLudo_green1==miniLudo_yellow1==miniLudo_green2:
                                            miniLudo_green1=-1
                                            miniLudo_green2=-1
                                            await ctx.send("You have sent back <@"+str(miniLudo_player4.id)+"> 's both piece 1 and piece 2 back home.")
                                        elif miniLudo_green1==miniLudo_yellow1:
                                            miniLudo_green1=-1
                                            await ctx.send("You have sent back <@"+str(miniLudo_player4.id)+"> 's piece 1  back home.")
                                        else:
                                            miniLudo_green2=-1
                                            await ctx.send("You have sent back <@"+str(miniLudo_player4.id)+"> 's piece 2 back home.")
                                    elif miniLudo_board[miniLudo_path_yellow[miniLudo_yellow1-1]]==":red_circle:":
                                        miniLudo_board[miniLudo_path_yellow[miniLudo_yellow1-1]]=":yellow_circle:"
                                        if miniLudo_red1==miniLudo_yellow1==miniLudo_red2:
                                            miniLudo_red1=-1
                                            miniLudo_red2=-1
                                            await ctx.send("You have sent back <@"+str(miniLudo_player1.id)+"> 's both piece 1 and piece 2 back home.")
                                        elif miniLudo_red1==miniLudo_yellow1:
                                            miniLudo_red1=-1
                                            await ctx.send("You have sent back <@"+str(miniLudo_player1.id)+"> 's piece 1  back home.")
                                        else:
                                            miniLudo_red2=-1
                                            await ctx.send("You have sent back <@"+str(miniLudo_player1.id)+"> 's piece 2 back home.")
                                    elif miniLudo_board[miniLudo_path_yellow[miniLudo_yellow1-1]]==":blue_circle:":
                                        miniLudo_board[miniLudo_path_yellow[miniLudo_yellow1-1]]=":yellow_circle:"
                                        if miniLudo_blue1==miniLudo_yellow1==miniLudo_blue2:
                                            miniLudo_blue1=-1
                                            miniLudo_blue2=-1
                                            await ctx.send("You have sent back <@"+str(miniLudo_player2.id)+"> 's both piece 1 and piece 2 back home.")
                                        elif miniLudo_blue1==miniLudo_yellow1:
                                            miniLudo_blue1=-1
                                            await ctx.send("You have sent back <@"+str(miniLudo_player2.id)+"> 's piece 1  back home.")
                                        else:
                                            miniLudo_blue2=-1
                                            await ctx.send("You have sent back <@"+str(miniLudo_player2.id)+"> 's piece 2 back home.")
                                await ctx.send(self.miniLudo_board_print(3))
                                if  miniLudo_yellow1 ==26 and miniLudo_yellow2 ==26:
                                    if len(miniLudo_winner)==2:
                                        await ctx.send("The match is over")
                                        miniLudo_winner.append(miniLudo_player1)
                                        miniLudo_gameover=True
                                        await ctx.send("Thus, the final leaderboard is:")
                                        await ctx.send(self.miniLudo_leaderboard())
                                    else :
                                        miniLudo_winner.append(miniLudo_player1)
                                        await ctx.send(":yellow_circle:(red) you are {}".format(len(miniLudo_winner)-miniLudo_fakeplayers))
                                        t=self.miniLudo_next_player()
                                        await ctx.send("Now its <@"+str(t.id)+"> turn to roll the dice")
                                else:
                                    if miniLudo_dice!=6:
                                        t=self.miniLudo_next_player()
                                        await ctx.send("Now its <@"+str(t.id)+"> turn to roll the dice")
                                    else:
                                        await ctx.send("You are lucky, next turn is also your.")
                            elif miniLudo_yellow1+miniLudo_dice >26 and miniLudo_yellow2+miniLudo_dice >26:
                                await ctx.send("None of your pieces can move, so try on next turn.")
                                miniLudo_roll_check=False
                                t=self.miniLudo_next_player()
                                await ctx.send("Now its <@"+str(t.id)+"> turn to roll the dice")
                            else:
                                await ctx.send("This piece cannot move therefore move the other piece.")
                        else :
                            if miniLudo_green1==26 and miniLudo_green2+miniLudo_dice<27:
                                await ctx.send("This piece has already reached its destination, please move the otherone")                            
                            elif miniLudo_green1==-1 and miniLudo_dice!=6:
                                await ctx.send("This piece is not out. Please move the other piece.")
                            elif miniLudo_green1==-1 and miniLudo_dice==6:
                                await ctx.send("Piece_1 is out. Reroll to move it.")
                                miniLudo_roll_check=False
                                miniLudo_green1=0
                            elif miniLudo_green1+miniLudo_dice <=26:
                                miniLudo_roll_check=False
                                if miniLudo_green1==0:
                                    miniLudo_board[15]=":green_square:"
                                elif miniLudo_path_green[miniLudo_green1-1] in miniLudo_stars:
                                    miniLudo_board[miniLudo_path_green[miniLudo_green1-1]]=":radioactive:"
                                elif miniLudo_path_green[miniLudo_green1-1] in [22,23]:
                                    miniLudo_board[miniLudo_path_green[miniLudo_green1-1]]=":green_square:"
                                else:
                                    miniLudo_board[miniLudo_path_green[miniLudo_green1-1]]=":white_large_square:"
                                miniLudo_green1 += miniLudo_dice
                                if miniLudo_board[miniLudo_path_green[miniLudo_green1-1]]==":white_large_square:" or miniLudo_board[miniLudo_path_green[miniLudo_green1-1]]==":radioactive:" or (miniLudo_green1-1) in miniLudo_stars:
                                    miniLudo_board[miniLudo_path_green[miniLudo_green1-1]]=":green_circle:"
                                    await ctx.send("your move:")
                                else:
                                    if miniLudo_board[miniLudo_path_green[miniLudo_green1-1]]==":red_circle:":
                                        miniLudo_board[miniLudo_path_green[miniLudo_green1-1]]=":green_circle:"
                                        if miniLudo_red1==miniLudo_green1==miniLudo_red2:
                                            miniLudo_red1=-1
                                            miniLudo_red2=-1
                                            await ctx.send("You have sent back <@"+str(miniLudo_player1.id)+"> 's both piece 1 and piece 2 back home.")
                                        elif miniLudo_red1==miniLudo_green1:
                                            miniLudo_red1=-1
                                            await ctx.send("You have sent back <@"+str(miniLudo_player1.id)+"> 's piece 1  back home.")
                                        else:
                                            miniLudo_red2=-1
                                            await ctx.send("You have sent back <@"+str(miniLudo_player1.id)+"> 's piece 2 back home.")
                                    elif miniLudo_board[miniLudo_path_green[miniLudo_green1-1]]==":yellow_circle:":
                                        miniLudo_board[miniLudo_path_green[miniLudo_green1-1]]=":green_circle:"
                                        if miniLudo_yellow1==miniLudo_green1==miniLudo_yellow2:
                                            miniLudo_yellow1=-1
                                            miniLudo_yellow2=-1
                                            await ctx.send("You have sent back <@"+str(miniLudo_player3.id)+"> 's both piece 1 and piece 2 back home.")
                                        elif miniLudo_yellow1==miniLudo_green1:
                                            miniLudo_yellow1=-1
                                            await ctx.send("You have sent back <@"+str(miniLudo_player3.id)+"> 's piece 1  back home.")
                                        else:
                                            miniLudo_yellow2=-1
                                            await ctx.send("You have sent back <@"+str(miniLudo_player3.id)+"> 's piece 2 back home.")
                                    elif miniLudo_board[miniLudo_path_green[miniLudo_green1-1]]==":blue_circle:":
                                        miniLudo_board[miniLudo_path_green[miniLudo_green1-1]]=":green_circle:"
                                        if miniLudo_blue1==miniLudo_green1==miniLudo_blue2:
                                            miniLudo_blue1=-1
                                            miniLudo_blue2=-1
                                            await ctx.send("You have sent back <@"+str(miniLudo_player2.id)+"> 's both piece 1 and piece 2 back home.")
                                        elif miniLudo_blue1==miniLudo_green1:
                                            miniLudo_blue1=-1
                                            await ctx.send("You have sent back <@"+str(miniLudo_player2.id)+"> 's piece 1  back home.")
                                        else:
                                            miniLudo_blue2=-1
                                            await ctx.send("You have sent back <@"+str(miniLudo_player2.id)+"> 's piece 2 back home.")
                                await ctx.send(self.miniLudo_board_print(4))
                                if  miniLudo_green1 ==26 and miniLudo_green2 ==26:
                                    if len(miniLudo_winner)==2:
                                        await ctx.send("The match is over")
                                        miniLudo_winner.append(miniLudo_player1)
                                        miniLudo_gameover=True
                                        await ctx.send("Thus, the final leaderboard is:")
                                        await ctx.send(self.miniLudo_leaderboard())
                                    else :
                                        miniLudo_winner.append(miniLudo_player1)
                                        await ctx.send(":green_circle:(red) you are {}".format(len(miniLudo_winner)-miniLudo_fakeplayers))
                                        t=self.miniLudo_next_player()
                                        await ctx.send("Now its <@"+str(t.id)+"> turn to roll the dice")
                                else:
                                    if miniLudo_dice!=6:
                                        t=self.miniLudo_next_player()
                                        await ctx.send("Now its <@"+str(t.id)+"> turn to roll the dice")
                                    else:
                                        await ctx.send("You are lucky, next turn is also your.")
                            elif miniLudo_green1+miniLudo_dice >26 and miniLudo_green2+miniLudo_dice >26:
                                await ctx.send("None of your pieces can move, so try on next turn.")
                                miniLudo_roll_check=False
                                t=self.miniLudo_next_player()
                                await ctx.send("Now its <@"+str(t.id)+"> turn to roll the dice")
                            else:
                                await ctx.send("This piece cannot move therefore move the other piece.")
                    elif a==2:
                        if mover==1:
                            if miniLudo_red2==26 and miniLudo_red1+miniLudo_dice<27:
                                await ctx.send("This piece has already reached its destination, please move the otherone")
                            elif miniLudo_red2==-1 and miniLudo_dice!=6:
                                await ctx.send("This piece is not out. Please move the other piece.")
                            elif miniLudo_red2==-1 and miniLudo_dice==6:
                                await ctx.send("Piece_1 is out. Reroll to move it.")
                                miniLudo_roll_check=False
                                miniLudo_red2=0
                            elif miniLudo_red2+miniLudo_dice <=26:
                                miniLudo_roll_check=False
                                if miniLudo_red2==0:
                                    miniLudo_board[42]=":red_square:"
                                elif miniLudo_path_red[miniLudo_red2-1] in miniLudo_stars:
                                    miniLudo_board[miniLudo_path_red[miniLudo_red2-1]]=":radioactive:"
                                elif miniLudo_path_red[miniLudo_red2-1] in [31,38]:
                                    miniLudo_board[miniLudo_path_red[miniLudo_red2-1]]=":red_square:"
                                else:
                                    miniLudo_board[miniLudo_path_red[miniLudo_red2-1]]=":white_large_square:"
                                miniLudo_red2 += miniLudo_dice
                                if miniLudo_board[miniLudo_path_red[miniLudo_red2-1]]==":white_large_square:" or miniLudo_board[miniLudo_path_red[miniLudo_red2-1]]==":radioactive:" or (miniLudo_red2-1) in miniLudo_stars:
                                    miniLudo_board[miniLudo_path_red[miniLudo_red2-1]]=":red_circle:"
                                    await ctx.send("your move:")
                                else:
                                    if miniLudo_board[miniLudo_path_red[miniLudo_red2-1]]==":green_circle:":
                                        miniLudo_board[miniLudo_path_red[miniLudo_red2-1]]=":red_circle:"
                                        if miniLudo_green1==miniLudo_red2==miniLudo_green2:
                                            miniLudo_green1=-1
                                            miniLudo_green2=-1
                                            await ctx.send("You have sent back <@"+str(miniLudo_player4.id)+"> 's both piece 1 and piece 2 back home.")
                                        elif miniLudo_green1==miniLudo_red2:
                                            miniLudo_green1=-1
                                            await ctx.send("You have sent back <@"+str(miniLudo_player4.id)+"> 's piece 1  back home.")
                                        else:
                                            miniLudo_green2=-1
                                            await ctx.send("You have sent back <@"+str(miniLudo_player4.id)+"> 's piece 2 back home.")
                                    elif miniLudo_board[miniLudo_path_red[miniLudo_red2-1]]==":yellow_circle:":
                                        miniLudo_board[miniLudo_path_red[miniLudo_red2-1]]=":red_circle:"
                                        if miniLudo_yellow1==miniLudo_red2==miniLudo_yellow2:
                                            miniLudo_yellow1=-1
                                            miniLudo_yellow2=-1
                                            await ctx.send("You have sent back <@"+str(miniLudo_player3.id)+"> 's both piece 1 and piece 2 back home.")
                                        elif miniLudo_yellow1==miniLudo_red2:
                                            miniLudo_yellow1=-1
                                            await ctx.send("You have sent back <@"+str(miniLudo_player3.id)+"> 's piece 1  back home.")
                                        else:
                                            miniLudo_yellow2=-1
                                            await ctx.send("You have sent back <@"+str(miniLudo_player3.id)+"> 's piece 2 back home.")
                                    elif miniLudo_board[miniLudo_path_red[miniLudo_red2-1]]==":blue_circle:":
                                        miniLudo_board[miniLudo_path_red[miniLudo_red2-1]]=":red_circle:"
                                        if miniLudo_blue1==miniLudo_red2==miniLudo_blue2:
                                            miniLudo_blue1=-1
                                            miniLudo_blue2=-1
                                            await ctx.send("You have sent back <@"+str(miniLudo_player2.id)+"> 's both piece 1 and piece 2 back home.")
                                        elif miniLudo_blue1==miniLudo_red2:
                                            miniLudo_blue1=-1
                                            await ctx.send("You have sent back <@"+str(miniLudo_player2.id)+"> 's piece 1  back home.")
                                        else:
                                            miniLudo_blue2=-1
                                            await ctx.send("You have sent back <@"+str(miniLudo_player2.id)+"> 's piece 2 back home.")
                                await ctx.send(self.miniLudo_board_print(1))
                                if  miniLudo_red1 ==26 and miniLudo_red2 ==26:
                                    if len(miniLudo_winner)==2:
                                        await ctx.send("The match is over")
                                        miniLudo_winner.append(miniLudo_player1)
                                        miniLudo_gameover=True
                                        await ctx.send("Thus, the final leaderboard is:")
                                        await ctx.send(self.miniLudo_leaderboard())
                                    else :
                                        miniLudo_winner.append(miniLudo_player1)
                                        await ctx.send(":red_circle:(red) you are {}".format(len(miniLudo_winner)-miniLudo_fakeplayers))
                                        t=self.miniLudo_next_player()
                                        await ctx.send("Now its <@"+str(t.id)+"> turn to roll the dice")
                                else:
                                    if miniLudo_dice!=6:
                                        t=self.miniLudo_next_player()
                                        await ctx.send("Now its <@"+str(t.id)+"> turn to roll the dice")
                                    else:
                                        await ctx.send("You are lucky, next turn is also your.")
                            elif miniLudo_red1+miniLudo_dice >26 and miniLudo_red2+miniLudo_dice >26:
                                await ctx.send("None of your pieces can move, so try on next turn.")
                                miniLudo_roll_check=False
                                t=self.miniLudo_next_player()
                                await ctx.send("Now its <@"+str(t.id)+"> turn to roll the dice")
                            else:
                                await ctx.send("This piece cannot move therefore move the other piece.")
                        elif mover==2:
                            if miniLudo_blue2==26 and miniLudo_blue1+miniLudo_dice<27:
                                await ctx.send("This piece has already reached its destination, please move the otherone")
                            elif miniLudo_blue2==-1 and miniLudo_dice!=6:
                                await ctx.send("This piece is not out. Please move the other piece.")
                            elif miniLudo_blue2==-1 and miniLudo_dice==6:
                                await ctx.send("Piece_1 is out. Reroll to move it.")
                                miniLudo_roll_check=False
                                miniLudo_blue2=0
                            elif miniLudo_blue2+miniLudo_dice <=26:
                                miniLudo_roll_check=False
                                if miniLudo_blue2==0:
                                    miniLudo_board[48]=":blue_square:"
                                elif miniLudo_path_blue[miniLudo_blue2-1] in miniLudo_stars:
                                    miniLudo_board[miniLudo_path_blue[miniLudo_blue2-1]]=":radioactive:"
                                elif miniLudo_path_blue[miniLudo_blue2-1] in [25,26]:
                                    miniLudo_board[miniLudo_path_blue[miniLudo_blue2-1]]=":blue_square:"
                                else:
                                    miniLudo_board[miniLudo_path_red[miniLudo_blue2-1]]=":white_large_square:"
                                miniLudo_blue2 += miniLudo_dice
                                if miniLudo_board[miniLudo_path_blue[miniLudo_blue2-1]]==":white_large_square:" or miniLudo_board[miniLudo_path_blue[miniLudo_blue2-1]]==":radioactive:" or (miniLudo_blue2-1) in miniLudo_stars:
                                    miniLudo_board[miniLudo_path_blue[miniLudo_blue2-1]]=":blue_circle:"
                                    await ctx.send("your move:")
                                else:
                                    if miniLudo_board[miniLudo_path_blue[miniLudo_blue2-1]]==":green_circle:":
                                        miniLudo_board[miniLudo_path_blue[miniLudo_blue2-1]]=":blue_circle:"
                                        if miniLudo_green1==miniLudo_blue2==miniLudo_green2:
                                            miniLudo_green1=-1
                                            miniLudo_green2=-1
                                            await ctx.send("You have sent back <@"+str(miniLudo_player4.id)+"> 's both piece 1 and piece 2 back home.")
                                        elif miniLudo_green1==miniLudo_blue2:
                                            miniLudo_green1=-1
                                            await ctx.send("You have sent back <@"+str(miniLudo_player4.id)+"> 's piece 1  back home.")
                                        else:
                                            miniLudo_green2=-1
                                            await ctx.send("You have sent back <@"+str(miniLudo_player4.id)+"> 's piece 2 back home.")
                                    elif miniLudo_board[miniLudo_path_blue[miniLudo_blue2-1]]==":yellow_circle:":
                                        miniLudo_board[miniLudo_path_blue[miniLudo_blue2-1]]=":blue_circle:"
                                        if miniLudo_yellow1==miniLudo_blue2==miniLudo_yellow2:
                                            miniLudo_yellow1=-1
                                            miniLudo_yellow2=-1
                                            await ctx.send("You have sent back <@"+str(miniLudo_player3.id)+"> 's both piece 1 and piece 2 back home.")
                                        elif miniLudo_yellow1==miniLudo_blue2:
                                            miniLudo_yellow1=-1
                                            await ctx.send("You have sent back <@"+str(miniLudo_player3.id)+"> 's piece 1  back home.")
                                        else:
                                            miniLudo_yellow2=-1
                                            await ctx.send("You have sent back <@"+str(miniLudo_player3.id)+"> 's piece 2 back home.")
                                    elif miniLudo_board[miniLudo_path_blue[miniLudo_blue2-1]]==":red_circle:":
                                        miniLudo_board[miniLudo_path_blue[miniLudo_blue2-1]]=":blue_circle:"
                                        if miniLudo_red1==miniLudo_blue2==miniLudo_red2:
                                            miniLudo_red1=-1
                                            miniLudo_red2=-1
                                            await ctx.send("You have sent back <@"+str(miniLudo_player1.id)+"> 's both piece 1 and piece 2 back home.")
                                        elif miniLudo_red1==miniLudo_blue2:
                                            miniLudo_red1=-1
                                            await ctx.send("You have sent back <@"+str(miniLudo_player1.id)+"> 's piece 1  back home.")
                                        else:
                                            miniLudo_red2=-1
                                            await ctx.send("You have sent back <@"+str(miniLudo_player1.id)+"> 's piece 2 back home.")
                                await ctx.send(self.miniLudo_board_print(2))
                                if  miniLudo_blue1 ==26 and miniLudo_blue2 ==26:
                                    if len(miniLudo_winner)==2:
                                        await ctx.send("The match is over")
                                        miniLudo_winner.append(miniLudo_player1)
                                        miniLudo_gameover=True
                                        await ctx.send("Thus, the final leaderboard is:")
                                        await ctx.send(self.miniLudo_leaderboard())
                                    else :
                                        miniLudo_winner.append(miniLudo_player1)
                                        await ctx.send(":blue_circle:(red) you are {}".format(len(miniLudo_winner)-miniLudo_fakeplayers))
                                        t=self.miniLudo_next_player()
                                        await ctx.send("Now its <@"+str(t.id)+"> turn to roll the dice")
                                else:
                                    if miniLudo_dice!=6:
                                        t=self.miniLudo_next_player()
                                        await ctx.send("Now its <@"+str(t.id)+"> turn to roll the dice")
                                    else:
                                        await ctx.send("You are lucky, next turn is also your.")
                            elif miniLudo_blue1+miniLudo_dice >26 and miniLudo_blue2+miniLudo_dice >26:
                                await ctx.send("None of your pieces can move, so try on next turn.")
                                miniLudo_roll_check=False
                                t=self.miniLudo_next_player()
                                await ctx.send("Now its <@"+str(t.id)+"> turn to roll the dice")
                            else:
                                await ctx.send("This piece cannot move therefore move the other piece.")
                        elif mover==3:
                            if miniLudo_yellow2==26 and miniLudo_yellow1+miniLudo_dice<27:
                                await ctx.send("This piece has already reached its destination, please move the otherone")
                            elif miniLudo_yellow2==-1 and miniLudo_dice!=6:
                                await ctx.send("This piece is not out. Please move the other piece.")
                            elif miniLudo_yellow2==-1 and miniLudo_dice==6:
                                await ctx.send("Piece_1 is out. Reroll to move it.")
                                miniLudo_roll_check=False
                                miniLudo_yellow2=0
                            elif miniLudo_yellow2+miniLudo_dice <=26:
                                miniLudo_roll_check=False
                                if miniLudo_yellow2==0:
                                    miniLudo_board[6]=":yellow_square:"
                                elif miniLudo_path_yellow[miniLudo_yellow2-1] in miniLudo_stars:
                                    miniLudo_board[miniLudo_path_yellow[miniLudo_yellow2-1]]=":radioactive:"
                                elif miniLudo_path_yellow[miniLudo_yellow2-1] in [17,10]:
                                    miniLudo_board[miniLudo_path_yellow[miniLudo_yellow2-1]]=":yellow_square:"
                                else:
                                    miniLudo_board[miniLudo_path_yellow[miniLudo_yellow2-1]]=":white_large_square:"
                                miniLudo_yellow2 += miniLudo_dice
                                if miniLudo_board[miniLudo_path_yellow[miniLudo_yellow2-1]]==":white_large_square:" or miniLudo_board[miniLudo_path_yellow[miniLudo_yellow2-1]]==":radioactive:" or (miniLudo_yellow2-1) in miniLudo_stars:
                                    miniLudo_board[miniLudo_path_yellow[miniLudo_yellow2-1]]=":yellow_circle:"
                                    await ctx.send("your move:")
                                else:
                                    if miniLudo_board[miniLudo_path_yellow[miniLudo_yellow2-1]]==":green_circle:":
                                        miniLudo_board[miniLudo_path_yellow[miniLudo_yellow2-1]]=":yellow_circle:"
                                        if miniLudo_green1==miniLudo_yellow2==miniLudo_green2:
                                            miniLudo_green1=-1
                                            miniLudo_green2=-1
                                            await ctx.send("You have sent back <@"+str(miniLudo_player4.id)+"> 's both piece 1 and piece 2 back home.")
                                        elif miniLudo_green1==miniLudo_yellow2:
                                            miniLudo_green1=-1
                                            await ctx.send("You have sent back <@"+str(miniLudo_player4.id)+"> 's piece 1  back home.")
                                        else:
                                            miniLudo_green2=-1
                                            await ctx.send("You have sent back <@"+str(miniLudo_player4.id)+"> 's piece 2 back home.")
                                    elif miniLudo_board[miniLudo_path_yellow[miniLudo_yellow2-1]]==":red_circle:":
                                        miniLudo_board[miniLudo_path_yellow[miniLudo_yellow2-1]]=":yellow_circle:"
                                        if miniLudo_red1==miniLudo_yellow1==miniLudo_red2:
                                            miniLudo_red1=-1
                                            miniLudo_red2=-1
                                            await ctx.send("You have sent back <@"+str(miniLudo_player1.id)+"> 's both piece 1 and piece 2 back home.")
                                        elif miniLudo_red1==miniLudo_yellow2:
                                            miniLudo_red1=-1
                                            await ctx.send("You have sent back <@"+str(miniLudo_player1.id)+"> 's piece 1  back home.")
                                        else:
                                            miniLudo_red2=-1
                                            await ctx.send("You have sent back <@"+str(miniLudo_player1.id)+"> 's piece 2 back home.")
                                    elif miniLudo_board[miniLudo_path_yellow[miniLudo_yellow2-1]]==":blue_circle:":
                                        miniLudo_board[miniLudo_path_yellow[miniLudo_yellow2-1]]=":yellow_circle:"
                                        if miniLudo_blue1==miniLudo_yellow2==miniLudo_blue2:
                                            miniLudo_blue1=-1
                                            miniLudo_blue2=-1
                                            await ctx.send("You have sent back <@"+str(miniLudo_player2.id)+"> 's both piece 1 and piece 2 back home.")
                                        elif miniLudo_blue1==miniLudo_yellow2:
                                            miniLudo_blue1=-1
                                            await ctx.send("You have sent back <@"+str(miniLudo_player2.id)+"> 's piece 1  back home.")
                                        else:
                                            miniLudo_blue2=-1
                                            await ctx.send("You have sent back <@"+str(miniLudo_player2.id)+"> 's piece 2 back home.")
                                await ctx.send(self.miniLudo_board_print(3))
                                if  miniLudo_yellow1 ==26 and miniLudo_yellow2 ==26:
                                    if len(miniLudo_winner)==2:
                                        await ctx.send("The match is over")
                                        miniLudo_winner.append(miniLudo_player1)
                                        miniLudo_gameover=True
                                        await ctx.send("Thus, the final leaderboard is:")
                                        await ctx.send(self.miniLudo_leaderboard())
                                    else :
                                        miniLudo_winner.append(miniLudo_player1)
                                        await ctx.send(":yellow_circle:(red) you are {}".format(len(miniLudo_winner)-miniLudo_fakeplayers))
                                        t=self.miniLudo_next_player()
                                        await ctx.send("Now its <@"+str(t.id)+"> turn to roll the dice")
                                else:
                                    if miniLudo_dice!=6:
                                        t=self.miniLudo_next_player()
                                        await ctx.send("Now its <@"+str(t.id)+"> turn to roll the dice")
                                    else:
                                        await ctx.send("You are lucky, next turn is also your.")
                            elif miniLudo_yellow1+miniLudo_dice >26 and miniLudo_yellow2+miniLudo_dice >26:
                                await ctx.send("None of your pieces can move, so try on next turn.")
                                miniLudo_roll_check=False
                                t=self.miniLudo_next_player()
                                await ctx.send("Now its <@"+str(t.id)+"> turn to roll the dice")
                            else:
                                await ctx.send("This piece cannot move therefore move the other piece.")
                        else :
                            if miniLudo_green2==26 and miniLudo_green1+miniLudo_dice<27:
                                await ctx.send("This piece has already reached its destination, please move the otherone")
                            elif miniLudo_green2==-1 and miniLudo_dice!=6:
                                await ctx.send("This piece is not out. Please move the other piece.")
                            elif miniLudo_green2==-1 and miniLudo_dice==6:
                                await ctx.send("Piece_1 is out. Reroll to move it.")
                                miniLudo_roll_check=False
                                miniLudo_green2=0
                            elif miniLudo_green2+miniLudo_dice <=26:
                                miniLudo_roll_check=False
                                if miniLudo_green2==0:
                                    miniLudo_board[0]=":green_square:"
                                elif miniLudo_path_green[miniLudo_green2-1] in miniLudo_stars:
                                    miniLudo_board[miniLudo_path_green[miniLudo_green2-1]]=":radioactive:"
                                elif miniLudo_path_green[miniLudo_green2-1] in [22,23]:
                                    miniLudo_board[miniLudo_path_green[miniLudo_green2-1]]=":green_square:"
                                else:
                                    miniLudo_board[miniLudo_path_green[miniLudo_green2-1]]=":white_large_square:"
                                miniLudo_green2 += miniLudo_dice
                                if miniLudo_board[miniLudo_path_green[miniLudo_green2-1]]==":white_large_square:" or miniLudo_board[miniLudo_path_green[miniLudo_green2-1]]==":radioactive:" or (miniLudo_green2-1) in miniLudo_stars:
                                    miniLudo_board[miniLudo_path_green[miniLudo_green2-1]]=":green_circle:"
                                    await ctx.send("your move:")
                                else:
                                    if miniLudo_board[miniLudo_path_green[miniLudo_green2-1]]==":red_circle:":
                                        miniLudo_board[miniLudo_path_green[miniLudo_green2-1]]=":green_circle:"
                                        if miniLudo_red1==miniLudo_green2==miniLudo_red2:
                                            miniLudo_red1=-1
                                            miniLudo_red2=-1
                                            await ctx.send("You have sent back <@"+str(miniLudo_player1.id)+"> 's both piece 1 and piece 2 back home.")
                                        elif miniLudo_red1==miniLudo_green2:
                                            miniLudo_red1=-1
                                            await ctx.send("You have sent back <@"+str(miniLudo_player1.id)+"> 's piece 1  back home.")
                                        else:
                                            miniLudo_red2=-1
                                            await ctx.send("You have sent back <@"+str(miniLudo_player1.id)+"> 's piece 2 back home.")
                                    elif miniLudo_board[miniLudo_path_green[miniLudo_green2-1]]==":yellow_circle:":
                                        miniLudo_board[miniLudo_path_green[miniLudo_green2-1]]=":green_circle:"
                                        if miniLudo_yellow1==miniLudo_green2==miniLudo_yellow2:
                                            miniLudo_yellow1=-1
                                            miniLudo_yellow2=-1
                                            await ctx.send("You have sent back <@"+str(miniLudo_player3.id)+"> 's both piece 1 and piece 2 back home.")
                                        elif miniLudo_yellow1==miniLudo_green2:
                                            miniLudo_yellow1=-1
                                            await ctx.send("You have sent back <@"+str(miniLudo_player3.id)+"> 's piece 1  back home.")
                                        else:
                                            miniLudo_yellow2=-1
                                            await ctx.send("You have sent back <@"+str(miniLudo_player3.id)+"> 's piece 2 back home.")
                                    elif miniLudo_board[miniLudo_path_green[miniLudo_green2-1]]==":blue_circle:":
                                        miniLudo_board[miniLudo_path_green[miniLudo_green2-1]]=":green_circle:"
                                        if miniLudo_blue1==miniLudo_green2==miniLudo_blue2:
                                            miniLudo_blue1=-1
                                            miniLudo_blue2=-1
                                            await ctx.send("You have sent back <@"+str(miniLudo_player2.id)+"> 's both piece 1 and piece 2 back home.")
                                        elif miniLudo_blue1==miniLudo_green2:
                                            miniLudo_blue1=-1
                                            await ctx.send("You have sent back <@"+str(miniLudo_player2.id)+"> 's piece 1  back home.")
                                        else:
                                            miniLudo_blue2=-1
                                            await ctx.send("You have sent back <@"+str(miniLudo_player2.id)+"> 's piece 2 back home.")
                                await ctx.send(self.miniLudo_board_print(4))
                                if  miniLudo_green1 ==26 and miniLudo_green2 ==26:
                                    if len(miniLudo_winner)==2:
                                        await ctx.send("The match is over")
                                        miniLudo_winner.append(miniLudo_player1)
                                        miniLudo_gameover=True
                                        await ctx.send("Thus, the final leaderboard is:")
                                        await ctx.send(self.miniLudo_leaderboard())
                                    else :
                                        miniLudo_winner.append(miniLudo_player1)
                                        await ctx.send(":yellow_circle:(red) you are {}".format(len(miniLudo_winner)-miniLudo_fakeplayers))
                                        t=self.miniLudo_next_player()
                                        await ctx.send("Now its <@"+str(t.id)+"> turn to roll the dice")
                                else:
                                    if miniLudo_dice!=6:
                                        t=self.miniLudo_next_player()
                                        await ctx.send("Now its <@"+str(t.id)+"> turn to roll the dice")
                                    else:
                                        await ctx.send("You are lucky, next turn is also your.")
                            elif miniLudo_green1+miniLudo_dice >26 and miniLudo_green2+miniLudo_dice >26:
                                await ctx.send("None of your pieces can move, so try on next turn.")
                                miniLudo_roll_check=False
                                t=self.miniLudo_next_player()
                                await ctx.send("Now its <@"+str(t.id)+"> turn to roll the dice")
                            else:
                                await ctx.send("This piece cannot move therefore move the other piece.")
                    else:
                        await ctx.send("Input either 1 or 2 to select the piece you want to move.")
                else:
                    await ctx.send("Roll before moving the piece.")
            else:
                await ctx.send("Wait for your turn or I will curse you.")
        else:
            await ctx.send("Please start a new game using the ~miniLudo command.")


    @commands.command(aliases=['quit_Ludo','quit_ludo','quitludo','quitLudo','quitMiniLudo','quitminiLudo','quitminiludo'])
    async def quit_miniLudo(self, ctx):
        global miniLudo_player1
        global miniLudo_player2
        global miniLudo_player3
        global miniLudo_player4
        global miniLudo_board
        global miniLudo_path_green
        global miniLudo_path_yellow
        global miniLudo_path_blue
        global miniLudo_path_red
        global miniLudo_stars
        global miniLudo_green1
        global miniLudo_green2
        global miniLudo_yellow1
        global miniLudo_yellow2
        global miniLudo_blue1
        global miniLudo_blue2
        global miniLudo_red1
        global miniLudo_red2
        global miniLudo_turn
        global miniLudo_gameover
        global miniLudo_roll_check
        global miniLudo_dice
        global miniLudo_winner
        if miniLudo_gameover:
            await ctx.send("The game is not being played. To play enter the command `~miniLudo`")
        else:
            miniLudo_player1=""
            miniLudo_player2=""
            miniLudo_player3=""
            miniLudo_player4=""
            miniLudo_board=[":green_circle:",":green_square:",":white_large_square:",":white_large_square:",":white_large_square:",":yellow_square:",":yellow_circle:",":green_square:",":green_circle:",":white_large_square:",":yellow_square:",":radioactive:",":yellow_circle:",":yellow_square:",":white_large_square:",":radioactive:",":white_large_square:",":yellow_square:",":white_large_square:",":white_large_square:",":white_large_square:",":white_large_square:",":green_square:",":green_square:",":white_square_button:",":blue_square: ",":blue_square:",":white_large_square:",":white_large_square:",":white_large_square:",":white_large_square:",":red_square:",":white_large_square:",":radioactive:",":white_large_square:",":red_square:",":red_circle:",":radioactive:",":red_square:",":white_large_square:",":blue_circle:",":blue_square:",":red_circle:",":red_square:",":white_large_square:",":white_large_square:",":white_large_square:",":blue_square:",":blue_circle:"]
            miniLudo_dice=0
            miniLudo_path_green=[15,16,9,2,3,4,11,18,19,20,27,34,33,32,39,46,45,44,37,30,29,28,21,22,23,24]
            miniLudo_path_yellow=[11,18,19,20,27,34,33,32,39,46,45,44,37,30,29,28,21,14,15,16,9,2,3,10,17,24]
            miniLudo_path_blue=[33,32,39,46,45,44,37,30,29,28,21,14,15,16,9,2,3,4,11,18,19,20,27,26,25,24]
            miniLudo_path_red=[37,30,29,28,21,14,15,16,9,2,3,4,11,18,19,20,27,34,33,32,39,46,45,38,31,24]
            miniLudo_stars=[15,11,33,37]
            miniLudo_green1=-1
            miniLudo_green2=-1
            miniLudo_yellow1=-1
            miniLudo_yellow2=-1
            miniLudo_blue1=-1
            miniLudo_blue2=-1
            miniLudo_red1=-1
            miniLudo_red2=-1
            miniLudo_turn=""
            miniLudo_winner=[]
            miniLudo_roll_check = False
            miniLudo_gameover=True
            await ctx.send("The game has ended. To play again enter the commmand `~miniLudo`")

    @miniLudo.error
    async def miniLudo_error(self, ctx, error):
        print(error)
        if isinstance(error, commands.BadArgument):
            await ctx.send("Please make sure to mention/ping players (ie. <@688534433879556134>).")

    @move.error
    async def move_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please enter only 1 or 2 to control your pieces.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please make sure to enter an integer.")


    def miniLudo_board_print(self, a):
        global miniLudo_board
        line=""
        if a==1:
            for i in range(7):
                for j in range(7):
                    line += miniLudo_board[i*7 +j]
                line+="\n"
        elif a ==2:
            for i in range(42,49):
                for j in range(7):
                    line += miniLudo_board[i-j*7]
                line+="\n"
        elif a==3:
            for i in range(48,5,-7):
                for j in range(7):
                    line += miniLudo_board[i -j]
                line+="\n"
        else:
            for i in range(6,-1,-1):
                for j in range(7):
                    line += miniLudo_board[i+j*7]
                line+="\n"
        return line
    def miniLudo_next_player(self):
        global miniLudo_winner
        global miniLudo_turn
        global miniLudo_player1
        global miniLudo_player2
        global miniLudo_player3
        global miniLudo_player4
        if miniLudo_turn==miniLudo_player1:
            if not(miniLudo_player2 in miniLudo_winner):
                miniLudo_turn=miniLudo_player2
                return miniLudo_player2
            elif not(miniLudo_player3 in miniLudo_winner):
                miniLudo_turn=miniLudo_player3
                return miniLudo_player3
            else:
                miniLudo_turn=miniLudo_player4
                return miniLudo_player4
        elif miniLudo_turn==miniLudo_player2:
            if not(miniLudo_player3 in miniLudo_winner):
                miniLudo_turn=miniLudo_player3
                return miniLudo_player3
            elif not(miniLudo_player4 in miniLudo_winner):
                miniLudo_turn=miniLudo_player4
                return miniLudo_player4
            else:
                miniLudo_turn=miniLudo_player1
                return miniLudo_player1
        elif miniLudo_turn==miniLudo_player3:
            if not(miniLudo_player4 in miniLudo_winner):
                miniLudo_turn=miniLudo_player4
                return miniLudo_player4
            elif not(miniLudo_player1 in miniLudo_winner):
                miniLudo_turn=miniLudo_player1
                return miniLudo_player1
            else:
                miniLudo_turn=miniLudo_player2
                return miniLudo_player2
        else:
            if not(miniLudo_player1 in miniLudo_winner):
                miniLudo_turn=miniLudo_player1
                return miniLudo_player1
            elif not(miniLudo_player2 in miniLudo_winner):
                miniLudo_turn=miniLudo_player2
                return miniLudo_player2
            else:
                miniLudo_turn=miniLudo_player3
                return miniLudo_player3

    def miniLudo_leaderboard(self):
        global miniLudo_fakeplayers
        global miniLudo_winner
        line=""
        if miniLudo_fakeplayers==0:
            for i in range(1,5):
                line+="<@" + str(miniLudo_winner[i-1])+ "> is {}\n".format(i)
        elif miniLudo_fakeplayers==1:
            for i in range(1,4):
                line+="<@" + str(miniLudo_winner[i])+ "> is {}\n".format(i)
        else:
            for i in range(1,3):
                line+="<@" + str(miniLudo_winner[i+1])+ "> is {}\n".format(i)
        return line


def setup(client):
    client.add_cog(Ludo(client))

