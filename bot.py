import discord
from discord.ext import commands
import os, dotenv
from datetime import datetime
from pytz import timezone

dotenv.load_dotenv()

intents = discord.Intents(members=True, messages=True, reactions=True, guilds=True)
bot = commands.Bot(command_prefix='!', intents=intents)

for filename in os.listdir("./cogs"): # Change "cogs" to your folder name
    if filename.endswith(".py"):
      extension = f"cogs.{filename[:-3]}"
      bot.load_extension(extension)

@bot.event
async def on_ready():
  print('We have logged in as {0.user}'.format(bot))

@bot.command()
async def ping(ctx):
  await ctx.send("Pong!")
  tz = timezone('EST')
  await ctx.send(datetime.now(tz))

@bot.command()
@commands.is_owner() 
async def restart(ctx):
  for filename in os.listdir("./cogs"): 
    if filename.endswith(".py"):
      cog = f"cogs.{filename[:-3]}"
      bot.reload_extension(cog)
  await ctx.send("Reloading...")

bot.run(f"{os.getenv('ENV')}")