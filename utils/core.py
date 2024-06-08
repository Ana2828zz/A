import discord
import json
import os
from discord.ext.commands import Bot

with open('utils/configData.json') as f:
    configData = json.load(f)

client = Bot(command_prefix = configData['PREFIX'], intents=discord.Intents.all())

@client.event
async def on_ready():
    await client.tree.sync()
    print('Ready to use!')

async def loadCogs():
    for filename in os.listdir('./commands'):
        if filename.endswith('.py'):
            await client.load_extension(f'commands.{filename[:-3]}')