import discord
import asyncio
import json

from discord.ext import commands
from better_profanity import profanity
from zCommands.zzCommands import Economy

class Check(commands.Cog):
  def __init__(self, bot):
    self.client = bot

  @commands.Cog.listener()
  async def on_ready(self):
    print('Now Checking Messages!')

  profanity.load_censor_words_from_file('jsons/badwords.txt')

  @commands.Cog.listener()
  async def on_message(self, message):
    content = message.content.replace("*", "")
    content = message.content.replace("|", "")
    content = message.content.replace("_", "")
    content = message.content.replace("`", "")
    content = message.content.replace("~", "")
    if not message.author.bot:
      if profanity.contains_profanity(content):
        mbed = discord.Embed(
          title = str(message.author) + ' ' + 'Has Been Warned For Using A Bad Word',
          description = "Ban Kardunga Pata Bhi Nhi Chalega! ;)",
          color = discord.Color.red()
        )
        await message.delete()
        await message.channel.send(embed = mbed)
        await message.author.send("You Can't Use That Word Here!")
        return
      else:
        if message.guild is not None:
          if not message.content.startswith('?'):
            Economy.increase_money(str(message.author.id))
          else: 
            return
        else:
          return

def setup(client):
  client.add_cog(Check(client))

