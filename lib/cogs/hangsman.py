import discord
from discord import embeds
from discord import colour
from discord.ext import commands
import random


wordGuesser_list = ["future","python","homie","pikachu","puppy","mathmatics","chemistry","groovy","gunna","tunmun","gubbara","laptop","pen","milk","butter","burgure","pizza","doracake","choclate","chicken","sunday","mouse","chair","doremon","shinchan","hagemaru","chotabheem","pokemon", "naruto","hinatahyuga","kakashi","dluffy","saitama","sakura","poppo","goku","shikamaru","itachi","ichigo","levi"]
wordGuesser_word = ''
wordGuesser_guessedLettters = ['a','e','i','o','u']
wordGuesser_gameover = True
wordGuesser_chances=0
wordGuesser_answer=''


class GuessTheWord(commands.Cog):

    def __init__(self,bot):
        self.bot = bot
        

    @commands.Cog.listener()
    async def on_ready(self):
        print("GuessTheWord cog is ready.")



    @commands.command(aliases=['wg','word_guesser'])
    async def wordGuesser(self, ctx):
        global wordGuesser_gameover
        global wordGuesser_chances
        global wordGuesser_guessedLettters
        global wordGuesser_answer

        if wordGuesser_gameover:
            wordGuesser_gameover = False
            self.give_word()
            self.chances()
            wordGuesser_answer = ''
            wordGuesser_guessedLettters = ['a','e','i','o','u']
            embed=discord.Embed(title="Guess The Word",description="Luck with scratching head.",colour=discord.Color.random(seed=None))
            embed.add_field(name="Rules to play :",value="Rules are same as hangsman. Guess the word within specific chances. All the vowels are already marked. You have to guess all the consonant present in the word",inline=False)
            embed.add_field(name="How to Play :",value="Use command `~guess (the letter)` to guess a consonant")
            embed.set_thumbnail(url='https://lh3.googleusercontent.com/Zx2bYc6anwawINc4OtTNcvav605vEdRSehu0uy_FyyCq3itAcQnv7POiG10jNSvo9xczjl1X1JmSQqOLoJx3DgCSgw=w640-h400-e365-rj-sc0x00ffffff')
            await ctx.send(embed=embed)            
            embed=discord.Embed(title='Guess this word', description=self.wordTillNow(), colour=discord.Color.random(seed=None))
            embed.set_footer(text=f'You have {wordGuesser_chances} chances to guess this word.')
            await ctx.send(embed=embed)
        else:
            await ctx.send("A game is already in progress! Finish it before starting a new one.")



    @commands.command(aliases=['g'])
    async def guess(self, ctx, letter:str):

        global wordGuesser_word
        global wordGuesser_gameover
        global wordGuesser_guessedLettters
        global wordGuesser_chances
        global wordGuesser_answer

        if not wordGuesser_gameover:
            if letter.lower() in ['a','e','i','o','u']:
                await ctx.send('Guess consonants only. Vowels are already given.')
            elif letter.lower() in wordGuesser_guessedLettters:
                await ctx.send('You have already gueessed this consonant.')
            elif letter.lower() not in ['q','w','r','t','y','p','s','d','f','g','h','j','k','l','z','x','c','v','b','n','m']:
                await ctx.send('Please guess singel consonant only.')
            else:
                wordGuesser_guessedLettters.append(letter.lower())
                wordGuesser_chances -=1
                self.wordTillNow()
                if wordGuesser_answer == wordGuesser_word:
                    wordGuesser_gameover = True
                    embed=discord.Embed(title='You have guessed the word', description=self.wordTillNow(), colour=discord.Color.green())
                    embed.set_footer(text=f'You have won.')
                    return await ctx.send(embed=embed)
                else:
                    if wordGuesser_chances !=0:
                        if letter.lower() in wordGuesser_word:
                            embed=discord.Embed(title='Correct letter', description=self.wordTillNow(), colour=discord.Color.green())
                            embed.set_footer(text=f'You have {wordGuesser_chances} chances left to guess this word.')
                            return await ctx.send(embed=embed)
                        else:
                            embed=discord.Embed(title='wrong letter', description=self.wordTillNow(), colour=discord.Color.red())
                            embed.set_footer(text=f'You have {wordGuesser_chances} chances left to guess this word.')
                            return await ctx.send(embed=embed)
                    else:
                        wordGuesser_gameover = True
                        embed=discord.Embed(title='You lost', description=f"The word was\n {self.theWord()}", colour=discord.Color.red())
                        embed.set_footer(text=f'No chances left.')
                        return await ctx.send(embed=embed)
        else:
            await ctx.send("Please start the game using `~wordGusser` to use this command and play the game.")

    def chances(self):
        global wordGuesser_chances
        global wordGuesser_word
        vowel=0
        for i in wordGuesser_word:
            if i in ['a','e','i','o','u']:
                vowel+=1
        wordGuesser_chances = int((len(wordGuesser_word)-vowel)*1.5)

    def wordTillNow(self):
        global wordGuesser_word
        global wordGuesser_guessedLettters
        global wordGuesser_answer
        wordGuesser_answer = ''
        wordTillNow=""
        for letter in wordGuesser_word:
          if letter in wordGuesser_guessedLettters:
            wordTillNow +=self.symbol_convertor(letter)
            wordGuesser_answer +=letter
          else:
            wordTillNow +=  ":white_large_square:" 
            wordGuesser_answer +=  "*"
        return wordTillNow

    def theWord(self):
        global wordGuesser_word
        word=''
        for letter in wordGuesser_word:
            word +=self.symbol_convertor(letter)
        return word

    def symbol_convertor(self, a):
        symbol=f":regional_indicator_{a}:"
        return symbol

    def give_word(self):
        global wordGuesser_list
        global wordGuesser_word
        wordGuesser_word = random.choice(wordGuesser_list).lower()
    
    @guess.error
    async def guess_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please enter a single consonant.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Please make sure it is an alphabet.")


def setup(bot):
    bot.add_cog(GuessTheWord(bot))