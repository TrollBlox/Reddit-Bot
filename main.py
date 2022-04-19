import json
import discord
import ucomments as ucomments
import uposts as uposts
import rcomments as rcomments
import rposts as rposts
import snsfw as nsfw
import help as h
from reddit import reddit

with open("config.json", "r") as read_file:
  readConfig = json.load(read_file)

with open("guilds.json", "r") as write_guilds:
  readGuilds = json.load(write_guilds)

redditor = reddit.redditor("trollblox_").saved()
allowed_mentions = discord.AllowedMentions(everyone = True)

class MyClient(discord.Client):
  async def on_ready(self):
    # await self.change_presence(activity = discord.Game(name = "!help"))
    print(f'Logged on as {self.user}!') #comment

  async def on_message(self, message):
    if message.author == self.user:
      return

    if message.content == "!help":
      await h.generalhelp(message)
      return

    if message.content[0:2] == "u/":
      text = message.content.split()
      if message.content == "u/" or message.content == "u/help":
        await h.uhelp(message)
        return
      elif text[1] == "comments":
        await ucomments.execute(message)
        return
      elif text[1] == "posts":
        await uposts.execute(message)
        return
      else:
        await message.channel.send("I don't recoginze that command!")
        return

    if message.content[0:2] == "r/":
      text = message.content.split()
      if message.content == "r/" or message.content == "r/help":
        await h.rhelp(message)
        return
      elif text[1] == "comments":
        await rcomments.execute(message)
        return
      elif text[1] == "posts":
        await rposts.execute(message)
        return
      else:
        await message.channel.send("I don't recognize that command!")
        return

    if message.content[0:2] == "s/":
      text = message.content.split()
      if message.content == "s/" or message.content == "s/help":
        await h.shelp(message)
        return
      elif text[0][2:] == "nsfw":
        await nsfw.execute(message)
        return
      else:
        await message.channel.send("I don't recognize that command!")
        return
  
  async def on_guild_join(self, guild):
    with open("guilds.json",'r+') as file:
      file_data = json.load(file)
      readGuilds["guildids"].append(str(guild.id))
      readGuilds["nsfwposts"].append(False)
      file.seek(0)
      json.dump(file_data, file, indent = 4)

client = MyClient()
client.run(readConfig["token"])
