def load_commands(bot, showdown):
    
    @bot.command(name='showdown')
    async def pokemon(ctx):
        #bot.loop.create_task #timeout task
        await showdown.run_timeout_instance(ctx)
        
    