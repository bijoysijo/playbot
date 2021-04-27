import discord
import os
from dotenv import load_dotenv
import requests
import json
import random
from deta import Deta

#to load .env file
load_dotenv()

#deta base
deta = Deta(os.getenv('DETA_PROJECT_KEY'))
deta.Base("encouragements")

#method to return db
def getdb(name):
  return deta.Base(name)

#establish connection with discord client
client = discord.Client()

#generics
sad_words = ["sad", "depressed", "unhappy", "angry", "miserable"]
starter_encouragements = ["Cheer up!", "Hang in there.", "You are a great person / bot!"]

#to get encouraging quotes
def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

#update db with user supplied encouraging message
def update_encouragements_table(encouraging_message):
  db = getdb("encouragements")
  if db.get("encouragements"):
    updates = {"cheerios": db.util.append(encouraging_message)}
    db.update(updates, "encouragements")
  else:
    db.put({"cheerios": [encouraging_message]}, "encouragements")

#delete user requested encouraging message from db
def delete_from_encouragements_table(index):
  db = getdb("encouragements")
  encouragements_list = db.get("encouragements")["cheerios"]
  if index in encouragements_list:
    encouragements_list.remove(index)
    db.delete("encouragements")
    db.put({"cheerios": encouragements_list}, "encouragements")
    return encouragements_list
  else:
    return "Item not in list"

#intializer event
@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

#on_message events
@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('$hello'):
    await message.channel.send('Hello!')

  if message.content.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)

  if message.content.startswith('$new'):
    encouraging_message = message.content.split('$new ', 1)[1]
    update_encouragements_table(encouraging_message)
    await message.channel.send("New encouraging message added")

  if message.content.startswith('$del'):
    db = getdb("encouragements")
    if db.get("encouragements"):
      index = message.content.split("$del",1)[1].lstrip()
      info = delete_from_encouragements_table(index)
      await message.channel.send(info)

  if message.content.startswith("$list"):
    encouragements = []
    db = getdb("encouragements")
    if db.get("encouragements"):
      encouragements = db.get("encouragements")["cheerios"]
    await message.channel.send(encouragements)

  if any(word in message.content for word in sad_words):
    db = getdb("encouragements")
    if db.get("encouragements")["cheerios"]:
      await message.channel.send(random.choice(db.get("encouragements")["cheerios"]))
    else:
      await message.channel.send(random.choice(starter_encouragements))


#to establish connection with client using bot token
client.run(os.getenv('TOKEN', 'Token not found'))




