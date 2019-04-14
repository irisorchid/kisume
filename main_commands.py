import random

#TODO:
def dynamic_prefix(bot, message):
    return '!'
    
function_list = []
    
#TODO: use named tuple for modules instead ?
    
def load_commands(bot, modules):
    
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
        
    @bot.command(name='unravel')
    async def test(ctx):
        print(ctx.message.content)
        print(ctx.channel)
        print(ctx.guild.voice_channels)
        print(ctx.bot.voice_clients)
        
    @bot.command(name='kusoge')
    async def quit(ctx):
        for i in modules:
            await i.close()
        #might want to sleep here
        await bot.logout()
        
    @bot.command()
    async def voice_connect(ctx):
        voice_channel = ctx.guild.get_channel(modules[0].voice_id)
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(voice_channel)
        await voice_channel.connect()
        
    @bot.command()
    async def voice_disconnect(ctx):
        if ctx.voice_client is not None:
            return await ctx.voice_client.disconnect()
    
    """
    @bot.command(name='initiate_listener')
    async def blackmagic(ctx):
        
        async def showdown_message(message):
            if message.author != bot.user and message.channel == ctx.channel and not message.content.startswith('!'):
                await ctx.send('multiply')
        
        function_list.append(showdown_message)
        bot.add_listener(showdown_message, 'on_message')
        
    @bot.command(name='remove_all')
    async def whitemagic(ctx):
    
        for f in function_list:
            bot.remove_listener(f, 'on_message')
    """