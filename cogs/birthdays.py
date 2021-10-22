import discord
import asyncio
import datetime
import json
from discord.ext import commands, tasks

class Birthday(commands.Cog):
  def __init__(self, bot):
    self.client = bot

  @commands.Cog.listener()
  async def on_ready(self):
    print('Birthday Bot Ready!')
    self.checkForBirthdays.start()

  @tasks.loop(seconds = 86400)
  async def checkForBirthdays(self):
    print("Checking For Birthdays!")
    now = datetime.datetime.now()
    curmonth = now.month
    curday = now.day
    curyear = now.year

    with open('jsons/birthday.json', 'r') as f:
      var = json.load(f)
      for member in var:
        if var[member]['month'] == curmonth:
          if var[member]['day'] == curday:
            if var[member]['wished'] == 0:
              channel = self.client.get_channel(878999525258330112)
              year = var[member]["year"]
              await channel.send(f"**Happy Birthday <@{member}>!** You're Now {curyear-year} Old!🎉🎊")
              var[member]['wished'] = 1
              with open("jsons/birthday.json", "w") as f:
                json.dump(var, f)
        else:
          if var[member]['wished'] == 1:
            var[member]['wished'] == 0
            with open('jsons/birthday.json', "w") as f:
              json.dump(var, f)

  @commands.command()
  async def set_birthday(self ,ctx, day: int, month: int, year: int):
    try:
      if month > 13 or month < 1:
              await ctx.send("Please Enter A Valid Date!")
              return
      else:
        pass    
      if month in (1, 3, 5, 7, 8, 10, 12):
          if day > 31 or day < 1:
              await ctx.send("Please Enter A Valid Date!")
              return
          else:
              pass
      elif month in (4, 6, 9, 11):
          if day > 30 or day < 1:
              await ctx.send("Please Enter A Valid Date!")
              return
          else:
              pass
      elif month == 2:
          if day > 29 or day < 1:
              await ctx.send("Please Enter A Valid Date!")
              return
          else:
              pass
      else:
          await ctx.send("Please Enter A Valid Date!")
          return
    except:
        await ctx.send("Please Enter A Valid Date!")
        return
    
    with open("jsons/birthday.json", "r") as f:
      users = json.load(f)

    users[str(ctx.author.id)] = {}
    users[str(ctx.author.id)]['day'] = day
    users[str(ctx.author.id)]['month'] = month
    users[str(ctx.author.id)]['year'] = year
    users[str(ctx.author.id)]['wished'] = 0

    with open("jsons/birthday.json", "w") as f:
      json.dump(users, f)
    
    if month == 1:
      m = "January"
    elif month == 2:
      m = "February"
    elif month == 3:
      m = "March"
    elif month == 4:
      m = "April"
    elif month == 5:
      m = "May"
    elif month == 6:
      m = "June"
    elif month == 7:
      m = "July"
    elif month == 8:
      m = "August"
    elif month == 9:
      m = "September"
    elif month == 10:
      m = "October"
    elif month == 11:
      m = "November"
    elif month == 12:
      m = "December"
    
    if day == 1:
      e = "st"
    elif day == 2:
      e = "nd"
    elif day ==3:
      e= "rd"
    else:
      e = "th"

    await ctx.send(f"Duly Noted! I'll Wish {ctx.author} on **{day}{e}-{m}!**")

def setup(client):
  client.add_cog(Birthday(client))

