import discord
import loggin as log

async def generalhelp(message):
  embed = discord.Embed(title = "Reddit Help", description = "Commands:\nr/[subreddit] - search inside a subreddit\nu/[user] - search inside a user\ns/[setting] - change settings for the robot\n\nUse the prefix (ex. s/) to get a command specific help menu!", color = 0xff4500)
  await message.channel.send(embed = embed)
  await log.cmdlogging(message, "got general help")
  return

async def uhelp(message):
  embed = discord.Embed(title = "u/ Help", description = "Command format:\n\nu/[user] comments [way to sort (ex. hot, top)] [amount (default = 1, max = 5)]\nu/[user] posts [way to sort (ex. hot, top)] [type (ex. image, text)] [amount (default = 1, max = 5)]", color = 0xff4500)
  await message.channel.send(embed = embed)
  await log.cmdlogging(message, "got u/ help")
  return

async def rhelp(message):
  embed = discord.Embed(title = "r/ Help", description = "Command format:\n\nr/[subreddit] comments [way to sort (ex. hot, top)] [amoutn (default = 1, max = 5)]\nr/[subreddit] posts [way to sort (ex. hot, top)] [type (ex. image, text)] [amount (default = 1, max = 5)]", color = 0xff4500)
  await message.channel.send(embed = embed)
  await log.cmdlogging(message, "got r/ help")
  return

async def shelp(message):
  embed = discord.Embed(title = "s/ Help", description = "Settings:\n\ns/nsfw [Optional: enable/disable] - returns whether or not nsfw posts are enabled, and change the availability. Only server administrators can change this setting.", color = 0xff4500)
  await message.channel.send(embed = embed)
  await log.cmdlogging(message, "got s/ help")
  return
