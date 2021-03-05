import discord
import os
import requests
import json

from dotenv import load_dotenv

client = discord.Client()
load_dotenv(".env")

def get_cat_facts():
  response = requests.get("https://meowfacts.herokuapp.com/")
  json_data = json.loads(response.text)
  facts = json_data['data']
  return(facts)

def get_inspiring_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$inspire'):
        quote = get_inspiring_quote()
        await message.channel.send(quote)

    if message.content.startswith('$catfacts'):
        quote = get_cat_facts()
        await message.channel.send(quote)

client.run(os.getenv('TOKEN'))
