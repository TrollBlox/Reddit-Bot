from datetime import datetime
import time
from reddit import reddit
import discord
import loggin as log
from prawcore.exceptions import NotFound

# Command order u/user comments sort amount
#                 0      1         2     3

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
    collection = reddit.redditor(message_content[0][2:]).comments
  except NotFound:
    await message.channel.send("Couldn't find that user!")
    return

  if message_content[2] == "best":
    comments = collection.best(limit = None)
  elif message_content[2] == "hot":
    comments = collection.hot(limit = None)
  elif message_content[2] == "new":
    comments = collection.new(limit = None)
  elif message_content[2] == "top":
    comments = collection.top("month", limit = None)
  elif message_content[2] == "controversial" or "con":
    comments = collection.controversial("month", limit = None)
  else:
    await message.channel.send("Couldn't find that sort!")
    return

  messages = 0
  for comment in comments:

    if len(comment.body) > 4093:
      extra = "..."
    else:
      extra = ""
    embed = discord.Embed(title = "Comment from: " + comment.submission.title, url = "https://www.reddit.com" + comment.submission.permalink, description = comment.body[0:4092] + extra, color = 0xff4500)

    time_posted = comment.created

    embed.set_author(name = "r/" + comment.subreddit.display_name, url = "https://www.reddit.com/r/" + comment.subreddit.display_name, icon_url = comment.subreddit.icon_img)
    embed.set_footer(text = "u/" + comment.author.name, icon_url = comment.author.icon_img)
    embed.timestamp = datetime.fromtimestamp(time_posted)

    await message.channel.send(embed = embed)
    time.sleep(1)
    messages += 1
    if messages >= limit:
      log.cmdlogging(message, "viewed comments from u/" + comment.author.name)
      return

async def help(message): # TODO: fix this
  await message.channel.send("Format for comments command: u/[user] comments [the way to sort the comments (top, hot, etc.)] [the number of comments. max = 5, default = 1]")
  return
