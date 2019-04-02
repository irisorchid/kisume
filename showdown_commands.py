def load_commands(bot, showdown):
    
    # @bot.command()
    # async def sdctest(ctx):
        # await ctx.send('hello')
    
    @bot.command(name='showdown2')
    async def pokemon(ctx):
        await showdown.run_timeout_instance(ctx)
        
    