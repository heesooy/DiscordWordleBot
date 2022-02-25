from datetime import datetime
from discord.ext import commands
from pytz import timezone
from mongo import *
import utils

class AnswersCog(commands.Cog):
  def __init__(self, bot):
    self.answers = utils.get_answer_list()

  def get_answer(self, date):
    return self.answers[date]

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
    answer = self.get_answer(utils.now().date())
    if word == answer[0]:
      await ctx.send("Thats it! Copy paste your Wordle guess thing!")
      insert_wordle_record(ctx, answer)
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
    if message.channel.name != "wordle" and message.channel.name != "bot-testing":
      return
    if message.content.startswith("Wordle"):
      m = message.content.split(' ')
      num_guesses = int(m[2][0])
      stats = m[2][5:]
      tri = self.convertToTrinary(stats)
      if record_to_wordle_record(message, tri, num_guesses, utils.now().date()) == None:
        await message.channel.send("Please use `!answer` to verify your answer first.")
        return
      await message.channel.send("Recorded " + m[2][0] + f" guesses on Wordle #**{m[1]}**!")

  @commands.command('stats')
  async def stats(self, ctx):
    guesses = get_average_num_guesses(ctx.author)
    if guesses == None:
      await ctx.send("You have not made any guesses. Use `!answer` to answer todays Wordle")
      return
    await ctx.send(f"You have averaged **{guesses}** guesses per Wordle!")
  
def setup(bot):
  bot.add_cog(AnswersCog(bot))