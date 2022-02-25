from datetime import datetime
from discord.ext import commands
from pytz import timezone
from mongo import *
import utils

class AnswersCog(commands.Cog):
  def __init__(self, bot):
    self.answers = utils.get_answer_list()

  def get_answer(self, date):
    return self.answers[date][0]

  def convertToTrinary(self, record):
    trinary = ""
    guesses = record.split('\n')
    for guess in guesses:
      for letter in guess:
        if letter == '⬛':
          trinary += '0'
        elif letter == '🟨':
          trinary += '1'
        elif letter == '🟩':
          trinary += '2'
    return trinary

  def convertFromTrinary(self, record):
    guesses = ""
    for i in range(len(record)):
      if record[i] == '0':
        guesses += '⬛'
      elif record[i] == '1':
        guesses += '🟨'
      elif record[i] == '2':
        guesses += '🟩'
      if i % 5 == 4 and i != len(record) - 1:
        guesses += '\n'
    return guesses


  @commands.command('answer')
  async def answer(self, ctx, word):
    print(utils.now().date())
    if word == self.get_answer(utils.now().date()):
      await ctx.send("Thats it! Copy paste your Wordle guess thing!")
      # insert_wordle_record(ctx, word)
      await ctx.message.delete()
    else:
      await ctx.send("You stupid.")
      await ctx.message.delete()

  @commands.command('record')
  async def record(self, ctx, *args):
    await ctx.channel.send("Dont use this!")
    return
    if ctx.channel.name != "wordle":
      return
    guesses = args[2][0]
    await ctx.send(f"It took you {guesses} guesses!")
  
  @commands.Cog.listener()
  async def on_message(self, message):
    if message.channel.name != "wordle":
      return
    if message.content.startswith("Wordle"):
      
      m = message.content.split(' ')
      print(m)
      await message.channel.send(m[2][0] + f" guesses on Wordle #**{m[1]}**!")
      stats = m[2][5:]
      tri = self.convertToTrinary(stats)



def setup(bot):
  bot.add_cog(AnswersCog(bot))