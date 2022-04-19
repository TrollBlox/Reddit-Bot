import json

with open("config.json", "r") as read_file:
  data = json.load(read_file)

async def cmdlogging(message, text):
  author = str(message.author.id)

  for i in range(len(data["coolids"])):
    author = author.replace(data["coolids"][i], data["coolnames"][i])

  date = message.created_at.strftime("%c")
  text = date + " - " + author + " " + text + " in " + message.guild.name + "."

  print(text)
  with open("archives.txt", "a") as f:
    f.write("\n" + str(text))

async def messagelogging(message):
  author = str(message.author.id)

  for i in range(len(data["coolids"])):
    author = author.replace(data["coolids"][i], data["coolnames"][i])
  
  date = message.created_at.strftime("%c")
  text = date + " - " + author + " said \"" + message.content + "\" in the guild " + message.guild.name + "."

  print(text)
  with open("messages.txt", "a") as f:
    f.write("\n" + str(text))
