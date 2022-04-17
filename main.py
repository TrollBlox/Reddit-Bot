from multiprocessing.sharedctypes import Value
import time
import praw
from prawcore.exceptions import NotFound
import json
import discord

with open("config.json", "r") as read_file:
  data = json.load(read_file)

reddit = praw.Reddit(
  client_id = data["client_id"],
  client_secret = data["client_secret"],
  user_agent = data["user_agent"],
  username = data["username"],
  password = data["password"],
  check_for_async = False,
)

redditor = reddit.redditor("trollblox_").saved()
allowed_mentions = discord.AllowedMentions(everyone = True)

class MyClient(discord.Client):
  async def on_ready(self):
    print(f'Logged on as {self.user}!')

  async def on_message(self, message):
    if message.author == client.user:
      return

    if message.content[0] == "$":
      text = message.content.split()
      limit = 0
      if len(text) == 1:
        limit = 10
      else:
        limit = text[1]
      try:
        if limit == "all":
          redditor = reddit.redditor(text[0][1:]).comments.new(limit = None)
        else: 
          redditor = reddit.redditor(text[0][1:]).comments.new(limit = int(limit))
      except NotFound:
        await message.channel.send("Could not find that user!")
      except ValueError:
        await message.channel.send("Not a valid number!")

      for comment in redditor:
        try:
          # await message.channel.send(content = "@everyone " + comment.body, allowed_mentions = allowed_mentions)
          await message.channel.send("```\n" + comment.body + "\n```")
          time.sleep(1)
        except:
          await message.channel.send("Something went wrong displaying the comment!")

client = MyClient()
client.run(data["token"])
