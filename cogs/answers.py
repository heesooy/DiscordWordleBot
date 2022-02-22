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

def setup(bot):
  bot.add_cog(AnswersCog(bot))