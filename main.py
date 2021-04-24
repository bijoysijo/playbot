import discord
import os
from dotenv import load_dotenv

load_dotenv()

client = discord.Client()

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  if message.content.startswith('$hello'):
    await message.channel.send('Hello!')

print(os.getenv('TOKEN', 'Token not found'))
# client.run('ODM1NDc4MDM0Nzg5Njk1NDk5.YIQBjQ.X9tKDh6Nvt8X3QRZZ8tZzxOU1rc')


