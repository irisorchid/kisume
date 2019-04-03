import random

def load_commands(bot, modules=None):
    
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
        
    @bot.command(name='kusoge')
    async def quit(ctx):
        await bot.logout()