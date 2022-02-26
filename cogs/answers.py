from datetime import datetime
from discord.ext import commands
from pytz import timezone
from mongo import *
import utils

class AnswersCog(commands.Cog):
  def __init__(self, bot):
    self.answers_by_date, self.answers_by_number = utils.get_answer_list()

  def get_answer_by_date(self, date):
    return self.answers_by_date[date]
  def get_answer_by_number(self, num):
    return self.answers_by_number[num]

  def convertToTrinary(self, record):
    trinary = ""
    guesses = record.split('\n')
    for guess in guesses:
      for letter in guess:
        if letter == '🟨' or letter == '🟦':
          trinary += '1'
        elif letter == '🟩' or letter == '🟧':
          trinary += '2'
        else: 
          trinary += '0'
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
  async def answer(self, ctx):
    await ctx.send("Apparently this sends notifs w the answer to people so uh, don't use this. Just paste ur copy pasta.")
    return
    # answer = self.get_answer(utils.now().date())
    # if word == answer[0]:
    #   await ctx.send("Thats it! Copy paste your Wordle guess thing!")
    #   insert_wordle_record(ctx, answer)
    #   await ctx.message.delete()
    # else:
    #   await ctx.send("You stupid.")
    #   await ctx.message.delete()

  @commands.command('record')
  async def record(self, ctx, *args):
    await ctx.channel.send("Dont use this!")
    return
    # if ctx.channel.name != "wordle":
    #   return
    # guesses = args[2][0]
    # await ctx.send(f"It took you {guesses} guesses!")
  
  @commands.Cog.listener()
  async def on_message(self, message):
    if message.channel.name != "wordle" and message.channel.name != "bot-testing":
      return
    if message.content.startswith("Wordle"):
      m = message.content.split(' ')
      if len(m) != 3:
        await message.channel.send("Don't be a dick and try to break the bot...")
        return
      num_guesses = int(m[2][0])
      wordle_num = int(m[1])
      stats = m[2][5:]
      tri = self.convertToTrinary(stats)
      answer = self.get_answer_by_number(wordle_num)
      if answer[0] != utils.now().date():
        await message.channel.send("You cannot answer for a previous day!")
        return
      if insert_wordle_record(message, answer, tri, num_guesses) == None:
        await message.channel.send("You have already answered for this day!")
        return
      await message.channel.send("Recorded " + m[2][0] + f" guesses on Wordle #**{m[1]}**!")

  @commands.command('stats')
  async def stats(self, ctx):
    guesses = get_average_num_guesses(ctx.author)
    if guesses == None:
      await ctx.send("You have not made any guesses. Paste your thing!")
      return
    await ctx.send(f"You have averaged **{guesses}** guesses per Wordle!")
  
def setup(bot):
  bot.add_cog(AnswersCog(bot))