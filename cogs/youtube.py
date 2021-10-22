import discord
import requests
import asyncio
import json
import re
import os

from discord.ext import commands, tasks

class Youtube(commands.Cog):
  def __init__(self, bot):
    self.client = bot

  @commands.Cog.listener()
  async def on_ready(self):
    print('Now Checking For Videos!')
    self.checkforvideo.start()

    
  @tasks.loop(seconds = 60)
  async def checkforvideo(self):
    with open("jsons/data.json", "r") as f:
      data = json.load(f)
    
    if data is not None:
      for ytchannelid in data:
        if ytchannelid is not None:
          channel = "https://www.youtube.com/channel/"+ytchannelid
          html = requests.get(channel + "/videos").text
          url = "https://www.youtube.com/watch?v=" + re.search('(?<="videoId":").*?(?=")', html).group()

          if not data[ytchannelid]["latest_video"] == url:
            data[ytchannelid]["latest_video"] = url
            discordchannel = data[ytchannelid]["dcchannelid"]
            channel = self.client.get_channel(discordchannel)
            msg = data[ytchannelid]["text"]
            await channel.send(f"{msg} {url}")

            with open("jsons/data.json", "w") as f:
              json.dump(data, f)

def setup(client):
  client.add_cog(Youtube(client))
