import json
import discord
import ucomments as ucomments
import uposts as uposts
import rcomments as rcomments
import rposts as rposts
import loggin as log
import snsfw as nsfw
from reddit import reddit

with open("config.json", "r") as read_file:
  readConfig = json.load(read_file)

with open("guilds.json", "r") as write_guilds:
  readGuilds = json.load(write_guilds)

redditor = reddit.redditor("trollblox_").saved()
allowed_mentions = discord.AllowedMentions(everyone = True)

class MyClient(discord.Client):
  async def on_ready(self):
    print(f'Logged on as {self.user}!')

  async def on_message(self, message):
    if message.author == self.user:
      return

    if message.content[0:2] == "u/":
      text = message.content.split()
      if text[1] == "comments":
        await ucomments.execute(message)
      elif text[1] == "posts":
        await uposts.execute(message)
      else:
        await message.channel.send("I don't recoginze that command!")

    if message.content[0:2] == "r/":
      text = message.content.split()
      if text[1] == "comments":
        await rcomments.execute(message)
      elif text[1] == "posts":
        await rposts.execute(message)
      else:
        await message.channel.send("I don't recognize that command!")

    if message.content[0:2] == "s/":
      text = message.content.split()
      if text[0][2:] == "nsfw":
        await nsfw.execute(message)
      else:
        await message.channel.send("I don't recognize that command!")
  
  async def on_guild_join(self, guild):
    with open("guilds.json",'r+') as file:
      file_data = json.load(file)
      readGuilds["guildids"].append(str(guild.id))
      readGuilds["nsfwposts"].append(False)
      file.seek(0)
      json.dump(file_data, file, indent = 4)

client = MyClient()
client.run(readConfig["token"])
