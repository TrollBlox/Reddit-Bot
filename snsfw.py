import json
import loggin as log

async def execute(message):
  with open("guilds.json") as read_file:
    data = json.load(read_file)
  jsonguildentrynum = 0
  for id in data["guildids"]:
    if str(message.guild.id) in id:
      break
    jsonguildentrynum += 1
  text = message.content.split()

  if len(text) == 1:
    await log.cmdlogging(message, "viewed current nsfw settings in the guild " + message.guild.name)
    if data["nsfwposts"][jsonguildentrynum]:
      await message.channel.send("NSFW posts are enabled!")
      return
    else:
      await message.channel.send("NSFW posts are disabled!")
      return

  if not message.author.guild_permissions.administrator:
    await message.channel.send("You do not have permissions to change NSFW settings!")
    return
  
  if text[1] == "enable" or text[1] == "true" or text[1] == "on":
    if data["nsfwposts"][jsonguildentrynum] == True:
      await message.channel.send("NSFW posts are already enabled!")
      return
    data["nsfwposts"][jsonguildentrynum] = (True)
    with open("guilds.json", "w") as f:
      json.dump(data, f)
    await message.channel.send("Enabled NSFW posts!")
    await log.cmdlogging(message, "enabled nsfw posts in the guild " + message.guild.name)
  elif text[1] == "disable" or text[1] == "false" or text[1] == "off":
    if data["nsfwposts"][jsonguildentrynum] == False:
      await message.channel.send("NSFW posts are already disabled!")
      return
    data["nsfwposts"][jsonguildentrynum] = (False)
    with open("guilds.json", "w") as f:
      json.dump(data, f)
    await message.channel.send("Disabled NSFW posts!")
    await log.cmdlogging(message, "disabled nsfw posts in the guild " + message.guild.name)
  else:
    await message.channel.send("I don't understand!")
    return

async def help(message):
  message.channel.send("Help for s/nsfw")
