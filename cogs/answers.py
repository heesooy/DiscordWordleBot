from datetime import datetime
from discord.ext import commands
from pytz import timezone
import utils

class AnswersCog(commands.Cog):
  def __init__(self, bot):
    self.answers = utils.get_answer_list()

  def get_answer(self, date):
    return self.answers[date]

  @commands.command('answer')
  async def answer(self, ctx, word):
    tz = timezone('US/Pacific')
    today = datetime.now(tz).date()
    if word == self.get_answer(today):
      await ctx.send("Thats it!")
      await ctx.message.delete()
    else:
      await ctx.send("You stupid.")
      await ctx.message.delete()

  @commands.command('record')
  async def record(self, ctx, *args):
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
      await message.channel.send(m[2][0] + " guesses!")


def setup(bot):
  bot.add_cog(AnswersCog(bot))