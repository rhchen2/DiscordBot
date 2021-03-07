import discord
import os
import requests

from dotenv import load_dotenv
from manga.manga_controller import manga_main
from randomFeatures.randomHelpers import *

client = discord.Client()
load_dotenv("config/.env")
TOKEN = os.getenv('DISCORD_TOKEN')

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

    if message.content.startswith('$randomfacts'):
        quote = get_random_fact()
        await message.channel.send(quote)

    if message.content.startswith('$manga'):
        msg = manga_main(message.content)
        await message.channel.send(msg)

client.run(TOKEN)
