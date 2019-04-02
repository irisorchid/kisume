import os
import asyncio
import random
import time

import discord
import websockets

from discord.ext import commands
from dotenv import load_dotenv

import showdown

load_dotenv(verbose=True)
discord_token = os.getenv('discord_token')
discord_channel_id = os.getenv('discord_channel_id') #for channel specific stuff

#TODO:
def dynamic_prefix(bot, message):
    return '!'

bot = commands.Bot(command_prefix='!')

instance = showdown.Showdown(bot, os.getenv('showdown_username'), os.getenv('showdown_password'))


def load_commands(outbot):
    @outbot.command()
    async def hello2(ctx):
        await ctx.send('hello2')
            
class FOOBAR:
    
    def __init__(self, bot):
        self.bot = bot
        self.timer = 10
        self.bot_time = 0
        load_commands(self.bot)
    

food = FOOBAR(bot)
        
print(showdown.bot2)

@bot.event
async def on_ready():
    print('Hello World')

"""
@bot.event
async def on_message(message):
    if message.content.startswith('!echo'):
        print('ldkasfhkjhfjkas')
"""
async def back(food):
    await asyncio.sleep(food.timer)
    food.timer = time.time() - food.bot_time
    if food.timer >= 10:
        print('TIMEOUT')
    else:
        food.timer = 10 - food.timer
        print(food.timer)
    
@bot.command()
async def hello(ctx):
    await ctx.send('Hello World')

@bot.command()
async def echo(ctx, *, content:str):
    await ctx.send(content)
    
@bot.command()
async def choose(ctx, *, content:str):
    pick_one = [x.strip() for x in content.split(',') if x.strip() != '']
    choices = len(pick_one)
    if (choices == 0):
        return
    await ctx.send(pick_one[random.randrange(choices)])
    
@bot.command(name='showdown')
async def pokemon(ctx):
    food.bot_time = time.time()
    #bot.loop.create_task(back())
    await instance.run_timeout_instance(ctx)
    #await here shouldn't run until instance times out
    print('showdown end test')
    await ctx.send('showdown end test')

@bot.command(name='unravel')
async def test(ctx):
    #print stuff about server
    print(ctx.message.content)
    print(ctx.channel)    
    
@bot.command()
async def test2(ctx):
    await instance.test(ctx)
    
@bot.command()
async def switch(ctx, *, content:str):
    food.bot_time = time.time()
    await instance.switch(content)
    
@bot.command()
async def kusoge(ctx):
    #cleanup maybe? instance.close()
    await bot.logout()
    
bot.run(discord_token)