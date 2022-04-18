from datetime import datetime
import random
import time
from reddit import reddit
import discord
import loggin as log
from prawcore.exceptions import NotFound

# Command order r/subreddit comments sort amount
#                 0            1       2     3

async def execute(message):
  message_content = message.content.split()

  if len(message_content) == 1:
    await help(message)
    return

  limit = 0
  if len(message_content) == 3 or message_content[3] == "default":
    limit = 1
  elif message_content[3] == "max":
    limit = 5
  else: 
    try:
      limit = int(message_content[3])
    except ValueError:
      await message.channel.send("Invalid number!")
      return
  
  if limit > 5:
    await message.channel.send("You cannot request more than 5 comments at a time!")
    return

  try:
    collection = reddit.subreddit(message_content[0][2:])
  except NotFound:
    await message.channel.send("Couldn't find that subreddit!")
    return

  if message_content[2] == "best":
    submissions = collection.best(limit = None)
  elif message_content[2] == "hot":
    submissions = collection.hot(limit = None)
  elif message_content[2] == "new":
    submissions = collection.new(limit = None)
  elif message_content[2] == "top":
    submissions = collection.top("month", limit = None)
  elif message_content[2] == "controversial" or "con":
    submissions = collection.controversial("month", limit = None)
  else:
    await message.channel.send("Couldn't find that sort!")
    return

  messages = 0
  for submission in submissions:
    if random.randint(0, 1) == 0:
      continue
    for i in range(limit):
      if len(submission.comments[i].body) > 4093:
        extra = "..."
      else:
        extra = ""
      embed = discord.Embed(title = "Comment from: " + submission.title, url = "https://www.reddit.com" + submission.permalink, description = submission.comments[i].body[0:4092] + extra, color = 0xff4500)

      time_posted = submission.comments[i].created

      embed.set_author(name = "r/" + submission.subreddit.display_name, url = "https://www.reddit.com/r/" + submission.subreddit.display_name, icon_url = submission.subreddit.icon_img)
      embed.set_footer(text = "u/" + submission.comments[i].author.name, icon_url = submission.comments[i].author.icon_img)
      embed.timestamp = datetime.fromtimestamp(time_posted)

      await message.channel.send(embed = embed)
      time.sleep(1)
      messages += 1
      if messages >= limit:
        break
    log.cmdlogging(message, "view comments from r/" + submission.subreddit.display_name)
    return

async def help(message): # TODO: fix this
  await message.channel.send("Format for comments command: r/[subreddit] comments [search criteria for the post in the subreddit] [the way to sort the comments (top, hot, etc.)] [the number of comments. max = 5, default = 1]")
  return
