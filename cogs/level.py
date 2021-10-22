import discord
import os
import json
import asyncio

from discord import Member, File
from discord.ext import commands
from datetime import *
from pymongo import MongoClient
from typing import Optional
from zCommands.zzCommands import Levels
from easy_pil import Editor, Canvas, load_image_async, Font

level = ['Level-5+', 'Level-10+', 'Level-15+', 'Level-20+', 'Level-25+', 'Level-30+', 'Level-40+', 'Level-50+', 'Level-75+', 'Level-100+', 'Level-150+']
levelnum = [5, 10, 15, 20, 25, 30, 40, 50, 75, 100, 150]

my_secret = os.environ['clusterr']
cluster = MongoClient(my_secret)

levelling = cluster["DiscordBot"]["Levelling"]

numbers = ("1️⃣", "2⃣", "3⃣", "4⃣", "5⃣",
		   "6⃣", "7⃣", "8⃣", "9⃣", "🔟")

class Levelsys(commands.Cog):

  def __init__(self, bot):
    self.client = bot
    self.polls = []

  @commands.Cog.listener()
  async def on_ready(self):
    print('Levelling System Now Online!')

  @commands.Cog.listener()
  async def on_message(self, message):
    if not message.content.startswith('?'):
      if message.guild is not None:
        if message.author.bot:
          return
        recieved_data = Levels.increase_xp(str(message.author.id), str(message.guild.id), int(20))
        if recieved_data == "NONE":
          return
        else:
          data = recieved_data.split(" ")
          if data[0] == "NEW-LEVEL":
            await message.channel.send(f"{message.author.mention} Just Leveled Up To **Level: {data[1]}**!")
          elif data[0] == "NEW-LEVEL-ROLES":
            await message.author.add_roles(discord.utils.get(message.author.guild.roles, name=data[2]))
            mbed = discord.Embed(title=f"{message.author} You Have Gotten role **{data[2]}**!", color = message.author.colour)
            mbed.set_thumbnail(url=message.author.avatar_url)
            await message.channel.send(embed=mbed)
          else:
            print("LOL ERROR")

  @commands.command()
  async def rank(self, ctx, user: Optional[discord.Member]):
    if ctx.guild is not None:
      userr = user or ctx.author
      file = await Levels.make_user_rank_card(str(ctx.author.guild.id), userr.id, userr.avatar_url, str(userr))
      await ctx.send(file=file)
    else:
      await ctx.send("Rank Command Isn't Available In Bot DM")

  @commands.command()
  async def backgrounds(self, ctx):
    if ctx.guild is None:
      for i in range(0, 4):
        file = File(filename=f"images/{i}.png")
        await ctx.send(file=file)

  @commands.command()
  async def change_background(ctx):
    pass

  @commands.command()
  async def leaderboard(self, ctx):
    rankings = levelling.find().sort("xp",-1)
    i = 1
    mbed = discord.Embed(title="Rankings: ", color = discord.Color.from_rgb(102, 204, 255))
    for x in rankings:
      try:
        temp = ctx.guild.get_member(x["id"])
        tempxp = x["xp"]
        lvl = 0
        while True:
          if tempxp < ((50*(lvl**2))+(50*lvl)):
            break
          lvl +=1
        mbed.add_field(name=f"{i}: {temp.name}", value=f"Level: {lvl}")
      except:
        pass
      if i == 11:
        break
    await ctx.send(embed = mbed)

  @commands.command()
  @commands.has_role("Server-Mod")
  async def increase_xp(self, ctx, userid: str, increaseby: int):
    Levels.increase_xp(userid, ctx.author.id, increaseby)
    await ctx.send(f"Increased Xp by {increaseby}; if your level is increased then this won't tell")

  @commands.command()
  @commands.has_role("Server-Mod")
  async def decrease_xp(self, ctx, userid: str, decreaseby: int):
    Levels.decrease_xp(userid, ctx.author.id, decreaseby)
    await ctx.send(f"Decreased Xp by {decreaseby}; if your level is decreased then this won't tell")
  
  @commands.command(name="mkpoll")
  async def create_poll(self, ctx, hours: int, question: str, *options):
    if len(options) > 10:
      await ctx.send("You Can Only Supply a Maximum Of 10 Options!")
    else:
      mbed = discord.Embed(
        title=f"Poll By {ctx.author}",
        description=question,
        color = ctx.author.colour,
        timestamp=datetime.utcnow()
      )
      fields = [("Options", "\n".join([f"{numbers[idx]} {option}" for idx, option in enumerate(options)]), False),
            ("Instructions", "React to cast a vote!", False)]
      
      for name, value, inline in fields:
        mbed.add_field(name=name, value=value, inline=inline)
      
      message = await ctx.send(embed=mbed)
      await ctx.message.delete()

      for emoji in numbers[:len(options)]:
        await message.add_reaction(emoji)

      self.polls.append((message.channel.id, message.id))

      await asyncio.sleep(hours)

      print(message.reactions)

      cache_msg = discord.utils.get(self.client.cached_messages, id=message.id)
      
      most_voted = max(cache_msg.reactions, key=lambda r: r.count)
      await cache_msg.delete()
      await ctx.send(f"The results are in and option {most_voted.emoji} was the most popular with {most_voted.count-1:,} votes!")
    


def setup(client):
  client.add_cog(Levelsys(client))

