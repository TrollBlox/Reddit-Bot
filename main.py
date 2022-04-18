import json
import discord
import ucomments as ucomments
import uposts as uposts
import rcomments as rcomments
import rposts as rposts
import loggin as log
from reddit import reddit

with open("config.json", "r") as read_file:
  data = json.load(read_file)

redditor = reddit.redditor("trollblox_").saved()
allowed_mentions = discord.AllowedMentions(everyone = True)

class MyClient(discord.Client):
  async def on_ready(self):
    print(f'Logged on as {self.user}!')

  async def on_message(self, message):
    if message.author == client.user:
      return

    if message.content[0:2] == "u/" or message.content[0:2] == "r/":
      await log.cmdlogging(message)
    else:
      await log.messagelogging(message)

    if message.content[0:2] == "u/":
      text = message.content.split()
      if text[1] == "comments":
        await ucomments.execute(message)
      if text[1] == "posts":
        await uposts.execute(message)

    if message.content[0:2] == "r/":
      text = message.content.split()
      if text[1] == "comments":
        await rcomments.execute(message)
      if text[1] == "posts":
        await rposts.execute(message)

client = MyClient()
client.run(data["token"])
