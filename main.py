import os
import discord
from discord.ext import commands

from dotenv import load_dotenv

#dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(verbose=True)

discord_bot_token = os.getenv('discord_bot_token')

client = commands.Bot(command_prefix = '.')

@client.event
async def on_ready():
    print('Hello World')
    
client.run(discord_bot_token)