def load_commands(bot, showdown):
    
    #restricts commands to channel_id
    def channel_restrict(f): pass
    
    #TODO: bind to channel
    @bot.command(name='showdown')
    async def pokemon(ctx):
        if ctx.channel.id != showdown.channel_id:
            return
        #bot.loop.create_task #timeout task
        
        #Critical, only run this once, check ws availability here? currrent stuff will break
        await showdown.connect_with_timeout(ctx)
        
        #if showdown doesn't have listener
        #add listener here with ctx.channel
        #also add listener to showdown
        
        #else, do nothing
        
    #should result gracefully with dynamic listener gone
    # @bot.command()
    # async def showdown_close(ctx):
        # await showdown.close()

def generate_showdown_commands(bot, showdown, ctx):

    async def showdown_commands(message):
        if message.author != bot.user and message.channel == ctx.channel and message.content.startswith('~'):
            args = message.lower().split(' ')
            command = args[0][1:]
            
            target = args[1]
            #TODO: assert valid target
            
            if not ctx.channel.id in showdown.rooms: return
            room = showdown.rooms[ctx.channel.id]
            if room is None: return
            
            if command == 'switch':
                await showdown.choose(room, command, target)
            if command == 'move':
                return
                if args[2] = 'mega': pass
                if args[2] = 'zmove': pass
            
    return showdown_commands
    
def load_showdown_commands(bot, showdown, ctx):
    showdown_commands = generate_showdown_commands(bot, showdown, ctx)
    showdown.listener[ctx.channel.id] = showdown_commands
    bot.add_listener(showdown_commands, 'on_message')

def unload_showdown_commands(bot, showdown, ctx):
    showdown_commands = showdown.listener.pop(ctx.channel.id, None)
    if showdown_commands is not None:
        bot.remove_listener(showdown_commands, 'on_message')