def load_commands(bot, showdown):
    
    #restricts commands to channel_id
    def channel_restrict(f): pass
    
    @bot.command(name='showdown')
    async def pokemon(ctx):
        if ctx.channel.id != showdown.channel_id:
            return
        #bot.loop.create_task #timeout task
        await showdown.run_timeout_instance(ctx)
        
    @bot.command()
    async def switch(ctx, arg):
        #TODO: check valid arg
        await showdown.switch(showdown.rooms[ctx.channel.id], arg)
        
    @bot.command()
    async def sclose(ctx):
        await showdown.close()
        
    # @bot.listen('on_message')
    # async def showdown_message(message):
        # if message.author != bot.user and message.channel.name == 'bot-testing':
            # await message.channel.send('black magic')