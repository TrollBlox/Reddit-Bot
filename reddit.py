import praw
import json

with open("config.json", "r") as read_file:
  data = json.load(read_file)


reddit = praw.Reddit(
  client_id = data["client_id"],
  client_secret = data["client_secret"],
  user_agent = data["user_agent"],
  check_for_async = False,
)