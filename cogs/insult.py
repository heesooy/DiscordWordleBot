from datetime import datetime
from discord.ext import commands
from pytz import timezone
import utils
import random

class InsultCog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.insults = utils.get_insults_list()

  @commands.command('insult')
  @commands.has_any_role('The Principal', 'Bad Kid', 'Admin', 'DJ')
  async def insult(self, ctx, mention_id):
    if len(ctx.message.mentions) == 0:
      await ctx.send("You forgot to tag someone. I guess that makes YOU the idiot!")
      return
    user = ctx.message.mentions[0]
    insult = random.choice(self.insults)
    await ctx.send(user.mention + " " + insult)

def setup(bot):
  bot.add_cog(InsultCog(bot))