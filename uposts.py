import datetime
import time
from reddit import reddit
import discord
from prawcore.exceptions import NotFound
import json

with open("config.json", "r") as read_file:
  data = json.load(read_file)

# Command order u/user posts sort type amount
#                 0      1     2    3    4

async def execute(message):
  message_content = message.content.split()

  if len(message_content) == 1:
    await help(message)
    return

  limit = 0
  if len(message_content) == 4 or message_content[4] == "default":
    limit = 1
  elif message_content[4] == "max":
    limit = 5
  else: 
    try:
      limit = int(message_content[4])
    except ValueError:
      await message.channel.send("Invalid number!")
      return
  
  if limit > 5:
    await message.channel.send("You cannot request more than 5 posts at a time!")
    return

  try:
    collection = reddit.redditor(message_content[0][2:]).submissions
  except NotFound:
    await message.channel.send("Couldn't find that user!")
    return

  if message_content[2] == "best":
    posts = collection.best(limit = None)
  elif message_content[2] == "hot":
    posts = collection.hot(limit = None)
  elif message_content[2] == "new":
    posts = collection.new(limit = None)
  elif message_content[2] == "top":
    posts = collection.top("month", limit = None)
  elif message_content[2] == "rising" or "rise":
    posts = collection.rising(limit = None)
  elif message_content[2] == "controversial" or "con":
    posts = collection.controversial("month", limit = None)
  else:
    await message.channel.send("Couldn't find that sort!")
    return

  if message_content[3] == "all":
    image = True
    gif = True
    text = True
  elif message_content[3] == "image":
    image = True
    gif = False
    text = False
  elif message_content[3] == "gif":
    image = False
    gif = True
    text = False
  elif message_content[3] == "text":
    image = False
    gif = False
    text = True
  elif message_content[3] == "media":
    image = True
    gif = True
    text = False
  else:
    await message.channel.send("Couldn't find that post type!")
    return

  messages = 0
  for post in posts:
    post_is_text = False
    if post.is_self:
      post_is_text = True
      if not text:
        continue
    elif (".png" in post.url or ".jpg" in post.url) and not image:
      continue
    elif ".gif" in post.url and not gif:
      continue
    elif "gallery" in post.url:
      continue
    elif "v.redd.it" in post.url:
      continue
    
    if post.over_18 and not data["nsfwposts"]:
      await message.channel.send("NSFW posts are disabled!")
      messages += 1
      continue

    if post_is_text:
      if post.selftext == "":
        post.selftext = "[no description provided]"
      if len(post.selftext) > 4093:
        extra = "..."
      else:
        extra = ""
      embed = discord.Embed(title = post.title, url = "https://www.reddit.com" + post.permalink, description = post.selftext[0:4092] + extra, color = 0xff4500)
    else:
      embed = discord.Embed(title = post.title, url = "https://www.reddit.com" + post.permalink, color = 0xff4500)
      embed.set_image(url = post.url)

    time_posted = post.created

    embed.set_author(name = "/r/" + post.subreddit.display_name, url = "https://www.reddit.com/r/" + post.subreddit.display_name, icon_url = post.subreddit.icon_img)
    embed.set_footer(text = "/u/" + post.author.name, icon_url = post.author.icon_img)
    embed.timestamp = datetime.datetime.fromtimestamp(time_posted)

    await message.channel.send(embed = embed)
    time.sleep(1)
    messages += 1
    if messages >= limit:
      return

async def help(message):
  await message.channel.send("Format for posts command: u/[user] posts [the way to sort the posts (top, hot, etc.)] [the type of comment (image, text, gif, media)] [the number of posts. max = 5, default = 1]")
  return
